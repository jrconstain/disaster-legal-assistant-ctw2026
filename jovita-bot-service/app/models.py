from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class DamageExtraction(BaseModel):
    category: str
    description: str
    scope: Literal['private', 'common', 'uncertain'] = 'uncertain'


class ExpenseExtraction(BaseModel):
    description: str
    amount_cop: int | None = None
    paid: bool = False
    has_support: bool = False


class TriageExtraction(BaseModel):
    name: str | None = None
    cedula: str | None = None
    ownership_status: Literal['owner', 'tenant', 'other', 'unknown'] | None = None
    address: str | None = None
    city: str | None = None
    department: str | None = None
    property_name: str | None = None
    building_type: Literal[
        'apartment_in_horizontal_property', 'house', 'other', 'unknown'
    ] | None = None
    has_credit: bool | None = None
    bank: str | None = None
    has_insurance: bool | None = None
    event_type: str | None = None
    event_date: str | None = Field(default=None, description='YYYY-MM-DD if stated')
    approx_time: str | None = None
    event_description: str | None = None
    user_reports_uninhabitable: bool | None = None
    damages: list[DamageExtraction] = Field(default_factory=list)
    expenses: list[ExpenseExtraction] = Field(default_factory=list)
    email: str | None = None


class PolicyCoverage(BaseModel):
    name: str
    building_limit_cop: int | None = None
    contents_limit_cop: int | None = None
    deductible: str | None = None


class PolicyExtraction(BaseModel):
    insurer: str | None = None
    policy_number: str | None = None
    insured_name: str | None = None
    insured_id: str | None = None
    property_address: str | None = None
    effective_from: str | None = None
    effective_to: str | None = None
    earthquake_coverage_found: bool = False
    coverages: list[PolicyCoverage] = Field(default_factory=list)
    claim_channels: list[str] = Field(default_factory=list)
    mortgage_declared: bool | None = None
    onerous_beneficiary: str | None = None
    warnings: list[str] = Field(default_factory=list)


class ImageObservation(BaseModel):
    short_description: str
    visible_elements: list[str] = Field(default_factory=list)
    possible_scope: Literal['private', 'common', 'uncertain'] = 'uncertain'
    technical_conclusion: None = None


class LocalAttachment(BaseModel):
    path: Path
    mime_type: str
    kind: Literal['document', 'image', 'audio', 'video']
    filename: str | None = None


class OutboundEvent(BaseModel):
    type: Literal['text', 'buttons', 'document']
    text: str | None = None
    buttons: list[dict[str, str]] = Field(default_factory=list)
    file_path: str | None = None
    filename: str | None = None
    caption: str | None = None


class EngineResult(BaseModel):
    events: list[OutboundEvent] = Field(default_factory=list)
    case: dict
