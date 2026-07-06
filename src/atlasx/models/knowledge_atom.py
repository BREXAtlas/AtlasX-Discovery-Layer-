"""First-principles knowledge atom model."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


def _unknown(value: object) -> str:
    if value is None:
        return "unknown"
    text = str(value).strip()
    return text if text else "unknown"


class KnowledgeAtom(BaseModel):
    """A fundamental claim, question, mechanism, variable, or evidence unit."""

    atom_id: str
    paper_id: str
    source_trace: str
    atom_type: str = "claim"
    paper_question: str = "unknown"
    field_question: str = "unknown"
    discovery_question: str = "unknown"
    entity: str = "unknown"
    input_signal_or_intervention: str = "not reported"
    condition: str = "not reported"
    mechanism: str = "unknown"
    outcome: str = "unknown"
    evidence_statement: str = "unknown"
    evidence_type: str = "unknown"
    evidence_strength: str = "unknown"
    boundary_conditions: str = "not reported"
    assumptions: str = "unknown"
    gap: str = "unknown"
    connection_candidates: list[str] = Field(default_factory=list)
    next_step: str = "unknown"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    human_review_required: bool = True

    @field_validator(
        "atom_id",
        "paper_id",
        "source_trace",
        "atom_type",
        "paper_question",
        "field_question",
        "discovery_question",
        "entity",
        "input_signal_or_intervention",
        "condition",
        "mechanism",
        "outcome",
        "evidence_statement",
        "evidence_type",
        "evidence_strength",
        "boundary_conditions",
        "assumptions",
        "gap",
        "next_step",
        mode="before",
    )
    @classmethod
    def preserve_unknowns(cls, value: object) -> str:
        return _unknown(value)

