from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from app.ai.mock_provider import MockProvider
from app.config import PROJECT_ROOT, Settings
from app.engine import JovitaEngine
from app.models import LocalAttachment
from app.scenario import attachment_from_scenario, load_scenario
from app.storage import CaseStore


class FakeLegalDocs:
    def __init__(self, out_dir: Path):
        self.out_dir = out_dir

    def generate(self, *, case_json_path: Path) -> dict:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        pdf = self.out_dir / 'document.pdf'
        pdf.write_bytes(b'%PDF-1.4\n% fake test pdf\n%%EOF\n')
        return {'status': 'generated', 'route': 'insurance', 'provider': 'mock', 'pdf': str(pdf.resolve())}


def _settings(tmp_path: Path) -> Settings:
    s = Settings.from_env()
    return replace(s, data_dir=tmp_path / 'data', ai_provider='mock', legal_docs_mode='disabled')


def test_first_message_is_fixed_welcome_and_consent(tmp_path):
    settings = _settings(tmp_path)
    store = CaseStore(settings)
    engine = JovitaEngine(settings=settings, store=store, ai=MockProvider(), legal_docs=FakeLegalDocs(tmp_path / 'out'))

    result = engine.process(user_id='57300', text='hola', message_id='m1')
    assert len(result.events) == 2
    assert result.events[0].type == 'text'
    assert result.events[0].text.startswith('Hola 👋 Soy Jovita')
    assert result.events[1].type == 'buttons'
    assert [b['id'] for b in result.events[1].buttons] == ['consent_yes', 'consent_no']
    assert result.case['consent'] is None
    # The first inbound text is not persisted into the case before consent.
    assert result.case['history'] == []


def test_full_juan_scenario_builds_case_and_triggers_legal_docs(tmp_path):
    settings = _settings(tmp_path)
    store = CaseStore(settings)
    engine = JovitaEngine(settings=settings, store=store, ai=MockProvider(), legal_docs=FakeLegalDocs(tmp_path / 'out'))
    turns = load_scenario(PROJECT_ROOT / 'fixtures' / 'juan_jose' / 'conversation.md')
    final = None
    for i, turn in enumerate(turns, 1):
        attachments = [attachment_from_scenario(PROJECT_ROOT, raw) for raw in turn.get('attachments', [])]
        final = engine.process(
            user_id='573001112233',
            text=str(turn.get('text') or ''),
            attachments=attachments,
            profile_name='Juan José',
            message_id=f'm{i}',
        )

    assert final is not None
    case = final.case
    assert case['name'] == 'Juan José Rojas Constaín'
    assert case['cedula'] == '1-113-682-988'
    assert case['ownership_status'] == 'owner'
    assert case['has_credit'] is True
    assert case['credit']['bank'] == 'Bancolombia'
    assert case['has_insurance'] is True
    assert case['_jovita']['route'] == 'insurance'
    assert case['claim']['policy_number'] == 'HOG-2026-0081640'
    assert case['event']['date'] == '2026-08-10'
    assert case['event']['approx_time'] == '7:34'
    assert len(case['documents']) == 1
    assert len(case['evidence']) == 3
    assert all(x['technical_conclusion'] is None for x in case['evidence'])
    assert case['is_confirmed'] is True
    assert case['_jovita']['state'] == 'ready_to_file'
    assert case['claim']['status'] == 'generated'
    assert Path(case['generated_outputs'][-1]['pdf']).exists()
    assert any(e.type == 'document' for e in final.events)
