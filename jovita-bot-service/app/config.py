from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / '.env')


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().casefold() in {'1', 'true', 'yes', 'y', 'si', 'sí', 'on'}


@dataclass(frozen=True, slots=True)
class Settings:
    app_env: str
    data_dir: Path
    consent_more_info_url: str

    ai_provider: str
    openai_api_key: str
    openai_model: str
    openai_transcribe_model: str
    openai_image_detail: str
    openai_pdf_detail: str

    graph_api_version: str
    whatsapp_verify_token: str
    whatsapp_access_token: str
    whatsapp_phone_number_id: str
    meta_app_secret: str
    whatsapp_dry_run: bool

    legal_docs_mode: str
    legal_docs_root: Path
    legal_docs_url: str
    legal_docs_provider: str
    legal_docs_api_token: str
    knowledge_path: Path

    @classmethod
    def from_env(cls) -> 'Settings':
        repo_root = PROJECT_ROOT.parent
        legal_root = Path(
            os.getenv('LEGAL_DOCS_ROOT', str(repo_root / 'legal-docs-service'))
        ).expanduser()
        knowledge = Path(
            os.getenv(
                'LEGAL_DOCS_KNOWLEDGE_PATH',
                str(legal_root / 'knowledge' / 'knowledgebase_inmuebles_colombia_v0.1.md'),
            )
        ).expanduser()
        return cls(
            app_env=os.getenv('APP_ENV', 'development').strip(),
            data_dir=Path(os.getenv('DATA_DIR', str(PROJECT_ROOT / 'data'))).expanduser(),
            consent_more_info_url=os.getenv(
                'CONSENT_MORE_INFO_URL', 'https://example.com/privacidad'
            ).strip(),
            ai_provider=os.getenv('AI_PROVIDER', 'openai').strip().lower(),
            openai_api_key=os.getenv('OPENAI_API_KEY', '').strip(),
            openai_model=os.getenv('OPENAI_MODEL', 'gpt-5.6-luna').strip(),
            openai_transcribe_model=os.getenv(
                'OPENAI_TRANSCRIBE_MODEL', 'gpt-4o-mini-transcribe'
            ).strip(),
            openai_image_detail=os.getenv('OPENAI_IMAGE_DETAIL', 'low').strip(),
            openai_pdf_detail=os.getenv('OPENAI_PDF_DETAIL', 'high').strip(),
            graph_api_version=os.getenv('GRAPH_API_VERSION', 'v25.0').strip(),
            whatsapp_verify_token=os.getenv('WHATSAPP_VERIFY_TOKEN', '').strip(),
            whatsapp_access_token=os.getenv('WHATSAPP_ACCESS_TOKEN', '').strip(),
            whatsapp_phone_number_id=os.getenv('WHATSAPP_PHONE_NUMBER_ID', '').strip(),
            meta_app_secret=os.getenv('META_APP_SECRET', '').strip(),
            whatsapp_dry_run=env_bool('WHATSAPP_DRY_RUN', default=True),
            legal_docs_mode=os.getenv('LEGAL_DOCS_MODE', 'subprocess').strip().lower(),
            legal_docs_root=legal_root,
            legal_docs_url=os.getenv('LEGAL_DOCS_URL', '').rstrip('/'),
            legal_docs_provider=os.getenv('LEGAL_DOCS_PROVIDER', 'openai').strip().lower(),
            legal_docs_api_token=os.getenv('LEGAL_DOCS_API_TOKEN', '').strip(),
            knowledge_path=knowledge,
        )
