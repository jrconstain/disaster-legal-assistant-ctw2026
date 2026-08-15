from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


DocumentType = Literal[
    "norma",
    "jurisprudencia",
    "acto_administrativo",
    "comunicado",
    "boletin",
    "guia",
    "protocolo",
    "manual",
    "preguntas_frecuentes",
    "pagina_institucional",
    "formulario",
    "convocatoria",
    "directorio",
    "informe",
    "reporte_situacion",
    "ficha_tecnica",
    "otro",
]

BlockType = Literal[
    "heading",
    "paragraph",
    "numbered_item",
    "bullet_list",
    "legal_article",
    "legal_quote",
    "note",
    "table",
    "definition",
    "contact_block",
    "quote",
    "divider",
]


class CompactMetadata(BaseModel):
    schema_version: Literal["2.0.0"] = "2.0.0"
    document_id: str
    title: str
    document_type: DocumentType
    issuer: str | None = None
    publication_date: str | None = None
    event_date: str | None = None
    jurisdiction: str | None = None
    source_file: str
    source_url: str | None = None
    topics: list[str] = Field(default_factory=list, max_length=5)


class ContactItem(BaseModel):
    label: str | None = None
    value: str


class ContentBlock(BaseModel):
    type: BlockType
    level: int | None = Field(default=None, ge=1, le=6)
    title: str | None = None
    number: str | None = None
    text: str | None = None
    citation: str | None = None
    items: list[str] = Field(default_factory=list)
    headers: list[str] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)
    contacts: list[ContactItem] = Field(default_factory=list)
    source_pages: list[int] = Field(default_factory=list)


class DocumentConversionResult(BaseModel):
    metadata: CompactMetadata
    blocks: list[ContentBlock]
    processing_notes: list[str] = Field(default_factory=list)
