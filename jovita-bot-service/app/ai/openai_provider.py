from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from openai import OpenAI

from app.config import Settings
from app.models import ImageObservation, PolicyExtraction, TriageExtraction
from app.prompts import (
    IMAGE_SYSTEM_PROMPT,
    POLICY_SYSTEM_PROMPT,
    TRIAGE_SYSTEM_PROMPT,
    case_context_for_llm,
)
from .base import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(self, settings: Settings):
        if not settings.openai_api_key:
            raise RuntimeError('OPENAI_API_KEY no está configurada.')
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def extract_triage(self, *, text: str, current_case: dict) -> TriageExtraction:
        response = self.client.responses.parse(
            model=self.settings.openai_model,
            input=[
                {'role': 'system', 'content': TRIAGE_SYSTEM_PROMPT},
                {
                    'role': 'user',
                    'content': (
                        'Estado actual del caso (solo contexto; no lo repitas como si '
                        'fuera nuevo):\n'
                        f'{case_context_for_llm(current_case)}\n\n'
                        'Nuevo mensaje del usuario del que debes extraer novedades:\n'
                        f'{text}'
                    ),
                },
            ],
            text_format=TriageExtraction,
        )
        if response.output_parsed is None:
            raise RuntimeError(f'OpenAI no devolvió extracción estructurada: {response.output_text[:1000]}')
        return response.output_parsed

    def extract_policy(self, *, pdf_path: Path) -> PolicyExtraction:
        uploaded = None
        try:
            with pdf_path.open('rb') as fh:
                uploaded = self.client.files.create(file=fh, purpose='user_data')
            response = self.client.responses.parse(
                model=self.settings.openai_model,
                input=[
                    {'role': 'system', 'content': POLICY_SYSTEM_PROMPT},
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'input_file',
                                'file_id': uploaded.id,
                                'detail': self.settings.openai_pdf_detail,
                            },
                            {
                                'type': 'input_text',
                                'text': 'Extrae los datos de esta póliza para el expediente. No decidas la cobertura del caso.',
                            },
                        ],
                    },
                ],
                text_format=PolicyExtraction,
            )
            if response.output_parsed is None:
                raise RuntimeError(f'OpenAI no devolvió extracción de póliza: {response.output_text[:1000]}')
            return response.output_parsed
        finally:
            if uploaded is not None:
                try:
                    self.client.files.delete(uploaded.id)
                except Exception:
                    pass

    def observe_image(self, *, image_path: Path) -> ImageObservation:
        mime = mimetypes.guess_type(image_path.name)[0] or 'image/jpeg'
        data = base64.b64encode(image_path.read_bytes()).decode('ascii')
        response = self.client.responses.parse(
            model=self.settings.openai_model,
            input=[
                {'role': 'system', 'content': IMAGE_SYSTEM_PROMPT},
                {
                    'role': 'user',
                    'content': [
                        {'type': 'input_text', 'text': 'Describe esta evidencia de manera prudente.'},
                        {
                            'type': 'input_image',
                            'image_url': f'data:{mime};base64,{data}',
                            'detail': self.settings.openai_image_detail,
                        },
                    ],
                },
            ],
            text_format=ImageObservation,
        )
        if response.output_parsed is None:
            raise RuntimeError(f'OpenAI no devolvió observación de imagen: {response.output_text[:1000]}')
        return response.output_parsed

    def transcribe_audio(self, *, audio_path: Path) -> str:
        with audio_path.open('rb') as fh:
            result = self.client.audio.transcriptions.create(
                model=self.settings.openai_transcribe_model,
                file=fh,
            )
        text = getattr(result, 'text', None)
        if not text:
            raise RuntimeError('La transcripción no devolvió texto.')
        return str(text).strip()
