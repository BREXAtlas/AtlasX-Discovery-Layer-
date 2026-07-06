"""Intake agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.paper import PaperDocument, PaperMetadata


class IntakeAgent(BaseAgent):
    """Identify source files and normalize metadata."""

    agent_name = "intake_agent"
    prompt_name = "01_intake_agent.md"

    def run(self, documents: list[PaperDocument]) -> list[PaperMetadata]:
        return [document.metadata for document in documents]

