from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


PIPELINE_VERSION = "2.0.0"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class StateStore:
    """
    Manifiesto incremental.

    Una conversión se considera reutilizable solo si:
    - existe una entrada para la ruta relativa del archivo,
    - el SHA-256 sigue siendo el mismo,
    - la versión del pipeline coincide,
    - y siguen existiendo todas las salidas requeridas.

    Si una conversión falla, NO se marca como exitosa.
    """

    def __init__(self, manifest_path: Path):
        self.path = manifest_path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {
                "manifest_version": 1,
                "pipeline_version": PIPELINE_VERSION,
                "files": {},
            }
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            data.setdefault("files", {})
            return data
        except Exception:
            # Do not silently overwrite a corrupt manifest.
            raise RuntimeError(
                f"El manifiesto de estado está corrupto: {self.path}. "
                "Revísalo o elimínalo para reconstruir el estado."
            )

    def save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(tmp, self.path)

    def inspect(
        self,
        key: str,
        source_hash: str,
        required_outputs: list[Path],
    ) -> tuple[str, str]:
        record = self.data["files"].get(key)

        if record is None:
            return "PROCESS", "nuevo"

        if record.get("pipeline_version") != PIPELINE_VERSION:
            return "PROCESS", "version_pipeline_cambio"

        if record.get("sha256") != source_hash:
            return "PROCESS", "archivo_modificado"

        missing = [str(p) for p in required_outputs if not p.exists()]
        if missing:
            return "PROCESS", "salida_faltante"

        if record.get("status") != "success":
            return "PROCESS", "conversion_anterior_incompleta"

        return "SKIP", "ya_convertido"

    def mark_success(
        self,
        key: str,
        source_hash: str,
        source_size: int,
        outputs: dict[str, str],
        model: str,
    ) -> None:
        self.data["pipeline_version"] = PIPELINE_VERSION
        self.data["files"][key] = {
            "status": "success",
            "sha256": source_hash,
            "size_bytes": source_size,
            "pipeline_version": PIPELINE_VERSION,
            "model": model,
            "converted_at_utc": utc_now(),
            "outputs": outputs,
        }
        self.save()
