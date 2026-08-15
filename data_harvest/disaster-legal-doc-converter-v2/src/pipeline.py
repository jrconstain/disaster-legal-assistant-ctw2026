from __future__ import annotations

import json
import os
from pathlib import Path

from .models import DocumentConversionResult
from .qa import run_qa
from .renderer import render_markdown
from .schema_utils import validate_metadata


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".rtf",
    ".odt",
    ".txt",
    ".md",
    ".html",
    ".htm",
}


def discover_files(input_dir: Path) -> list[Path]:
    """
    Recursivo. Si después crean subcarpetas dentro de input/, también funciona.
    """
    return sorted(
        p for p in input_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def relative_source_key(source_path: Path, input_dir: Path) -> str:
    return source_path.relative_to(input_dir).as_posix()


def target_paths(
    source_path: Path,
    input_dir: Path,
    output_dir: Path,
) -> dict[str, Path]:
    rel = source_path.relative_to(input_dir)

    return {
        "markdown": output_dir / "markdown" / rel.with_suffix(".md"),
        "structured": output_dir / "structured" / rel.with_suffix(".json"),
        "qa": output_dir / "qa" / rel.with_suffix(".qa.json"),
        "error": output_dir / "errors" / rel.with_suffix(".error.json"),
    }


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def save_result(
    source_path: Path,
    input_dir: Path,
    result: DocumentConversionResult,
    output_dir: Path,
    metadata_schema_path: Path,
) -> dict[str, Path]:
    paths = target_paths(source_path, input_dir, output_dir)

    metadata = result.metadata.model_dump(mode="json")
    schema_errors = validate_metadata(
        metadata,
        metadata_schema_path,
    )

    if schema_errors:
        raise ValueError(
            "La metadata no cumple el schema compacto:\n- "
            + "\n- ".join(schema_errors)
        )

    markdown = render_markdown(result)
    qa = run_qa(source_path, result, markdown)

    _atomic_write_text(paths["markdown"], markdown)
    _atomic_write_text(
        paths["structured"],
        json.dumps(
            result.model_dump(mode="json"),
            ensure_ascii=False,
            indent=2,
        ),
    )
    _atomic_write_text(
        paths["qa"],
        json.dumps(qa, ensure_ascii=False, indent=2),
    )

    # Remove stale error after a successful retry.
    if paths["error"].exists():
        paths["error"].unlink()

    return paths


def process_one(
    source_path: Path,
    input_dir: Path,
    output_dir: Path,
    prompt_path: Path,
    metadata_schema_path: Path,
    model: str,
    detail: str,
    keep_openai_files: bool,
) -> tuple[DocumentConversionResult, dict[str, Path]]:
    # Lazy import allows offline smoke tests without OpenAI SDK/API key.
    from .openai_converter import convert_with_openai

    result = convert_with_openai(
        source_path=source_path,
        prompt_path=prompt_path,
        model=model,
        pdf_detail=detail,
        keep_openai_file=keep_openai_files,
    )

    paths = save_result(
        source_path=source_path,
        input_dir=input_dir,
        result=result,
        output_dir=output_dir,
        metadata_schema_path=metadata_schema_path,
    )

    return result, paths
