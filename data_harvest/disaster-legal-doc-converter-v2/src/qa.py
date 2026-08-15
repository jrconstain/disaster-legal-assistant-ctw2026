from __future__ import annotations

from pathlib import Path

import fitz

from .models import DocumentConversionResult


def inspect_pdf(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    return {
        "page_count": len(doc),
        "local_extracted_characters": sum(
            len(page.get_text("text")) for page in doc
        ),
    }


def run_qa(
    source_path: Path,
    result: DocumentConversionResult,
    markdown: str,
) -> dict:
    local = (
        inspect_pdf(source_path)
        if source_path.suffix.lower() == ".pdf"
        else {}
    )

    warnings = []

    if not result.blocks:
        warnings.append("No se generaron bloques de contenido.")

    if local.get("page_count"):
        bad_pages = sorted({
            p
            for block in result.blocks
            for p in block.source_pages
            if p < 1 or p > local["page_count"]
        })
        if bad_pages:
            warnings.append(
                f"Se referencian páginas inexistentes: {bad_pages}"
            )

    table_blocks = [b for b in result.blocks if b.type == "table"]
    for idx, table in enumerate(table_blocks, 1):
        n = len(table.headers)
        if n and any(len(row) != n for row in table.rows):
            warnings.append(
                f"Tabla {idx}: hay filas con un número de celdas distinto "
                f"al número de encabezados ({n})."
            )

    return {
        "source_file": source_path.name,
        "pdf": local,
        "blocks": len(result.blocks),
        "tables": len(table_blocks),
        "markdown_characters": len(markdown),
        "processing_notes": result.processing_notes,
        "warnings": warnings,
        "passed": not warnings,
    }
