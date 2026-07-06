"""STEMd analysis models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class STEMdDimension(BaseModel):
    """One STEMd dimension with rationale and traceability."""

    value: str = "unknown"
    rationale: str = "unknown"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    source_trace: str = "unknown"


class STEMdAnalysis(BaseModel):
    """Specificity, Translatability, Evidence, Mechanism, Discovery direction."""

    paper_id: str
    atom_id: str
    specificity: STEMdDimension
    translatability: STEMdDimension
    evidence: STEMdDimension
    mechanism_systems: STEMdDimension
    discovery_direction: STEMdDimension
    human_review_required: bool = True

