from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv

from .io import (
    PROJECT_ROOT,
    extract_attached_pdf_text,
    infer_route,
    load_case,
    load_knowledge,
    local_evidence_images,
    resolve_path,
)
from .llm import generate_mock, generate_with_openai
from .renderer import render_pdf
from .schemas import LegalDocumentDraft
from .validate import validate_draft


load_dotenv(PROJECT_ROOT / ".env")

# Bogotá uses UTC-5 year-round. Using a fixed offset avoids the optional
# Windows tzdata dependency that ZoneInfo("America/Bogota") would require.
BOGOTA_TZ = timezone(timedelta(hours=-5), name="America/Bogota")


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def generate_document(
    *,
    case_json_path: str | Path,
    knowledge_md_path: str | Path,
    route: str = "auto",
    provider: str | None = None,
    output_dir: str | Path | None = None,
    test_mode: bool = False,
    strict_validation: bool | None = None,
    draft_callback: Callable[[LegalDocumentDraft], None] | None = None,
) -> dict:
    """Generate one PDF from CASE_JSON + knowledge Markdown + referenced local files.

    This is intentionally the only service boundary the future trigger/webhook needs.

    `test_mode` does not change the legal content. It only labels the output and lets the
    console runner expose a human-readable preview before rendering.

    `draft_callback` is called immediately after the LLM returns and BEFORE reconciliation
    / validation. This is useful for the local demo because it lets us see what the model
    actually produced.
    """

    case = load_case(case_json_path)
    knowledge = load_knowledge(knowledge_md_path)
    actual_route = infer_route(case) if route == "auto" else route
    if actual_route not in {"insurance", "rental"}:
        raise ValueError("route debe ser auto, insurance o rental")

    documents_text = extract_attached_pdf_text(case)
    images = local_evidence_images(case)
    actual_provider = provider or os.getenv("LLM_PROVIDER", "openai")

    if actual_provider == "mock":
        draft = generate_mock(
            route=actual_route,
            case=case,
            knowledge=knowledge,
            documents_text=documents_text,
        )
    elif actual_provider == "openai":
        draft = generate_with_openai(
            route=actual_route,
            case=case,
            knowledge=knowledge,
            documents_text=documents_text,
            images=images,
        )
    else:
        raise ValueError("provider debe ser openai o mock")

    # In test mode we want to see the RAW structured answer before our deterministic
    # reconciliation fixes E-* / DOC-* placement or other small MVP issues.
    if draft_callback is not None:
        draft_callback(draft)

    if strict_validation is None:
        strict_validation = _env_bool("STRICT_VALIDATION", False)

    validation_warnings = validate_draft(
        route=actual_route,
        draft=draft,
        case=case,
        knowledge=knowledge,
        strict=strict_validation,
    )

    base_output = resolve_path(output_dir or os.getenv("OUTPUT_DIR", "outputs"))
    timestamp = datetime.now(BOGOTA_TZ).strftime("%Y%m%d_%H%M%S")
    phone = str(case.get("phone") or "case").replace("@lid", "").replace("/", "-")
    mode = "test" if test_mode else "run"
    folder = base_output / f"{timestamp}_{mode}_{actual_route}_{phone}"
    folder.mkdir(parents=True, exist_ok=True)

    draft_path = folder / "draft.json"
    pdf_path = folder / "document.pdf"
    draft_path.write_text(draft.model_dump_json(indent=2), encoding="utf-8")
    render_pdf(draft=draft, case=case, output_path=pdf_path)

    result = {
        "status": "generated",
        "mode": mode,
        "route": actual_route,
        "provider": actual_provider,
        "case_json": str(resolve_path(case_json_path)),
        "knowledge_md": str(resolve_path(knowledge_md_path)),
        "pdf": str(pdf_path.resolve()),
        "pdf_uri": pdf_path.resolve().as_uri(),
        "draft_json": str(draft_path.resolve()),
        "evidence_count": len(images),
        "document_count": len(documents_text),
        "validation_warnings": validation_warnings,
    }
    (folder / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def generate_from_trigger(
    trigger: dict,
    *,
    test_mode: bool = False,
    strict_validation: bool | None = None,
    draft_callback: Callable[[LegalDocumentDraft], None] | None = None,
) -> dict:
    return generate_document(
        case_json_path=trigger["case_json_path"],
        knowledge_md_path=trigger["knowledge_md_path"],
        route=trigger.get("route", "auto"),
        provider=trigger.get("provider"),
        output_dir=trigger.get("output_dir"),
        test_mode=test_mode,
        strict_validation=strict_validation,
        draft_callback=draft_callback,
    )
