from __future__ import annotations

import base64
import json
import mimetypes
import os
import re
from pathlib import Path

from dotenv import load_dotenv

from .io import PROJECT_ROOT
from .schemas import (
    AttachmentRef,
    EvidenceRef,
    Identifier,
    LegalDocumentDraft,
    LegalReasoningStep,
    NotificationContact,
    Party,
)


load_dotenv(PROJECT_ROOT / ".env")


def _read_prompt(name: str) -> str:
    return (PROJECT_ROOT / "prompts" / name).read_text(encoding="utf-8")


def _system_prompt(route: str) -> str:
    specific = "insurance_notice.md" if route == "insurance" else "rental_notice.md"
    return _read_prompt("common.md") + "\n\n" + _read_prompt(specific)


def _data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def _case_context(case: dict, knowledge: str, documents_text: dict[str, str]) -> str:
    docs = []
    for doc_id, text in documents_text.items():
        docs.append(f"\n### DOCUMENTO {doc_id}\n{text}")
    return (
        "# CASE_JSON\n"
        + json.dumps(case, ensure_ascii=False, indent=2)
        + "\n\n# KNOWLEDGE_BASE_MD\n"
        + knowledge
        + "\n\n# ATTACHED_DOCUMENT_TEXT\n"
        + ("\n".join(docs) if docs else "No hay texto documental extraido.")
    )


def generate_with_openai(
    *,
    route: str,
    case: dict,
    knowledge: str,
    documents_text: dict[str, str],
    images: list[tuple[str, Path]],
) -> LegalDocumentDraft:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en .env")

    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    effort = os.getenv("OPENAI_REASONING_EFFORT", "medium")
    max_images = int(os.getenv("MAX_EVIDENCE_IMAGES", "8"))

    content: list[dict] = [
        {
            "type": "input_text",
            "text": _case_context(case, knowledge, documents_text),
        }
    ]
    for evidence_id, path in images[:max_images]:
        content.append(
            {
                "type": "input_text",
                "text": f"La siguiente imagen corresponde a la evidencia {evidence_id}.",
            }
        )
        content.append(
            {
                "type": "input_image",
                "image_url": _data_url(path),
                "detail": "low",
            }
        )

    client = OpenAI(api_key=api_key)
    response = client.responses.parse(
        model=model,
        reasoning={"effort": effort},
        input=[
            {"role": "system", "content": _system_prompt(route)},
            {"role": "user", "content": content},
        ],
        text_format=LegalDocumentDraft,
    )
    draft = response.output_parsed
    if draft is None:
        raise RuntimeError("El modelo no devolvio un LegalDocumentDraft estructurado.")
    return draft


def _first_email(text: str, preferred: str | None = None) -> str | None:
    emails = re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text)
    if preferred:
        for email in emails:
            if preferred.lower() in email.lower():
                return email
    return emails[0] if emails else None


