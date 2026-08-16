from __future__ import annotations

import argparse
import json
from pathlib import Path

from service.io import PROJECT_ROOT, load_case, load_json, resolve_path
from service.schemas import LegalDocumentDraft
from service.service import generate_document, generate_from_trigger


DEMO_CASES = {
    "insurance": PROJECT_ROOT / "fixtures/insurance_case_01/case.json",
    "rental": PROJECT_ROOT / "fixtures/rental_case_01/case.json",
}
DEFAULT_KB = PROJECT_ROOT / "knowledge/knowledgebase_inmuebles_colombia_v0.1.md"


def _short(value: str | None, limit: int = 150) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _print_case_summary(
    *,
    case: dict,
    case_path: Path,
    knowledge_path: Path,
    route: str,
    provider: str,
) -> None:
    documents = case.get("documents", [])
    evidence = case.get("evidence", [])
    location = case.get("location") or {}
    claim = case.get("claim") or {}

    print("\n" + "=" * 68)
    print("MODO PRUEBA LOCAL · GENERADOR DE DOCUMENTOS")
    print("=" * 68)
    print(f"Persona:      {case.get('name') or case.get('phone')}")
    print(f"Ruta:         {route}")
    print(f"Proveedor:    {provider}")
    print(f"Inmueble:     {location.get('address') or 'No indicado'}")
    print(f"Destino:      {claim.get('target') or 'Se extraera del expediente'}")
    print(f"Documentos:   {len(documents)}")
    print(f"Evidencias:   {len(evidence)}")
    print(f"CASE_JSON:    {resolve_path(case_path)}")
    print(f"KNOWLEDGE_MD: {resolve_path(knowledge_path)}")
    print("\nEl servicio va a consumir estos datos, llamar al LLM y construir el PDF localmente.")


def _print_llm_preview(draft: LegalDocumentDraft) -> None:
    """Show part of the RAW structured LLM response before PDF rendering."""

    print("\n" + "-" * 68)
    print("PRE-RESPUESTA ESTRUCTURADA DEL LLM (ANTES DE RENDERIZAR)")
    print("-" * 68)
    print(f"Tipo:         {draft.document_type}")
    print(f"Titulo:       {_short(draft.title)}")
    print(f"Destinatario: {_short(draft.recipient.name or draft.recipient.role)}")
    print(f"Asunto:       {_short(draft.subject)}")
    print(f"Apertura:     {_short(draft.opening, 220)}")

    if draft.facts:
        print("\nHechos (muestra):")
        for fact in draft.facts[:3]:
            print(f"  - {_short(fact, 220)}")

    if draft.damages:
        print("\nAfectaciones (muestra):")
        for damage in draft.damages[:3]:
            print(f"  - {_short(damage, 220)}")

    if draft.requests:
        print("\nSolicitudes (muestra):")
        for request in draft.requests[:3]:
            print(f"  - {_short(request, 220)}")

    if draft.attachments:
        print("\nAttachments devueltos por el LLM:")
        print("  " + ", ".join(x.attachment_id for x in draft.attachments))
    if draft.evidence:
        print("Evidence devuelta por el LLM:")
        print("  " + ", ".join(x.evidence_id for x in draft.evidence))

    print("-" * 68)
    print("Ahora se reconciliaran referencias E-* / DOC-* y se renderizara el PDF.\n")


def _run_test_mode(*, case_path: Path, knowledge_path: Path, route: str, provider: str, run) -> None:
    case = load_case(case_path)
    _print_case_summary(
        case=case,
        case_path=case_path,
        knowledge_path=knowledge_path,
        route=route,
        provider=provider,
    )

    while True:
        answer = input("\nEscribe ACTIVAR para ejecutar la prueba o SALIR: ").strip().lower()
        if answer == "salir":
            print("Prueba cancelada.")
            return
        if answer != "activar":
            print("Comando no reconocido.")
            continue

        print("\nActivando flujo...")
        print("1/3 Leyendo JSON, Markdown, PDFs y evidencias locales...")
        print("2/3 Llamando al LLM para producir LegalDocumentDraft...")

        result = run(_print_llm_preview)

        print("3/3 PDF construido programaticamente.")
        warnings = result.get("validation_warnings") or []
        if warnings:
            print("\nAvisos de reconciliacion/validacion (NO bloquearon la prueba):")
            for warning in warnings:
                print(f"  - {warning}")

        print("\n" + "=" * 68)
        print("PRUEBA TERMINADA")
        print("=" * 68)
        print(f"PDF:   {result['pdf']}")
        print(f"ABRIR: {result['pdf_uri']}")
        print(f"Draft: {result['draft_json']}")
        print("\nEn PowerShell/Windows Terminal, normalmente puedes Ctrl+click sobre ABRIR.")
        return


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generador local minimal de documentos legales CTW 2026"
    )
    parser.add_argument("--demo", choices=["insurance", "rental"], help="Usar fixture incluido")
    parser.add_argument("--case", dest="case_path", help="Ruta local al JSON del caso")
    parser.add_argument(
        "--knowledge",
        default=str(DEFAULT_KB),
        help="Ruta local al Markdown de knowledge base",
    )
    parser.add_argument("--route", choices=["auto", "insurance", "rental"], default="auto")
    parser.add_argument("--provider", choices=["openai", "mock"], default=None)
    parser.add_argument(
        "--test",
        action="store_true",
        help="Modo prueba: muestra datos, pide ACTIVAR, enseña preview del LLM y link al PDF",
    )
    # Backwards compatibility with the previous repo command.
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Alias legacy de --test",
    )
    parser.add_argument("--strict", action="store_true", help="Convertir warnings juridicos en errores")
    parser.add_argument("--trigger", help="JSON pequeno con case_json_path + knowledge_md_path")
    args = parser.parse_args()

    provider = args.provider or "openai"
    test_mode = args.test or args.interactive

    if args.trigger:
        trigger = load_json(args.trigger)
        case_path = Path(trigger["case_json_path"])
        knowledge_path = Path(trigger["knowledge_md_path"])
        route = trigger.get("route", "auto")
        provider = trigger.get("provider") or provider

        # Resolve route for the console label without changing the trigger itself.
        case = load_case(case_path)
        if route == "auto":
            claim_type = str((case.get("claim") or {}).get("type") or "")
            route_label = "rental" if "rental" in claim_type else "insurance"
        else:
            route_label = route

        def run(callback=None):
            return generate_from_trigger(
                trigger,
                test_mode=test_mode,
                strict_validation=args.strict,
                draft_callback=callback,
            )

    else:
        case_path = DEMO_CASES[args.demo] if args.demo else Path(args.case_path or "")
        if not str(case_path):
            parser.error("Use --demo, --case o --trigger")

        knowledge_path = Path(args.knowledge)
        route = args.demo if args.demo else args.route
        case = load_case(case_path)
        if route == "auto":
            claim_type = str((case.get("claim") or {}).get("type") or "")
            route_label = "rental" if "rental" in claim_type else "insurance"
        else:
            route_label = route

        def run(callback=None):
            return generate_document(
                case_json_path=case_path,
                knowledge_md_path=knowledge_path,
                route=route,
                provider=provider,
                test_mode=test_mode,
                strict_validation=args.strict,
                draft_callback=callback,
            )

    if test_mode:
        _run_test_mode(
            case_path=case_path,
            knowledge_path=knowledge_path,
            route=route_label,
            provider=provider,
            run=run,
        )
    else:
        result = run()
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
