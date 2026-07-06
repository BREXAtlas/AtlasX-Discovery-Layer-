"""Flexible source atom model for general notebook mode."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


def _unknown(value: object) -> str:
    if value is None:
        return "unknown"
    text = str(value).strip()
    return text if text else "unknown"


class SourceAtom(BaseModel):
    """A source-grounded unit extracted from a general document."""

    atom_id: str
    source_id: str
    source_trace: str
    route: str = "general"
    source_type: str = "unknown"
    atom_type: str = "claim"
    main_topic: str = "unknown"
    question_answered: str = "unknown"
    core_claim: str = "unknown"
    supporting_points: list[str] = Field(default_factory=list)
    evidence_or_examples: list[str] = Field(default_factory=list)
    key_terms: list[str] = Field(default_factory=list)
    named_entities: list[str] = Field(default_factory=list)
    timeline_or_sequence: list[str] = Field(default_factory=list)
    method_or_process: str = "not applicable"
    assumptions: str = "unknown"
    limitations: str = "unknown"
    contradictions: list[str] = Field(default_factory=list)
    connections: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list)
    study_notes: list[str] = Field(default_factory=list)
    user_takeaway: str = "unknown"
    summary: str = "unknown"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    human_review_required: bool = True

    @field_validator(
        "atom_id",
        "source_id",
        "source_trace",
        "route",
        "source_type",
        "atom_type",
        "main_topic",
        "question_answered",
        "core_claim",
        "method_or_process",
        "assumptions",
        "limitations",
        "user_takeaway",
        "summary",
        mode="before",
    )
    @classmethod
    def preserve_unknowns(cls, value: object) -> str:
        return _unknown(value)

