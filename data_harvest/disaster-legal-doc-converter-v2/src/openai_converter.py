from __future__ import annotations

from datetime import date
from pathlib import Path

from openai import OpenAI

from .models import DocumentConversionResult
from .schema_utils import safe_document_id


def convert_with_openai(
    source_path: Path,
    prompt_path: Path,
    model: str,
    pdf_detail: str = "high",
    keep_openai_file: bool = False,
) -> DocumentConversionResult:
    client = OpenAI()
    prompt = prompt_path.read_text(encoding="utf-8")
    uploaded = None

    try:
        with source_path.open("rb") as fh:
            uploaded = client.files.create(
                file=fh,
                purpose="user_data",
            )

        file_item = {
            "type": "input_file",
            "file_id": uploaded.id,
        }

        if source_path.suffix.lower() == ".pdf":
            file_item["detail"] = pdf_detail

        user_text = (
            f"Convierte íntegramente el documento adjunto. "
            f"Nombre exacto del archivo fuente: {source_path.name}. "
            f"Fecha de procesamiento: {date.today().isoformat()}. "
            "La prioridad absoluta es conservar el contenido del documento."
        )

        response = client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": [
                        file_item,
                        {
                            "type": "input_text",
                            "text": user_text,
                        },
                    ],
                },
            ],
            text_format=DocumentConversionResult,
        )

        parsed = response.output_parsed
        if parsed is None:
            raise RuntimeError(
                "La API no devolvió una salida estructurada válida. "
                f"Salida parcial: {response.output_text[:1500]}"
            )

        # Provenance determinista: el modelo no decide el nombre real del archivo.
        parsed.metadata.source_file = source_path.name
        parsed.metadata.document_id = safe_document_id(
            parsed.metadata.document_id
        )

        return parsed

    finally:
        if uploaded is not None and not keep_openai_file:
            try:
                client.files.delete(uploaded.id)
            except Exception:
                pass
