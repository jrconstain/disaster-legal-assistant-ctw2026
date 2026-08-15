from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from src.models import DocumentConversionResult
from src.pipeline import save_result
from src.state import StateStore, sha256_file


def main():
    fixture_path = BASE / "tests" / "fixtures" / "fasecolda_conversion.json"
    source_path = BASE / "input" / "FASECOLDA_comunicados_12aug-1357.pdf"
    output_dir = BASE / "examples" / "smoke_output"
    schema_path = BASE / "schemas" / "document_metadata.schema.json"

    raw = json.loads(fixture_path.read_text(encoding="utf-8"))
    result = DocumentConversionResult.model_validate(raw)

    saved = save_result(
        source_path=source_path,
        input_dir=BASE / "input",
        result=result,
        output_dir=output_dir,
        metadata_schema_path=schema_path,
    )

    # Test incremental state
    manifest = output_dir / ".state" / "manifest.json"
    if manifest.exists():
        manifest.unlink()

    state = StateStore(manifest)
    key = source_path.name
    digest = sha256_file(source_path)

    required = [
        saved["markdown"],
        saved["structured"],
        saved["qa"],
    ]

    first_action, first_reason = state.inspect(
        key,
        digest,
        required,
    )
    assert first_action == "PROCESS"
    assert first_reason == "nuevo"

    state.mark_success(
        key=key,
        source_hash=digest,
        source_size=source_path.stat().st_size,
        outputs={
            "markdown": str(saved["markdown"]),
            "structured": str(saved["structured"]),
            "qa": str(saved["qa"]),
        },
        model="offline-fixture",
    )

    second_action, second_reason = state.inspect(
        key,
        digest,
        required,
    )
    assert second_action == "SKIP"
    assert second_reason == "ya_convertido"

    print("SMOKE TEST OK")
    print("Primera inspección:", first_action, first_reason)
    print("Segunda inspección:", second_action, second_reason)
    print("Markdown:", saved["markdown"])
    print("Manifest:", manifest)


if __name__ == "__main__":
    main()
