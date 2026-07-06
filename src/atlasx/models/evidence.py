"""Evidence models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvidenceUnit(BaseModel):
    """A traceable statement of evidence."""

    evidence_id: str
    paper_id: str
    atom_id: str
    source_trace: str
    statement: str = "unknown"
    evidence_type: str = "unknown"
    strength: str = "unknown"
    limitations: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    human_review_required: bool = True


class EvidenceAppraisal(BaseModel):
    """Evidence quality and overclaiming risk."""

    paper_id: str
    atom_id: str
    evidence_type: str = "unknown"
    sample_size: str = "not reported"
    replication_status: str = "not reported"
    measurement_quality: str = "unknown"
    limitations: list[str] = Field(default_factory=list)
    risk_of_overclaiming: str = "requires human review"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    source_trace: str = "unknown"

