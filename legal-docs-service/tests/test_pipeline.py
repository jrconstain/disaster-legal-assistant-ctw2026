from __future__ import annotations

import json
from pathlib import Path

from service.service import generate_document


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge/knowledgebase_inmuebles_colombia_v0.1.md"


def test_insurance_notice_mock(tmp_path):
    result = generate_document(
        case_json_path=ROOT / "fixtures/insurance_case_01/case.json",
        knowledge_md_path=KB,
        route="insurance",
        provider="mock",
        output_dir=tmp_path,
    )
    assert Path(result["pdf"]).exists()
    draft = json.loads(Path(result["draft_json"]).read_text(encoding="utf-8"))
    assert draft["document_type"] == "insurance_loss_notice"
    assert draft["legal_reasoning"] == []
    all_text = json.dumps(draft, ensure_ascii=False)
    assert "280000" not in all_text
    assert len(draft["notifications"]) >= 2


def test_rental_notice_mock(tmp_path):
    result = generate_document(
        case_json_path=ROOT / "fixtures/rental_case_01/case.json",
        knowledge_md_path=KB,
        route="rental",
        provider="mock",
        output_dir=tmp_path,
    )
    assert Path(result["pdf"]).exists()
    draft = json.loads(Path(result["draft_json"]).read_text(encoding="utf-8"))
    assert draft["document_type"] == "rental_damage_notice"
    assert draft["legal_reasoning"]
    assert "WEB-RENT-CC-1982-1985-2008" in draft["legal_reasoning"][0]["source_ids"]
    assert len(draft["notifications"]) >= 2
