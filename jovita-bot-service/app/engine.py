from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from app.ai import AIProvider
from app.config import Settings
from app.legal_docs import LegalDocsClient, LegalDocsError
from app.models import EngineResult, LocalAttachment, OutboundEvent, PolicyExtraction, TriageExtraction
from app.prompts import WELCOME_MESSAGE, consent_message
from app.storage import CaseStore

CONSENT_YES = 'consent_yes'
CONSENT_NO = 'consent_no'
CONFIRM_YES = 'confirm_yes'
CONFIRM_CORRECT = 'confirm_correct'


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _yes(text: str) -> bool:
    value = text.strip().casefold()
    if value in {'sí', 'si', 's', 'yes', 'y', 'dale', 'de una', 'hagámoslo', 'hagamoslo', 'listo'}:
        return True
    # Natural WhatsApp replies often add punctuation or another short phrase,
    # e.g. "Sí, hagámoslo". Keep this permissive only for explicit affirmative
    # starts / generation phrases.
    return (
        value.startswith('sí,')
        or value.startswith('si,')
        or value.startswith('sí ')
        or value.startswith('si ')
        or 'hagámoslo' in value
        or 'hagamoslo' in value
    )


def _no(text: str) -> bool:
    value = text.strip().casefold()
    return value in {'no', 'n', 'no autorizo', 'no gracias'}


def _base_case(user_id: str, profile_name: str | None = None) -> dict:
    return {
        'case_id': f'jovita-{re.sub(r"[^0-9A-Za-z]+", "-", user_id).strip("-")}',
        'phone': user_id,
        'name': profile_name,
        'cedula': None,
        'claim': {
            'type': 'insurance_loss_notice',
            'status': 'triage',
            'target': None,
            'policy_number': None,
            'requested_output': 'aviso inicial descriptivo del siniestro con fotos; sin cuantificar la reclamación',
        },
        'location': {
            'city': None,
            'department': None,
            'country': 'Colombia',
            'address': None,
            'property_name': None,
            'is_synthetic': True,
        },
        'ownership_status': 'unknown',
        'event': {
            'type': None,
            'date': None,
            'approx_time': None,
            'description': None,
            'technical_assessment': None,
            'authority_reported': False,
            'user_reports_uninhabitable': None,
        },
        'damage': [],
        'has_insurance': None,
        'has_credit': None,
        'credit': {'bank': None, 'status': 'unknown'},
        'building_type': 'unknown',
        'consent': None,
        'is_confirmed': False,
        'documents': [],
        'evidence': [],
        'expenses': [],
        'history': [],
        'contact': {'email': None, 'phone': user_id, 'notification_address': None},
        'generated_outputs': [],
        '_jovita': {
            'state': 'new',
            'route': None,
            'policy_extraction': None,
            'policy_match': None,
            'created_at': _now(),
        },
    }


def _append_history(case: dict, role: str, content: str, attachments: list[str] | None = None) -> None:
    row = {'role': role, 'content': content, 'timestamp': _now()}
    if attachments:
        row['attachments'] = attachments
    case.setdefault('history', []).append(row)


def _set_if(value, target: dict, key: str) -> None:
    if value is not None:
        target[key] = value


