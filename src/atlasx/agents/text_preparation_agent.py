"""Text preparation agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.paper import PaperDocument, PaperTextChunk


class TextPreparationAgent(BaseAgent):
    """Return clean, traceable chunks prepared by the loader."""

    agent_name = "text_preparation_agent"
    prompt_name = "03_text_preparation_agent.md"

    def run(self, documents: list[PaperDocument]) -> dict[str, list[PaperTextChunk]]:
        return {document.paper_id: document.chunks for document in documents}