def _search_line(text: str, label: str) -> str | None:
    m = re.search(rf"{re.escape(label)}\s+([^\n]+)", text, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None


def _contact(case: dict) -> dict:
    return case.get("contact") or {}


def _evidence(case: dict) -> list[EvidenceRef]:
    return [
        EvidenceRef(
            evidence_id=str(item.get("id")),
            title=f"Evidencia {item.get('id')}",
            description=str(item.get("description") or "Imagen aportada con el caso"),
        )
        for item in case.get("evidence", [])
    ]


def _attachments(case: dict) -> list[AttachmentRef]:
    return [
        AttachmentRef(
            attachment_id=str(item.get("id")),
            label=str(item.get("filename") or item.get("description") or item.get("type") or "Documento"),
        )
        for item in case.get("documents", [])
    ]


def generate_mock(
    *, route: str, case: dict, knowledge: str, documents_text: dict[str, str]
) -> LegalDocumentDraft:
    """Deterministic local draft used by automated tests; no API key required."""
    doc_text = "\n".join(documents_text.values())
    claim = case.get("claim") or {}
    loc = case.get("location") or {}
    event = case.get("event") or {}
    contact = _contact(case)
    damages = [str(x.get("description")) for x in case.get("damage", [])]
    facts = [
        f"La persona informa un evento de tipo {event.get('type') or 'desastre'} ocurrido el {event.get('date') or 'fecha indicada en el expediente'}.",
        f"El inmueble reportado se encuentra en {loc.get('address') or 'la direccion registrada en el caso'}, {loc.get('city') or ''}.",
        str(event.get("description") or "Se reportaron afectaciones en el inmueble."),
    ]

    sender = Party(
        name=case.get("name"),
        role="Asegurado" if route == "insurance" else "Arrendataria",
        identification=case.get("cedula"),
        email=contact.get("email"),
        phone=contact.get("phone"),
        address=contact.get("notification_address") or loc.get("address"),
    )

    if route == "insurance":
        recipient = Party(
            name=claim.get("target"),
            role="Aseguradora",
            identification=None,
            email=_first_email(doc_text, "siniestros"),
            phone=_search_line(doc_text, "Línea nacional") or _search_line(doc_text, "Cali"),
            address=_search_line(doc_text, "Dirección"),
        )
        identifiers = []
        if claim.get("policy_number"):
            identifiers.append(Identifier(label="Poliza", value=str(claim["policy_number"])))
        return LegalDocumentDraft(
            document_type="insurance_loss_notice",
            title="Aviso de ocurrencia de siniestro",
            recipient=recipient,
            sender=sender,
            subject="Aviso de ocurrencia de siniestro y remision de evidencia fotografica",
            identifiers=identifiers,
            opening="Por medio de la presente pongo en conocimiento de la aseguradora la ocurrencia del evento y las afectaciones inicialmente observadas en el inmueble asegurado.",
            facts=facts,
            damages=damages,
            legal_reasoning=[],
            requests=[
                "Tener por informado el evento descrito en esta comunicacion.",
                "Confirmar la recepcion del aviso e indicar, si corresponde, el numero de siniestro o referencia para su seguimiento.",
                "Informar el canal o las instrucciones posteriores que deban seguirse para la evaluacion del caso.",
            ],
            evidence=_evidence(case),
            attachments=_attachments(case),
            notifications=[
                NotificationContact(name=sender.name, role=sender.role, email=sender.email, phone=sender.phone, address=sender.address),
                NotificationContact(name=recipient.name, role=recipient.role, email=recipient.email, phone=recipient.phone, address=recipient.address),
            ],
            closing="Adjunto las fotografias disponibles para documentar el estado observado. Esta comunicacion corresponde al aviso inicial del evento y no pretende cuantificar la perdida.",
            signature_name=str(case.get("name") or "Persona asegurada"),
            warnings=["Fixture sintetico de prueba. No constituye una reclamacion real."],
        )

    recipient_email = _first_email(doc_text, "contratos")
    recipient = Party(
        name=claim.get("target"),
        role="Inmobiliaria / administradora del contrato",
        identification=None,
        email=recipient_email,
        phone=None,
        address="Calle 10 # 00-00 Oficina 301, Cali" if "Calle 10 # 00-00" in doc_text else None,
    )
    reasoning = [
        LegalReasoningStep(
            rule="El arrendamiento tiene como finalidad permitir el uso y goce del inmueble para la destinacion pactada, y el arrendador debe mantenerlo en estado de servir para ese fin y atender las reparaciones necesarias que legalmente le correspondan.",
            case_application="El expediente reporta desprendimiento de cielo raso y una grieta, la salida preventiva de la arrendataria y una instruccion de la administracion de no regresar hasta que se realice una revision. No existe informe tecnico que permita afirmar destruccion total o dano estructural.",
            conclusion="Mientras se realiza la evaluacion, reparacion o habilitacion necesaria, se solicita una definicion escrita de las medidas contractuales aplicables y del tratamiento del canon, evitando presentar la terminacion como automatica sin soporte suficiente.",
            source_ids=["WEB-RENT-LEY820-BASE", "WEB-RENT-CC-1982-1985-2008"],
            citation_text="Ley 820 de 2003; Codigo Civil, arts. 1982, 1985 y 2008.",
        )
    ]
    return LegalDocumentDraft(
        document_type="rental_damage_notice",
        title="Comunicacion de afectacion del inmueble arrendado",
        recipient=recipient,
        sender=sender,
        subject="Notificacion de afectaciones, solicitud de evaluacion y definicion de medidas contractuales",
        identifiers=[Identifier(label="Contrato", value=str(claim.get("contract_reference") or "Contrato aportado"))],
        opening="Por medio de la presente informo las afectaciones reportadas despues del sismo y dejo constancia de la imposibilidad actual de retomar normalmente el uso residencial mientras esta pendiente la revision del inmueble.",
        facts=facts + ([str(event.get("authority_or_admin_instruction"))] if event.get("authority_or_admin_instruction") else []),
        damages=damages,
        legal_reasoning=reasoning,
        requests=[
            "Coordinar o informar la evaluacion del inmueble y las reparaciones o actuaciones necesarias para determinar cuando puede retomarse su uso residencial.",
            "Informar por escrito las condiciones para la rehabilitacion y eventual retorno al inmueble.",
            "Definir y ajustar el tratamiento del canon y de las obligaciones contractuales durante el periodo en que no ha sido posible ejercer el uso y goce residencial, evitando que se continue facturando como si el inmueble estuviera disponible para su destinacion ordinaria.",
        ],
        evidence=_evidence(case),
        attachments=_attachments(case),
        notifications=[
            NotificationContact(name=sender.name, role=sender.role, email=sender.email, phone=sender.phone, address=sender.address),
            NotificationContact(name=recipient.name, role=recipient.role, email=recipient.email, phone=recipient.phone, address=recipient.address),
        ],
        closing="Solicito respuesta escrita y que esta comunicacion se incorpore al expediente del contrato. Las fotografias se aportan como registro de las afectaciones visibles y no como dictamen tecnico.",
        signature_name=str(case.get("name") or "Arrendataria"),
        warnings=["Fixture sintetico de prueba."],
    )
