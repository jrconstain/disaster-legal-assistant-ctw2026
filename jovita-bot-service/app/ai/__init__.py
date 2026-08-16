from __future__ import annotations

from app.config import Settings
from .base import AIProvider
from .mock_provider import MockProvider


def build_provider(settings: Settings, override: str | None = None) -> AIProvider:
    name = (override or settings.ai_provider).strip().lower()
    if name == 'mock':
        return MockProvider()
    if name == 'openai':
        from .openai_provider import OpenAIProvider
        return OpenAIProvider(settings)
    if name == 'gemini':
        from .gemini_provider import GeminiProvider
        return GeminiProvider()
    raise ValueError(f'AI_PROVIDER no soportado: {name}')


__all__ = ['AIProvider', 'build_provider']
