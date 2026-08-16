from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_path(path: str | Path, base: Path | None = None) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    base = base or PROJECT_ROOT
    return (base / p).resolve()


def load_json(path: str | Path) -> dict[str, Any]:
    p = resolve_path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def unwrap_case(payload: dict[str, Any]) -> dict[str, Any]:
    """Accept direct case or WhatsApp shape {phone@lid: {...}}."""
    if "phone" in payload:
        return payload
    if len(payload) == 1:
        key, value = next(iter(payload.items()))
        if isinstance(value, dict):
            if "phone" not in value:
                value = {"phone": str(key), **value}
            return value
    raise ValueError("No pude identificar un caso en el JSON.")


def load_case(path: str | Path) -> dict[str, Any]:
    return unwrap_case(load_json(path))


def load_knowledge(path: str | Path) -> str:
    return resolve_path(path).read_text(encoding="utf-8")


def attachment_path(item: dict[str, Any]) -> Path | None:
    local_path = item.get("local_path")
    if not local_path:
        return None
    return resolve_path(local_path)


def extract_attached_pdf_text(case: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in case.get("documents", []):
        p = attachment_path(item)
        if not p or not p.exists() or p.suffix.lower() != ".pdf":
            continue
        reader = PdfReader(str(p))
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
        out[str(item.get("id", p.name))] = "\n\n".join(x for x in pages if x)
    return out


def local_evidence_images(case: dict[str, Any]) -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    for item in case.get("evidence", []):
        if not str(item.get("mime_type", "")).startswith("image/"):
            continue
        p = attachment_path(item)
        if p and p.exists():
            result.append((str(item.get("id", p.stem)), p))
    return result


def infer_route(case: dict[str, Any]) -> LiteralRoute:
    claim_type = str((case.get("claim") or {}).get("type") or "").lower()
    if "rental" in claim_type:
        return "rental"
    if "insurance" in claim_type:
        return "insurance"
    if str(case.get("ownership_status", "")).lower() in {"tenant", "arrendatario", "arrendataria"}:
        return "rental"
    if case.get("has_insurance") is True:
        return "insurance"
    raise ValueError("No pude inferir la ruta. Use route='insurance' o route='rental'.")


LiteralRoute = str
