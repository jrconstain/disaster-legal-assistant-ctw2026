from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import replace
from pathlib import Path

# Allow `python scripts/replay_markdown.py` from Windows/PowerShell without
# requiring the caller to set PYTHONPATH manually.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ai import build_provider
from app.config import PROJECT_ROOT, Settings
from app.engine import JovitaEngine
from app.legal_docs import LegalDocsClient
from app.scenario import attachment_from_scenario, load_scenario
from app.storage import CaseStore


def main() -> int:
    parser = argparse.ArgumentParser(description='Reproduce una conversación Jovita desde Markdown, sin WhatsApp.')
    parser.add_argument('--scenario', type=Path, default=PROJECT_ROOT / 'fixtures' / 'juan_jose' / 'conversation.md')
    parser.add_argument('--provider', choices=['mock', 'openai', 'gemini'], default='mock')
    parser.add_argument('--legal-docs-provider', choices=['mock', 'openai'], default='mock')
    parser.add_argument('--skip-docs', action='store_true', help='Prueba conversación/JSON sin invocar legal-docs-service.')
    parser.add_argument('--keep-data', action='store_true')
    args = parser.parse_args()

    settings = Settings.from_env()
    local_data = PROJECT_ROOT / 'data' / 'scenario_run'
    if local_data.exists() and not args.keep_data:
        shutil.rmtree(local_data)
    settings = replace(
        settings,
        data_dir=local_data,
        ai_provider=args.provider,
        legal_docs_provider=args.legal_docs_provider,
        legal_docs_mode='disabled' if args.skip_docs else settings.legal_docs_mode,
    )
    store = CaseStore(settings)
    ai = build_provider(settings, override=args.provider)
    engine = JovitaEngine(settings=settings, store=store, ai=ai, legal_docs=LegalDocsClient(settings))

    turns = load_scenario(args.scenario)
    user_id = '573001112233'
    print('\n=== JOVITA · REPLAY LOCAL DESDE MARKDOWN ===')
    print(f'Scenario: {args.scenario}')
    print(f'AI: {args.provider} | legal-docs: {settings.legal_docs_mode}/{args.legal_docs_provider}\n')

    for index, turn in enumerate(turns, start=1):
        text = str(turn.get('text') or '').strip()
        attachments = [
            attachment_from_scenario(PROJECT_ROOT, item)
            for item in (turn.get('attachments') or [])
        ]
        print(f'\n--- TURNO U{index:02d} ---')
        print('JUAN:', text or '[solo adjuntos]')
        for att in attachments:
            print(f'  + {att.kind}: {att.path}')
        result = engine.process(
            user_id=user_id,
            text=text,
            attachments=attachments,
            profile_name='Juan José',
            message_id=f'local-{index:02d}',
        )
        for event in result.events:
            if event.type in {'text', 'buttons'}:
                print('JOVITA:', event.text)
                if event.buttons:
                    print('  botones:', ', '.join(f"{b['title']} [{b['id']}]" for b in event.buttons))
            elif event.type == 'document':
                print('JOVITA: [PDF]', event.file_path)
        print('estado:', result.case.get('_jovita', {}).get('state'))

    final_case = store.load(user_id) or {}
    case_path = store.case_path(user_id)
    print('\n=== CASE.JSON FINAL ===')
    print(json.dumps(final_case, ensure_ascii=False, indent=2))
    print(f'\nGuardado en: {case_path.resolve()}')
    outputs = final_case.get('generated_outputs') or []
    if outputs and outputs[-1].get('pdf'):
        print(f"PDF legal: {outputs[-1]['pdf']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
