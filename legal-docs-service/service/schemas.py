from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Party(StrictModel):
    name: str | None
    role: str
    identification: str | None
    email: str | None
    phone: str | None
    address: str | None


class Identifier(StrictModel):
    label: str
    value: str


class LegalReasoningStep(StrictModel):
    """Subsumption: abstract rule -> case facts -> legal consequence/request."""

    rule: str
    case_application: str
    conclusion: str
    source_ids: list[str]
    citation_text: str


class EvidenceRef(StrictModel):
    evidence_id: str
    title: str
    description: str


class AttachmentRef(StrictModel):
    attachment_id: str
    label: str


class NotificationContact(StrictModel):
    name: str | None
    role: str
    email: str | None
    phone: str | None
    address: str | None


class LegalDocumentDraft(StrictModel):
    document_type: Literal["insurance_loss_notice", "rental_damage_notice"]
    title: str
    recipient: Party
    sender: Party
    subject: str
    identifiers: list[Identifier]
    opening: str
    facts: list[str]
    damages: list[str]
    legal_reasoning: list[LegalReasoningStep]
    requests: list[str]
    evidence: list[EvidenceRef]
    attachments: list[AttachmentRef]
    notifications: list[NotificationContact]
    closing: str
    signature_name: str
    warnings: list[str]
