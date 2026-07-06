"""Audit model for agent executions."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class AgentRunRecord(BaseModel):
    """JSONL audit row for one agent invocation."""

    agent_name: str
    paper_id: str | None = None
    status: str = "ok"
    provider: str = "offline"
    model: str | None = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    input_summary: str = ""
    output_summary: str = ""
    warnings: list[str] = Field(default_factory=list)

