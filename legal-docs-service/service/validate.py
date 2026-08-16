from __future__ import annotations

import json
import re

from .schemas import AttachmentRef, EvidenceRef, LegalDocumentDraft


class DraftValidationError(ValueError):
    pass


def _all_text(draft: LegalDocumentDraft) -> str:
    return json.dumps(draft.model_dump(), ensure_ascii=False)


def _evidence_ref_from_case(item: dict, label: str | None = None) -> EvidenceRef:
    evidence_id = str(item.get("id"))
    description = str(item.get("description") or label or "Imagen aportada con el caso")
    return EvidenceRef(
        evidence_id=evidence_id,
        title=label or f"Evidencia {evidence_id}",
        description=description,
    )


def _attachment_ref_from_case(item: dict, label: str | None = None) -> AttachmentRef:
    attachment_id = str(item.get("id"))
    return AttachmentRef(
        attachment_id=attachment_id,
        label=label
        or str(
            item.get("filename")
            or item.get("description")
            or item.get("type")
            or "Documento"
        ),
    )


def reconcile_references(*, draft: LegalDocumentDraft, case: dict) -> list[str]:
    """Repair the common E-* vs DOC-* classification error from the LLM.

    For this MVP, references are deterministic because CASE_JSON is the source of truth:
    - CASE_JSON.evidence -> draft.evidence
    - CASE_JSON.documents -> draft.attachments

    Unknown references are discarded with a warning instead of aborting the PDF.
    Missing case references are appended so the generated PDF keeps the evidence bundle.
    """

    warnings: list[str] = []
    case_evidence = {
        str(item.get("id")): item
        for item in case.get("evidence", [])
        if item.get("id") is not None
    }
    case_documents = {
        str(item.get("id")): item
        for item in case.get("documents", [])
        if item.get("id") is not None
    }

    evidence_out: dict[str, EvidenceRef] = {}
    attachments_out: dict[str, AttachmentRef] = {}

    # First respect valid references returned in the expected fields.
    for item in draft.evidence:
        ref = item.evidence_id
        if ref in case_evidence:
            evidence_out[ref] = item
        elif ref in case_documents:
            warnings.append(
                f"El LLM puso el documento {ref} dentro de evidence; se movio automaticamente a attachments."
            )
            attachments_out[ref] = _attachment_ref_from_case(
                case_documents[ref], label=item.title or item.description
            )
        else:
            warnings.append(
                f"El LLM devolvio una referencia desconocida en evidence ({ref}); se omitio."
            )

    for item in draft.attachments:
        ref = item.attachment_id
        if ref in case_documents:
            attachments_out[ref] = item
        elif ref in case_evidence:
            warnings.append(
                f"El LLM puso la evidencia {ref} dentro de attachments; se movio automaticamente a evidence."
            )
            evidence_out[ref] = _evidence_ref_from_case(
                case_evidence[ref], label=item.label
            )
        else:
            warnings.append(
                f"El LLM devolvio una referencia desconocida en attachments ({ref}); se omitio."
            )

    # The input case is the source of truth for the bundle sent with the letter.
    # This also makes the demo robust if the model forgets to enumerate one photo/document.
    for ref, raw in case_documents.items():
        if ref not in attachments_out:
            attachments_out[ref] = _attachment_ref_from_case(raw)
            warnings.append(
                f"El documento {ref} estaba en CASE_JSON pero no en la salida del LLM; se agrego automaticamente."
            )

    for ref, raw in case_evidence.items():
        if ref not in evidence_out:
            evidence_out[ref] = _evidence_ref_from_case(raw)
            warnings.append(
                f"La evidencia {ref} estaba en CASE_JSON pero no en la salida del LLM; se agrego automaticamente."
            )

    draft.attachments = list(attachments_out.values())
    draft.evidence = list(evidence_out.values())
    return warnings


def validate_draft(
    *,
    route: str,
    draft: LegalDocumentDraft,
    case: dict,
    knowledge: str,
    strict: bool = False,
) -> list[str]:
    """Run only the minimal guardrails needed by the MVP.

    Default behavior is tolerant: repair what can be repaired and return warnings.
    Set strict=True (or STRICT_VALIDATION=true in the service) to turn the legal/content
    warnings below into blocking errors.
    """

    warnings = reconcile_references(draft=draft, case=case)

    expected = "insurance_loss_notice" if route == "insurance" else "rental_damage_notice"
    if draft.document_type != expected:
        # Wrong route is the one condition we never auto-correct because the whole letter
        # could have been generated with the wrong strategy.
        raise DraftValidationError(
            f"Tipo inesperado: {draft.document_type}; se esperaba {expected}."
        )

    case_name = str(case.get("name") or "").strip()
    if case_name and draft.signature_name.strip() != case_name:
        warnings.append(
            "La firma devuelta por el LLM no coincidia con el nombre del caso; se corrigio usando CASE_JSON."
        )
        draft.signature_name = case_name

    # Check KB references, but do not stop the hackathon demo unless strict mode is enabled.
    for step in draft.legal_reasoning:
        valid_source_ids: list[str] = []
        for source_id in step.source_ids:
            problem = None
            if source_id.startswith("REVIEW-"):
                problem = f"Bloque de revision no citable: {source_id}"
            elif not re.search(
                rf"^##\s+{re.escape(source_id)}\b", knowledge, flags=re.MULTILINE
            ):
                problem = f"Fuente juridica no encontrada como seccion en KB: {source_id}"

            if problem:
                if strict:
                    raise DraftValidationError(problem)
                warnings.append(problem)
            else:
                valid_source_ids.append(source_id)
        step.source_ids = valid_source_ids

    text = _all_text(draft).lower()

    if route == "insurance":
        # Lawyer feedback: the first insurance document is descriptive, not a legal brief.
        if draft.legal_reasoning:
            message = (
                "El LLM incluyo fundamento juridico visible en el aviso inicial de seguro; "
                "se elimino automaticamente para esta etapa."
            )
            if strict:
                raise DraftValidationError(message)
            warnings.append(message)
            draft.legal_reasoning = []

        forbidden = [
            "$280",
            "280.000",
            "280000",
            "cuantia total",
            "debe indemnizar",
            "exijo indemnizacion",
        ]
        matches = [term for term in forbidden if term in text]
        if matches:
            message = (
                "El aviso inicial parece incluir cuantificacion o lenguaje propio de una reclamacion "
                f"({', '.join(matches)}). Revise el PDF antes de radicar."
            )
            if strict:
                raise DraftValidationError(message)
            warnings.append(message)

    if route == "rental":
        if not draft.legal_reasoning:
            message = (
                "La comunicacion de arrendamiento no incluyo la subsuncion juridica esperada."
            )
            if strict:
                raise DraftValidationError(message)
            warnings.append(message)

        technical = str((case.get("event") or {}).get("technical_assessment") or "").strip()
        if not technical and re.search(r"\bel inmueble es inhabitable\b", text):
            message = (
                "El texto afirma inhabitabilidad sin soporte tecnico registrado en CASE_JSON."
            )
            if strict:
                raise DraftValidationError(message)
            warnings.append(message)

    return warnings
