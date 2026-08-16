from __future__ import annotations

import re
from pathlib import Path

from app.models import (
    DamageExtraction,
    ImageObservation,
    PolicyCoverage,
    PolicyExtraction,
    TriageExtraction,
)
from .base import AIProvider


class MockProvider(AIProvider):
    """Proveedor determinístico para probar el flujo sin red ni API keys."""

    def extract_triage(self, *, text: str, current_case: dict) -> TriageExtraction:
        low = text.casefold()
        out = TriageExtraction()

        if 'juan josé rojas' in low or 'juan jose rojas' in low:
            out.name = 'Juan José Rojas Constaín' if 'consta' in low else 'Juan José Rojas'
        ced = re.search(r'(?:c[eé]dula\s*(?:es|:)?)\s*([\d-]{8,})', low)
        if ced:
            out.cedula = ced.group(1)
        if 'soy el dueño' in low or 'soy dueño' in low or 'soy el propietario' in low:
            out.ownership_status = 'owner'
        if 'villas de guadalupe' in low:
            out.property_name = 'Villas de Guadalupe'
            out.building_type = 'apartment_in_horizontal_property'
        if 'carrera 56' in low and '14-57' in low:
            out.address = 'Carrera 56 # 14-57, Apartamento 402'
            out.city = 'Santiago de Cali'
            out.department = 'Valle del Cauca'
        if 'apartamento 402' in low:
            out.building_type = 'apartment_in_horizontal_property'
        if 'bancolombia' in low:
            out.has_credit = True
            out.bank = 'Bancolombia'
        if 'crédito hipotecario' in low or 'credito hipotecario' in low:
            out.has_credit = True
        if 'no me acuerdo de haberle comprado ningún seguro' in low or 'no recuerdo haber comprado' in low:
            out.has_insurance = None
        if 'sismo' in low or 'terremoto' in low:
            out.event_type = 'earthquake'
        if '10 de agosto' in low:
            out.event_date = '2026-08-10'
        time_match = re.search(r'(?:a las|como a las)\s*(\d{1,2}:\d{2})', low)
        if time_match:
            out.approx_time = time_match.group(1)
        if 'inhabitable' in low:
            out.user_reports_uninhabitable = True
        if 'techo' in low:
            out.damages.append(DamageExtraction(category='ceiling_damage', scope='private', description='El usuario reporta caída o desprendimiento de partes del techo/cielo raso.'))
        if 'pared' in low or 'paredes' in low:
            out.damages.append(DamageExtraction(category='wall_damage', scope='uncertain', description='El usuario reporta paredes severamente afectadas.'))
        if 'objetos' in low or 'enseres' in low:
            out.damages.append(DamageExtraction(category='contents_damage', scope='private', description='El usuario reporta destrucción de objetos o contenidos de la vivienda.'))
        if 'no he hecho reparaciones' in low or 'no hice reparaciones' in low:
            pass
        if 'no tengo cotización' in low or 'no tengo cotizacion' in low:
            pass
        return out

    def extract_policy(self, *, pdf_path: Path) -> PolicyExtraction:
        return PolicyExtraction(
            insurer='Seguros Horizonte Andino S.A.',
            policy_number='HOG-2026-0081640',
            insured_name='Juan José Rojas Constaín',
            insured_id='1-113-682-988',
            property_address='Carrera 56 # 14-57, Apartamento 402, Edificio Villas de Guadalupe, Santiago de Cali, Valle del Cauca',
            effective_from='2026-01-20',
            effective_to='2027-01-20',
            earthquake_coverage_found=True,
            coverages=[
                PolicyCoverage(name='Terremoto, temblor y erupción volcánica', building_limit_cop=480000000, contents_limit_cop=60000000, deductible='2% del valor asegurado del bien afectado, mínimo $2.000.000'),
            ],
            claim_channels=[
                '01 8000 000 426',
                '(602) 555 0142',
                'siniestros.hogar@horizonteandino.example',
                'https://horizonteandino.example/siniestros',
            ],
            mortgage_declared=False,
            onerous_beneficiary='Ninguno',
            warnings=['La póliza sintética indica que la hipoteca no fue declarada en este fixture; el usuario sí reportó crédito hipotecario con Bancolombia.'],
        )

    def observe_image(self, *, image_path: Path) -> ImageObservation:
        name = image_path.name.casefold()
        if 'fachada' in name or '03_' in name:
            return ImageObservation(
                short_description='Vista exterior con afectación severa visible en cerramientos/mampostería de fachada y material desprendido.',
                visible_elements=['mampostería desprendida', 'aberturas en fachada', 'escombros'],
                possible_scope='uncertain',
                technical_conclusion=None,
            )
        if 'escombro' in name or '02_' in name:
            return ImageObservation(
                short_description='Interior con abundantes escombros, elementos de mampostería y acabados desprendidos, y mobiliario desplazado.',
                visible_elements=['escombros', 'mampostería rota', 'acabados desprendidos', 'mobiliario desplazado'],
                possible_scope='private',
                technical_conclusion=None,
            )
        return ImageObservation(
            short_description='Interior con desprendimientos visibles de mampostería/acabados y acumulación de escombros.',
            visible_elements=['mampostería expuesta', 'material desprendido', 'escombros'],
            possible_scope='private',
            technical_conclusion=None,
        )

    def transcribe_audio(self, *, audio_path: Path) -> str:
        sidecar = audio_path.with_suffix(audio_path.suffix + '.txt')
        if sidecar.exists():
            return sidecar.read_text(encoding='utf-8').strip()
        raise RuntimeError('MockProvider necesita un sidecar .txt para simular transcripción.')
