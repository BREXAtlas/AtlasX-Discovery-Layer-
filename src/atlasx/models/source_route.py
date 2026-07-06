"""Source routing decisions for notebook-style projects."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

ROUTES = {
    "research",
    "general",
    "learning",
    "strategic_brief",
    "source_collection",
    "unknown",
}


class SourceRouteDecision(BaseModel):
    """Deterministic route classification for one source."""

    source_id: str
    route: str
    source_kind: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    human_review_required: bool = True

    @field_validator("source_id", "source_kind", mode="before")
    @classmethod
    def require_unknown_text(cls, value: object) -> str:
        if value is None or str(value).strip() == "":
            return "unknown"
        return str(value).strip()

    @field_validator("route", mode="before")
    @classmethod
    def normalize_route(cls, value: object) -> str:
        text = "unknown" if value is None else str(value).strip().lower()
        return text if text in ROUTES else "unknown"

