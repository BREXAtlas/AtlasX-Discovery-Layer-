"""Knowledge graph models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    """Graph node export row."""

    node_id: str
    node_type: str
    label: str
    paper_id: str | None = None
    source_trace: str = "unknown"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    properties: dict[str, str] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """Graph edge export row."""

    edge_id: str
    source_id: str
    target_id: str
    edge_type: str
    label: str
    paper_id: str | None = None
    source_trace: str = "unknown"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: str = "unknown"