def _merge_triage(case: dict, extracted: TriageExtraction) -> None:
    _set_if(extracted.name, case, 'name')
    _set_if(extracted.cedula, case, 'cedula')
    if extracted.ownership_status and extracted.ownership_status != 'unknown':
        case['ownership_status'] = extracted.ownership_status
    loc = case['location']
    _set_if(extracted.address, loc, 'address')
    _set_if(extracted.city, loc, 'city')
    _set_if(extracted.department, loc, 'department')
    _set_if(extracted.property_name, loc, 'property_name')
    if extracted.building_type and extracted.building_type != 'unknown':
        case['building_type'] = extracted.building_type
    _set_if(extracted.has_credit, case, 'has_credit')
    if extracted.bank:
        case['credit']['bank'] = extracted.bank
        case['credit']['status'] = 'active_reported'
    _set_if(extracted.has_insurance, case, 'has_insurance')

    event = case['event']
    _set_if(extracted.event_type, event, 'type')
    _set_if(extracted.event_date, event, 'date')
    _set_if(extracted.approx_time, event, 'approx_time')
    _set_if(extracted.event_description, event, 'description')
    _set_if(extracted.user_reports_uninhabitable, event, 'user_reports_uninhabitable')

    existing = {(x.get('category'), x.get('description')) for x in case.get('damage', [])}
    for item in extracted.damages:
        key = (item.category, item.description)
        if key in existing:
            continue
        case['damage'].append(
            {
                'id': f'D-{len(case["damage"]) + 1:02d}',
                'category': item.category,
                'scope': item.scope,
                'description': item.description,
                'structural_damage_confirmed': False,
            }
        )
        existing.add(key)
    for item in extracted.expenses:
        case['expenses'].append(
            {
                'description': item.description,
                'amount_cop': item.amount_cop,
                'paid': item.paid,
                'support_document': None,
                'note': 'Soporte mencionado por el usuario.' if item.has_support else None,
            }
        )
    if extracted.email:
        case['contact']['email'] = extracted.email
    if case['location'].get('address'):
        case['contact']['notification_address'] = case['location']['address']



def _update_route(case: dict) -> None:
    """Keep a small deterministic routing label separate from LLM prose."""
    ownership = case.get('ownership_status')
    if ownership == 'tenant':
        case.setdefault('_jovita', {})['route'] = 'rental'
        return
    if ownership != 'owner':
        return
    if case.get('documents') and (case.get('_jovita') or {}).get('policy_match') is not False:
        case.setdefault('_jovita', {})['route'] = 'insurance'
    elif case.get('has_credit'):
        case.setdefault('_jovita', {})['route'] = 'mortgage_insurance'
    elif case.get('building_type') == 'apartment_in_horizontal_property':
        case.setdefault('_jovita', {})['route'] = 'horizontal_property'
    else:
        case.setdefault('_jovita', {})['route'] = 'coverage_discovery'

def _normalize_id(value: str | None) -> str:
    return re.sub(r'\D+', '', value or '')


def _norm_words(value: str | None) -> set[str]:
    clean = re.sub(r'[^a-z0-9áéíóúñ]+', ' ', (value or '').casefold())
    return {x for x in clean.split() if len(x) > 2}


