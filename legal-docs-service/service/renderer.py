from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer

from .io import attachment_path
from .schemas import LegalDocumentDraft


# Bogotá uses UTC-5 year-round. A fixed offset avoids depending on the
# optional tzdata package on Windows.
BOGOTA_TZ = timezone(timedelta(hours=-5), name="America/Bogota")


def _safe(text: str | None) -> str:
    if not text:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _contact_line(label: str, value: str | None) -> str | None:
    return f"<b>{label}:</b> {_safe(value)}" if value else None


def render_pdf(*, draft: LegalDocumentDraft, case: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=LETTER,
        leftMargin=2.3 * cm,
        rightMargin=2.3 * cm,
        topMargin=2.1 * cm,
        bottomMargin=2.0 * cm,
    )
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        spaceAfter=7,
        alignment=TA_LEFT,
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        spaceBefore=10,
        spaceAfter=6,
    )
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=14,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8.5,
        leading=11,
        textColor="#444444",
    )

    story = []
    today = datetime.now(BOGOTA_TZ).strftime("%d/%m/%Y")
    city = (case.get("location") or {}).get("city") or "Colombia"
    story.append(Paragraph(f"{_safe(city)}, {today}", body))
    story.append(Spacer(1, 6))

    story.append(Paragraph(_safe(draft.title), title))
    story.append(Paragraph("Señores", body))
    story.append(Paragraph(f"<b>{_safe(draft.recipient.name or draft.recipient.role)}</b>", body))
    if draft.recipient.email:
        story.append(Paragraph(_contact_line("Correo", draft.recipient.email), body))
    if draft.recipient.address:
        story.append(Paragraph(_contact_line("Dirección", draft.recipient.address), body))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<b>Asunto:</b> {_safe(draft.subject)}", body))
    for identifier in draft.identifiers:
        story.append(Paragraph(f"<b>{_safe(identifier.label)}:</b> {_safe(identifier.value)}", body))
    story.append(Spacer(1, 8))
    story.append(Paragraph(_safe(draft.opening), body))

    story.append(Paragraph("1. Hechos y afectaciones", heading))
    for i, fact in enumerate(draft.facts, 1):
        story.append(Paragraph(f"{i}. {_safe(fact)}", body))
    if draft.damages:
        story.append(Paragraph("Afectaciones reportadas o visibles en el expediente:", body))
        for item in draft.damages:
            story.append(Paragraph(f"- {_safe(item)}", body))

    section_no = 2
    if draft.legal_reasoning:
        story.append(Paragraph(f"{section_no}. Consideraciones aplicadas al caso", heading))
        for idx, step in enumerate(draft.legal_reasoning, 1):
            story.append(Paragraph(f"<b>{section_no}.{idx} Regla aplicable.</b> {_safe(step.rule)}", body))
            story.append(Paragraph(f"<b>Aplicación al caso.</b> {_safe(step.case_application)}", body))
            story.append(Paragraph(f"<b>Por consiguiente.</b> {_safe(step.conclusion)}", body))
            story.append(Paragraph(f"Referencia: {_safe(step.citation_text)}", small))
        section_no += 1

    story.append(Paragraph(f"{section_no}. Solicitudes", heading))
    for i, request in enumerate(draft.requests, 1):
        story.append(Paragraph(f"{i}. {_safe(request)}", body))
    section_no += 1

    story.append(Paragraph(f"{section_no}. Anexos", heading))
    for item in draft.attachments:
        story.append(Paragraph(f"- {_safe(item.attachment_id)}: {_safe(item.label)}", body))
    for item in draft.evidence:
        story.append(Paragraph(f"- {_safe(item.evidence_id)}: {_safe(item.description)}", body))
    section_no += 1

    # Lawyer feedback: notification chapter/section is indispensable.
    story.append(Paragraph(f"{section_no}. Notificaciones y datos de contacto", heading))
    for contact in draft.notifications:
        story.append(Paragraph(f"<b>{_safe(contact.role)}</b>{': ' + _safe(contact.name) if contact.name else ''}", body))
        for line in [
            _contact_line("Correo", contact.email),
            _contact_line("Teléfono", contact.phone),
            _contact_line("Dirección", contact.address),
        ]:
            if line:
                story.append(Paragraph(line, body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(Paragraph(_safe(draft.closing), body))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Atentamente,", body))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f"<b>{_safe(draft.signature_name)}</b>", body))
    if draft.sender.identification:
        story.append(Paragraph(f"C.C. {_safe(draft.sender.identification)}", body))

    if draft.evidence:
        story.append(PageBreak())
        story.append(Paragraph("Anexo fotográfico", title))
        evidence_by_id = {str(x.get("id")): x for x in case.get("evidence", [])}
        for ev in draft.evidence:
            raw = evidence_by_id.get(ev.evidence_id)
            if not raw:
                continue
            p = attachment_path(raw)
            if not p or not p.exists():
                continue
            story.append(Paragraph(f"<b>{_safe(ev.evidence_id)} - {_safe(ev.title)}</b>", heading))
            story.append(Paragraph(_safe(ev.description), body))
            try:
                with PILImage.open(p) as img:
                    w, h = img.size
                max_w, max_h = 15.2 * cm, 15.5 * cm
                scale = min(max_w / w, max_h / h, 1.0)
                story.append(Image(str(p), width=w * scale, height=h * scale))
            except Exception:
                story.append(Paragraph("No fue posible renderizar esta imagen.", small))
            story.append(Spacer(1, 12))

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(2.3 * cm, 1.0 * cm, "Documento generado a partir del expediente suministrado. Verifique los datos antes de radicar.")
        canvas.drawRightString(LETTER[0] - 2.3 * cm, 1.0 * cm, f"Página {canvas.getPageNumber()}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
