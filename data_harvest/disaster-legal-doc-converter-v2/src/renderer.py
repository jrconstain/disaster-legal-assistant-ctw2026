from __future__ import annotations

import yaml

from .models import ContentBlock, DocumentConversionResult


def _drop_empty_metadata(data: dict) -> dict:
    """
    El Markdown solo recibe metadata realmente útil.
    Nulls, listas vacías y campos técnicos del pipeline NO se renderizan.
    """
    clean = {}
    for key, value in data.items():
        if value is None:
            continue
        if value == []:
            continue
        clean[key] = value
    return clean


def _escape_table_cell(value: str) -> str:
    return (
        value
        .replace("|", r"\|")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "<br>")
    )


def _render_table(block: ContentBlock) -> str:
    if not block.headers:
        return block.text or ""

    n = len(block.headers)
    header = "| " + " | ".join(_escape_table_cell(x) for x in block.headers) + " |"
    sep = "| " + " | ".join(["---"] * n) + " |"
    body = []

    for row in block.rows:
        row = list(row[:n]) + [""] * max(0, n - len(row))
        body.append(
            "| " + " | ".join(_escape_table_cell(x) for x in row) + " |"
        )

    return "\n".join([header, sep, *body])


def _blockquote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def render_block(block: ContentBlock) -> str:
    t = block.type

    if t == "heading":
        level = block.level or 2
        return ("#" * level) + " " + (block.title or block.text or "")

    if t == "paragraph":
        return block.text or ""

    if t == "numbered_item":
        number = (block.number or "").strip()
        if number and not number.endswith((".", ")", ":")):
            number += "."
        return f"{number} {block.text or ''}".strip()

    if t == "bullet_list":
        return "\n".join(f"- {item}" for item in block.items)

    if t == "legal_article":
        parts = []
        if block.title:
            parts.append(f"### {block.title}")
        if block.text:
            parts.append(block.text)
        return "\n\n".join(parts)

    if t == "legal_quote":
        label = "**Texto jurídico citado"
        if block.citation:
            label += f" — {block.citation}"
        label += "**"
        return f"> {label}\n>\n" + _blockquote(block.text or "")

    if t == "note":
        label = block.title or "Nota"
        return f"> **{label}:** {block.text or ''}"

    if t == "table":
        return _render_table(block)

    if t == "definition":
        return f"**{block.title or ''}:** {block.text or ''}"

    if t == "contact_block":
        parts = []
        if block.title:
            parts.append(f"### {block.title}")
        if block.text:
            parts.append(block.text)
        for item in block.contacts:
            if item.label:
                parts.append(f"**{item.label}:** {item.value}")
            else:
                parts.append(item.value)
        return "  \n".join(parts)

    if t == "quote":
        return _blockquote(block.text or "")

    if t == "divider":
        return "---"

    return block.text or ""


def render_markdown(result: DocumentConversionResult) -> str:
    metadata = _drop_empty_metadata(
        result.metadata.model_dump(mode="json")
    )

    # default_flow_style=None mantiene el dict legible pero compacta listas simples:
    # topics: [seguros, vivienda, terremoto]
    yaml_text = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        width=1200,
        default_flow_style=None,
    ).rstrip()

    body = "\n\n".join(
        rendered
        for block in result.blocks
        if (rendered := render_block(block).strip())
    )

    # processing_notes deliberadamente NO se incluyen en el .md.
    return f"---\n{yaml_text}\n---\n\n{body}\n"