def _policy_matches_case(case: dict, policy: PolicyExtraction) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if case.get('cedula') and policy.insured_id:
        if _normalize_id(case['cedula']) != _normalize_id(policy.insured_id):
            reasons.append('La identificación del asegurado no coincide con la del caso.')
    if case.get('name') and policy.insured_name:
        case_words = _norm_words(case['name'])
        policy_words = _norm_words(policy.insured_name)
        if case_words and len(case_words & policy_words) < min(2, len(case_words)):
            reasons.append('El nombre del asegurado no parece coincidir con la persona del caso.')
    address = (case.get('location') or {}).get('address')
    if address and policy.property_address:
        required = {x for x in _norm_words(address) if any(c.isdigit() for c in x) or x in {'carrera', 'apartamento'}}
        if required and len(required & _norm_words(policy.property_address)) < max(1, len(required) // 2):
            reasons.append('La dirección asegurada no parece coincidir con el inmueble del caso.')
    return not reasons, reasons


def _policy_to_document(case: dict, path: Path, policy: PolicyExtraction) -> dict:
    return {
        'id': f'DOC-INS-{len(case.get("documents", [])) + 1:02d}',
        'type': 'insurance_policy',
        'filename': path.name,
        'source': 'local',
        'local_path': str(path.resolve()),
        'url': None,
        'mime_type': 'application/pdf',
        'is_synthetic': True,
        'extracted': policy.model_dump(mode='json'),
    }


def _summary(case: dict) -> str:
    claim = case.get('claim') or {}
    event = case.get('event') or {}
    location = case.get('location') or {}
    policy = (case.get('_jovita') or {}).get('policy_extraction') or {}
    damage_lines = '\n'.join(f"• {d.get('description')}" for d in case.get('damage', [])[:6]) or '• Sin detalle'
    evidence = case.get('evidence', [])
    return (
        'Antes de generar, revisa que esto esté bien:\n\n'
        f"👤 *Nombre:* {case.get('name') or 'Pendiente'}\n"
        f"🪪 *Cédula:* {case.get('cedula') or 'Pendiente'}\n"
        f"🏠 *Inmueble:* {location.get('address') or 'Pendiente'}"
        f"{', ' + location.get('property_name') if location.get('property_name') else ''}\n"
        f"📄 *Póliza:* {policy.get('policy_number') or claim.get('policy_number') or 'Pendiente'} — "
        f"{policy.get('insurer') or claim.get('target') or 'aseguradora por confirmar'}\n"
        f"🌎 *Evento:* {event.get('type') or 'emergencia'} — {event.get('date') or 'fecha pendiente'}"
        f"{(' ' + event.get('approx_time')) if event.get('approx_time') else ''}\n"
        f"📷 *Fotos guardadas:* {len(evidence)}\n\n"
        f"*Daños reportados/observados:*\n{damage_lines}\n\n"
        'El documento será un *aviso inicial descriptivo del siniestro*. No voy a afirmar que la aseguradora ya aceptó cobertura ni a inventar una cuantía.'
    )


def _readiness(case: dict) -> tuple[bool, list[str]]:
    missing: list[str] = []
    if case.get('ownership_status') != 'owner':
        missing.append('confirmar que eres propietario')
    if not case.get('name'):
        missing.append('nombre')
    if not case.get('cedula'):
        missing.append('identificación')
    if not (case.get('location') or {}).get('address'):
        missing.append('dirección del inmueble')
    if not (case.get('event') or {}).get('date'):
        missing.append('fecha del evento')
    if not case.get('documents'):
        missing.append('póliza')
    if not case.get('evidence'):
        missing.append('al menos una foto de evidencia')
    if (case.get('_jovita') or {}).get('policy_match') is False:
        missing.append('una póliza que coincida con la persona y el inmueble')
    return not missing, missing


class JovitaEngine:
    def __init__(
        self,
        *,
        settings: Settings,
        store: CaseStore,
        ai: AIProvider,
        legal_docs: LegalDocsClient | None = None,
    ):
        self.settings = settings
        self.store = store
        self.ai = ai
        self.legal_docs = legal_docs or LegalDocsClient(settings)

    def process(
        self,
        *,
        user_id: str,
        text: str = '',
        attachments: Iterable[LocalAttachment] = (),
        profile_name: str | None = None,
        message_id: str | None = None,
    ) -> EngineResult:
        case = self.store.load(user_id) or _base_case(user_id, profile_name)
        state = case['_jovita'].get('state', 'new')
        text = (text or '').strip()
        attachments = list(attachments)

        if message_id and not self.store.mark_processed(user_id, message_id):
            return EngineResult(events=[], case=case)

        if state == 'new':
            # Before consent, do not run extraction and do not persist the user's
            # free-text message in the case history. The inbound transport has already
            # delivered it, but Jovita only starts case processing after authorization.
            case['_jovita']['state'] = 'consent_pending'
            case['claim']['status'] = 'triage'
            events = [
                OutboundEvent(type='text', text=WELCOME_MESSAGE),
                OutboundEvent(
                    type='buttons',
                    text=consent_message(self.settings.consent_more_info_url),
                    buttons=[
                        {'id': CONSENT_YES, 'title': '✅ Sí'},
                        {'id': CONSENT_NO, 'title': '❌ No'},
                    ],
                ),
            ]
            self.store.save(user_id, case)
            return EngineResult(events=events, case=case)

        if state == 'consent_pending':
            if text == CONSENT_NO or _no(text):
                case['consent'] = False
                case['_jovita']['state'] = 'consent_denied'
                msg = 'Entendido. No analizaré ni usaré la información de tu caso. Si cambias de opinión, puedes volver a escribir y empezar de nuevo.'
                _append_history(case, 'user', text or 'No')
                _append_history(case, 'assistant', msg)
                self.store.save(user_id, case)
                return EngineResult(events=[OutboundEvent(type='text', text=msg)], case=case)
            if text == CONSENT_YES or _yes(text):
                case['consent'] = True
                case['_jovita']['state'] = 'triage'
                msg = 'Listo. Ahora sí, cuéntame qué pasó como te salga. Si tienes una póliza, contrato, fotos o notas de voz, puedes mandarlas en cualquier momento.'
                _append_history(case, 'user', text or 'Sí')
                _append_history(case, 'assistant', msg)
                self.store.save(user_id, case)
                return EngineResult(events=[OutboundEvent(type='text', text=msg)], case=case)
            msg = 'Necesito que me confirmes primero si autorizas el tratamiento de tus datos para analizar el caso.'
            return EngineResult(
                events=[OutboundEvent(type='buttons', text=msg, buttons=[{'id': CONSENT_YES, 'title': '✅ Sí'}, {'id': CONSENT_NO, 'title': '❌ No'}])],
                case=case,
            )

        if not case.get('consent'):
            return EngineResult(events=[OutboundEvent(type='text', text='Para continuar necesito tu autorización de tratamiento de datos.')], case=case)

        if state == 'ready_to_confirm' and (text == CONFIRM_YES or _yes(text)):
            _append_history(case, 'user', text or 'Confirmo')
            case['is_confirmed'] = True
            case['claim']['status'] = 'ready_to_generate'
            case['_jovita']['state'] = 'generating'
            case_path = self.store.save(user_id, case)
            try:
                generated = self.legal_docs.generate(case_json_path=case_path)
            except LegalDocsError as exc:
                case['_jovita']['state'] = 'generation_error'
                case['is_confirmed'] = False
                case['claim']['status'] = 'ready_to_generate'
                error_text = f'Tus datos quedaron confirmados, pero falló la generación del PDF: {exc}'
                _append_history(case, 'assistant', error_text)
                self.store.save(user_id, case)
                return EngineResult(events=[OutboundEvent(type='text', text=error_text)], case=case)

            case.setdefault('generated_outputs', []).append(generated)
            if generated.get('status') == 'skipped':
                # Useful for local conversation/JSON tests: confirmation is real, but
                # generation was deliberately disabled by the runner.
                case['_jovita']['state'] = 'ready_to_generate'
                case['claim']['status'] = 'ready_to_generate'
                msg = (
                    'Caso confirmado. En este modo de prueba omití la llamada al generador jurídico; '
                    'el case.json quedó listo para disparar legal-docs-service.'
                )
                _append_history(case, 'assistant', msg)
                self.store.save(user_id, case)
                return EngineResult(events=[OutboundEvent(type='text', text=msg)], case=case)

            case['_jovita']['state'] = 'ready_to_file'
            case['claim']['status'] = 'generated'
            pdf = generated.get('pdf')
            msg = 'Listo. Generé el aviso inicial del siniestro con la información que confirmaste y las evidencias guardadas. Revísalo antes de radicarlo.'
            _append_history(case, 'assistant', msg)
            self.store.save(user_id, case)
            events = [OutboundEvent(type='text', text=msg)]
            if pdf and Path(pdf).exists():
                events.append(OutboundEvent(type='document', file_path=str(Path(pdf).resolve()), filename='aviso_inicial_siniestro_Juan_Jose_Rojas.pdf', caption='Aviso inicial del siniestro'))
            return EngineResult(events=events, case=case)

        if state == 'ready_to_confirm' and text == CONFIRM_CORRECT:
            case['_jovita']['state'] = 'collecting_evidence'
            msg = 'Claro. Dime qué dato debo corregir y lo actualizo antes de generar.'
            _append_history(case, 'user', text)
            _append_history(case, 'assistant', msg)
            self.store.save(user_id, case)
            return EngineResult(events=[OutboundEvent(type='text', text=msg)], case=case)

        attachment_refs: list[str] = []
        notes: list[str] = []
        for att in attachments:
            persisted = self.store.persist_attachment(user_id=user_id, source_path=att.path, filename=att.filename, bucket='attachments')
            if att.kind == 'audio':
                transcript = self.ai.transcribe_audio(audio_path=persisted)
                text = f'{text}\n{transcript}'.strip()
                notes.append('Transcribí la nota de voz y la incorporé al relato.')
            elif att.kind == 'document' and att.mime_type == 'application/pdf':
                policy = self.ai.extract_policy(pdf_path=persisted)
                doc = _policy_to_document(case, persisted, policy)
                case['documents'].append(doc)
                attachment_refs.append(doc['id'])
                case['_jovita']['policy_extraction'] = policy.model_dump(mode='json')
                match, reasons = _policy_matches_case(case, policy)
                case['_jovita']['policy_match'] = match
                if match:
                    case['has_insurance'] = True
                    if policy.insured_name and (not case.get('name') or len(policy.insured_name) > len(str(case.get('name') or ''))):
                        case['name'] = policy.insured_name
                    if policy.insured_id and not case.get('cedula'):
                        case['cedula'] = policy.insured_id
                    case['claim']['target'] = policy.insurer
                    case['claim']['policy_number'] = policy.policy_number
                    notes.append('Leí la póliza y coincide con la identidad y el inmueble del caso.')
                    if policy.earthquake_coverage_found:
                        notes.append('Encontré un amparo relacionado con terremoto/temblor; esto no equivale a una decisión de cobertura del siniestro.')
                    if policy.warnings:
                        notes.extend(policy.warnings)
                else:
                    notes.append('No puedo usar esta póliza todavía: ' + ' '.join(reasons))
            elif att.kind == 'image':
                observation = self.ai.observe_image(image_path=persisted)
                ev_id = f'E-{len(case.get("evidence", [])) + 1:02d}'
                case['evidence'].append(
                    {
                        'id': ev_id,
                        'type': 'image',
                        'description': observation.short_description,
                        'source': 'local',
                        'local_path': str(persisted.resolve()),
                        'url': None,
                        'mime_type': att.mime_type,
                        'user_reported': True,
                        'model_observation': observation.short_description,
                        'technical_conclusion': None,
                        'is_synthetic': True,
                    }
                )
                attachment_refs.append(ev_id)
            elif att.kind == 'video':
                ev_id = f'E-{len(case.get("evidence", [])) + 1:02d}'
                case['evidence'].append(
                    {
                        'id': ev_id,
                        'type': 'video',
                        'description': 'Video aportado por el usuario; conservado como evidencia sin conclusión técnica automática en este MVP.',
                        'source': 'local',
                        'local_path': str(persisted.resolve()),
                        'url': None,
                        'mime_type': att.mime_type,
                        'user_reported': True,
                        'model_observation': None,
                        'technical_conclusion': None,
                        'is_synthetic': True,
                    }
                )
                attachment_refs.append(ev_id)

        if text and text not in {CONFIRM_YES, CONFIRM_CORRECT}:
            extracted = self.ai.extract_triage(text=text, current_case=case)
            _merge_triage(case, extracted)
            _update_route(case)
            _append_history(case, 'user', text, attachment_refs or None)
        elif attachment_refs:
            _append_history(case, 'user', 'Adjuntó archivos al caso.', attachment_refs)

        _update_route(case)
        ready, missing = _readiness(case)
        policy = case.get('_jovita', {}).get('policy_extraction') or {}
        policy_match = case.get('_jovita', {}).get('policy_match')

        if policy_match is False:
            case['_jovita']['state'] = 'waiting_document'
            msg = 'Recibí el PDF, pero los datos de la póliza no coinciden suficientemente con la persona o el inmueble del caso. Revisa si enviaste el archivo correcto.'
        elif not case.get('documents'):
            case['_jovita']['state'] = 'waiting_document'
            bank = (case.get('credit') or {}).get('bank')
            bank_phrase = f' con {bank}' if bank else ''
            msg = (
                'Por lo que me cuentas, eres propietario y todavía tienes un crédito hipotecario'
                f'{bank_phrase}. Aunque no recuerdes haber comprado un seguro por separado, vale la pena localizar la póliza vigente asociada al inmueble. '
                'Puedes pedir al banco el certificado o póliza de incendio/terremoto y enviármelo aquí en PDF. También puedes mandarme desde ya las fotos de los daños; las iré guardando sin sacar conclusiones estructurales.'
            )
        elif not case.get('evidence'):
            case['_jovita']['state'] = 'collecting_evidence'
            earthquake = ' un amparo relacionado con terremoto' if policy.get('earthquake_coverage_found') else ' información de cobertura'
            msg = (
                f'Póliza recibida. Identifiqué {policy.get("insurer") or "la aseguradora"}, la póliza {policy.get("policy_number") or ""} y{earthquake}. '
                'Eso nos permite avanzar, pero no significa todavía que la aseguradora haya aceptado todos los daños. Envíame las fotos o videos que tengas; los organizaré como evidencia sin diagnosticar daño estructural.'
            )
        elif not (case.get('event') or {}).get('date'):
            case['_jovita']['state'] = 'collecting_evidence'
            msg = (
                f'Ya guardé {len(case.get("evidence", []))} evidencias. En las imágenes puedo describir desprendimientos, mampostería dañada y escombros visibles, pero no determinar estabilidad o habitabilidad por foto. '
                'Solo me falta una cosa importante para el aviso: ¿qué día ocurrió el sismo o cuándo notaste los daños? Si recuerdas la hora aproximada, dímela también. Y cuéntame si ya pagaste alguna reparación o medida provisional.'
            )
        elif ready:
            case['_jovita']['state'] = 'ready_to_offer'
            case['claim']['status'] = 'ready_to_confirm'
            msg = (
                'Con lo que ya tengo podemos preparar un *aviso inicial del siniestro*: identifica la póliza, el inmueble, el evento y las evidencias disponibles, sin tener que inventar una cotización completa ni afirmar que la cobertura ya fue aceptada. '
                '¿Quieres que lo prepare ahora?'
            )
        else:
            case['_jovita']['state'] = 'collecting_evidence'
            msg = 'Voy bien con el expediente. Me falta: ' + ', '.join(missing) + '.'

        # Offering is a separate gate: a yes after this message opens confirmation.
        if state == 'ready_to_offer' and _yes(text):
            case['_jovita']['state'] = 'ready_to_confirm'
            msg = _summary(case)
            events = [
                OutboundEvent(
                    type='buttons',
                    text=msg,
                    buttons=[
                        {'id': CONFIRM_YES, 'title': '✅ Confirmar'},
                        {'id': CONFIRM_CORRECT, 'title': '✏️ Corregir'},
                    ],
                )
            ]
        else:
            prefix = (' '.join(notes) + '\n\n') if notes else ''
            events = [OutboundEvent(type='text', text=prefix + msg)]

        _append_history(case, 'assistant', events[0].text or '')
        self.store.save(user_id, case)
        return EngineResult(events=events, case=case)
