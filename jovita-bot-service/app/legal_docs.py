from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import requests

from app.config import Settings


class LegalDocsError(RuntimeError):
    pass


class LegalDocsClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, *, case_json_path: Path) -> dict:
        mode = self.settings.legal_docs_mode
        if mode == 'disabled':
            return {'status': 'skipped', 'reason': 'LEGAL_DOCS_MODE=disabled'}
        if mode == 'http':
            return self._http(case_json_path)
        if mode == 'subprocess':
            return self._subprocess(case_json_path)
        raise LegalDocsError(f'LEGAL_DOCS_MODE inválido: {mode}')

    def _subprocess(self, case_json_path: Path) -> dict:
        root = self.settings.legal_docs_root.resolve()
        main_py = root / 'main.py'
        if not main_py.exists():
            raise LegalDocsError(
                f'No encuentro legal-docs-service en {root}. '
                'Ponlo como carpeta hermana o define LEGAL_DOCS_ROOT.'
            )
        if not self.settings.knowledge_path.exists():
            raise LegalDocsError(f'No encuentro knowledge base: {self.settings.knowledge_path}')

        command = [
            sys.executable,
            str(main_py),
            '--case',
            str(case_json_path.resolve()),
            '--knowledge',
            str(self.settings.knowledge_path.resolve()),
            '--route',
            'insurance',
            '--provider',
            self.settings.legal_docs_provider,
        ]
        env = os.environ.copy()
        env.setdefault('LLM_PROVIDER', self.settings.legal_docs_provider)
        proc = subprocess.run(
            command,
            cwd=str(root),
            env=env,
            text=True,
            capture_output=True,
            timeout=240,
        )
        if proc.returncode != 0:
            raise LegalDocsError(
                'legal-docs-service falló.\n'
                f'STDOUT:\n{proc.stdout[-4000:]}\nSTDERR:\n{proc.stderr[-4000:]}'
            )
        # The normal CLI prints the result JSON. Be tolerant if logs precede it.
        stdout = proc.stdout.strip()
        starts = [i for i, c in enumerate(stdout) if c == '{']
        for start in starts:
            try:
                data = json.loads(stdout[start:])
                if isinstance(data, dict) and 'status' in data:
                    return data
            except json.JSONDecodeError:
                continue
        raise LegalDocsError(f'No pude leer JSON de legal-docs-service: {stdout[-4000:]}')

    def _http(self, case_json_path: Path) -> dict:
        if not self.settings.legal_docs_url:
            raise LegalDocsError('LEGAL_DOCS_URL es obligatorio con LEGAL_DOCS_MODE=http.')
        headers = {}
        if self.settings.legal_docs_api_token:
            headers['Authorization'] = f'Bearer {self.settings.legal_docs_api_token}'
        payload = {
            'case_json_path': str(case_json_path.resolve()),
            'knowledge_md_path': str(self.settings.knowledge_path),
            'route': 'insurance',
            'provider': self.settings.legal_docs_provider,
        }
        response = requests.post(
            f'{self.settings.legal_docs_url}/generate',
            json=payload,
            headers=headers,
            timeout=240,
        )
        if not response.ok:
            raise LegalDocsError(f'HTTP {response.status_code}: {response.text[:2000]}')
        return response.json()
