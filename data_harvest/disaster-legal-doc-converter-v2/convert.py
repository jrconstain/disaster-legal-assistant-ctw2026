from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.pipeline import (
    discover_files,
    process_one,
    relative_source_key,
    target_paths,
)
from src.state import PIPELINE_VERSION, StateStore, sha256_file


BASE = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Convierte incrementalmente documentos a Markdown canónico. "
            "Archivos ya convertidos y sin cambios NO vuelven a llamar la API."
        )
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=BASE / "input",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=BASE / "output",
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=BASE / "prompts" / "document_to_structured.md",
    )
    parser.add_argument(
        "--metadata-schema",
        type=Path,
        default=BASE / "schemas" / "document_metadata.schema.json",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--detail",
        choices=["auto", "low", "high"],
        default=None,
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocesa todos los archivos aunque ya estén convertidos.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué procesaría/omitiría sin llamar la API.",
    )
    parser.add_argument(
        "--keep-openai-files",
        action="store_true",
    )

    return parser.parse_args()


def main() -> int:
    load_dotenv(BASE / ".env")
    args = parse_args()

    model = args.model or os.getenv("OPENAI_MODEL", "gpt-5.6")
    detail = args.detail or os.getenv("PDF_DETAIL", "high")
    keep_openai_files = (
        args.keep_openai_files
        or os.getenv("KEEP_OPENAI_FILES", "false").lower() == "true"
    )

    if not args.input_dir.exists():
        print(f"ERROR: no existe {args.input_dir}", file=sys.stderr)
        return 2

    files = discover_files(args.input_dir)
    if not files:
        print(f"No encontré documentos en {args.input_dir}")
        return 0

    manifest_path = args.output_dir / ".state" / "manifest.json"
    state = StateStore(manifest_path)

    print(f"Pipeline: {PIPELINE_VERSION}")
    print(f"Modelo: {model}")
    print(f"Archivos encontrados: {len(files)}")
    print()

    plan = []

    for source in files:
        key = relative_source_key(source, args.input_dir)
        source_hash = sha256_file(source)
        paths = target_paths(
            source,
            args.input_dir,
            args.output_dir,
        )
        required = [
            paths["markdown"],
            paths["structured"],
            paths["qa"],
        ]

        if args.force:
            action, reason = "PROCESS", "force"
        else:
            action, reason = state.inspect(
                key=key,
                source_hash=source_hash,
                required_outputs=required,
            )

        plan.append(
            (source, key, source_hash, paths, action, reason)
        )

        print(f"{action:7} {key}  [{reason}]")

    if args.dry_run:
        to_process = sum(1 for x in plan if x[4] == "PROCESS")
        to_skip = sum(1 for x in plan if x[4] == "SKIP")
        print()
        print(f"Dry-run: procesaría {to_process}; omitiría {to_skip}.")
        return 0

    if not os.getenv("OPENAI_API_KEY"):
        if any(x[4] == "PROCESS" for x in plan):
            print(
                "\nERROR: hay archivos por procesar pero falta OPENAI_API_KEY.",
                file=sys.stderr,
            )
            return 2

    ok = 0
    skipped = 0
    failed = 0

    print("\n--- Conversión ---")

    for source, key, source_hash, paths, action, reason in plan:
        if action == "SKIP":
            print(f"SKIP    {key}")
            skipped += 1
            continue

        print(f"PROCESS {key}")

        try:
            _, saved = process_one(
                source_path=source,
                input_dir=args.input_dir,
                output_dir=args.output_dir,
                prompt_path=args.prompt,
                metadata_schema_path=args.metadata_schema,
                model=model,
                detail=detail,
                keep_openai_files=keep_openai_files,
            )

            output_strings = {
                name: str(path.relative_to(args.output_dir))
                for name, path in saved.items()
                if name != "error"
            }

            # CRITICAL: only mark complete AFTER every output was written.
            state.mark_success(
                key=key,
                source_hash=source_hash,
                source_size=source.stat().st_size,
                outputs=output_strings,
                model=model,
            )

            print(f"  ✓ {saved['markdown']}")
            ok += 1

        except Exception as exc:
            failed += 1
            paths["error"].parent.mkdir(parents=True, exist_ok=True)
            paths["error"].write_text(
                json.dumps(
                    {
                        "source_file": key,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"  ✗ {type(exc).__name__}: {exc}")
            print("    No se marcó como convertido; se reintentará en la próxima corrida.")

    print()
    print(
        f"Listo: convertidos={ok}, omitidos={skipped}, errores={failed}"
    )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
