from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from app.config import Settings


def _safe_key(value: str) -> str:
    compact = re.sub(r'[^0-9A-Za-z_.-]+', '_', value).strip('_')[:60]
    digest = hashlib.sha1(value.encode('utf-8')).hexdigest()[:10]
    return f'{compact or "user"}_{digest}'


class CaseStore:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.root = settings.data_dir
        self.root.mkdir(parents=True, exist_ok=True)

    def case_dir(self, user_id: str) -> Path:
        path = self.root / 'cases' / _safe_key(user_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def case_path(self, user_id: str) -> Path:
        return self.case_dir(user_id) / 'case.json'

    def load(self, user_id: str) -> dict | None:
        path = self.case_path(user_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding='utf-8'))

    def save(self, user_id: str, case: dict) -> Path:
        case.setdefault('_jovita', {})['last_updated'] = datetime.now(timezone.utc).isoformat()
        path = self.case_path(user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(case, ensure_ascii=False, indent=2)
        # GCS FUSE is not a full POSIX FS; replace may fail across implementations.
        # Write temp in same directory and fall back to direct write.
        try:
            fd, tmp_name = tempfile.mkstemp(prefix='case_', suffix='.json', dir=str(path.parent))
            os.close(fd)
            tmp = Path(tmp_name)
            tmp.write_text(payload, encoding='utf-8')
            os.replace(tmp, path)
        except OSError:
            path.write_text(payload, encoding='utf-8')
        return path

    def persist_attachment(
        self,
        *,
        user_id: str,
        source_path: Path,
        filename: str | None = None,
        bucket: str = 'incoming',
    ) -> Path:
        target_dir = self.case_dir(user_id) / bucket
        target_dir.mkdir(parents=True, exist_ok=True)
        clean_name = re.sub(r'[^0-9A-Za-z._-]+', '_', filename or source_path.name)
        digest = hashlib.sha1(source_path.read_bytes()).hexdigest()[:10]
        target = target_dir / f'{digest}_{clean_name}'
        if source_path.resolve() != target.resolve():
            shutil.copy2(source_path, target)
        return target.resolve()

    def mark_processed(self, user_id: str, message_id: str) -> bool:
        """Returns False if message_id was already seen."""
        if not message_id:
            return True
        path = self.case_dir(user_id) / 'processed_message_ids.json'
        values: list[str] = []
        if path.exists():
            try:
                values = json.loads(path.read_text(encoding='utf-8'))
            except Exception:
                values = []
        if message_id in values:
            return False
        values.append(message_id)
        values = values[-500:]
        path.write_text(json.dumps(values, indent=2), encoding='utf-8')
        return True
