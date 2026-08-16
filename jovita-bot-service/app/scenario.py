from __future__ import annotations

import re
from pathlib import Path

import yaml

from app.models import LocalAttachment

TURN_RE = re.compile(r'```jovita-turn\s*\n(.*?)\n```', re.DOTALL)


def load_scenario(path: Path) -> list[dict]:
    text = path.read_text(encoding='utf-8')
    turns: list[dict] = []
    for raw in TURN_RE.findall(text):
        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            raise ValueError('Cada bloque jovita-turn debe ser un objeto YAML.')
        turns.append(data)
    if not turns:
        raise ValueError(f'No encontré bloques ```jovita-turn en {path}')
    return turns


def attachment_from_scenario(base: Path, raw: dict) -> LocalAttachment:
    path = Path(raw['path'])
    if not path.is_absolute():
        # Paths in the fixture are relative to jovita-bot-service root, not to the markdown file.
        root = base
        path = (root / path).resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    kind = raw.get('kind')
    mime = raw.get('mime_type')
    if not kind or not mime:
        raise ValueError(f'Attachment requires kind + mime_type: {raw}')
    return LocalAttachment(path=path, kind=kind, mime_type=mime, filename=raw.get('filename') or path.name)
