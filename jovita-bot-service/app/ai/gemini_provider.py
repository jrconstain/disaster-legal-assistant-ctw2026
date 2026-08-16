from __future__ import annotations

from pathlib import Path

from app.models import ImageObservation, PolicyExtraction, TriageExtraction
from .base import AIProvider


class GeminiProvider(AIProvider):
    """Punto de extensión deliberado para Gemini + Google Search.

    El motor de conversación no depende del SDK de OpenAI. Cuando se implemente
    Gemini, basta con satisfacer esta interfaz y seleccionar AI_PROVIDER=gemini.
    La búsqueda web oficial debería vivir aquí como una capacidad del provider,
    no mezclada con el estado del caso.
    """

    def _todo(self):
        raise NotImplementedError(
            'GeminiProvider está preparado como interfaz pero no se implementa en este MVP.'
        )

    def extract_triage(self, *, text: str, current_case: dict) -> TriageExtraction:
        self._todo()

    def extract_policy(self, *, pdf_path: Path) -> PolicyExtraction:
        self._todo()

    def observe_image(self, *, image_path: Path) -> ImageObservation:
        self._todo()

    def transcribe_audio(self, *, audio_path: Path) -> str:
        self._todo()
