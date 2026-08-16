from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.models import ImageObservation, PolicyExtraction, TriageExtraction


class AIProvider(ABC):
    @abstractmethod
    def extract_triage(self, *, text: str, current_case: dict) -> TriageExtraction:
        raise NotImplementedError

    @abstractmethod
    def extract_policy(self, *, pdf_path: Path) -> PolicyExtraction:
        raise NotImplementedError

    @abstractmethod
    def observe_image(self, *, image_path: Path) -> ImageObservation:
        raise NotImplementedError

    @abstractmethod
    def transcribe_audio(self, *, audio_path: Path) -> str:
        raise NotImplementedError
