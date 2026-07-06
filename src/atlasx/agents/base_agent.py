"""Shared agent helpers."""

from __future__ import annotations

from pathlib import Path


class BaseAgent:
    """Small base class for named AtlasX agents."""

    agent_name = "base_agent"
    prompt_name: str | None = None

    def prompt_text(self) -> str:
        """Load the reusable Markdown prompt for this agent when available."""

        if not self.prompt_name:
            return self.agent_name
        repo_root = Path(__file__).resolve().parents[3]
        prompt_path = repo_root / "prompts" / "agents" / self.prompt_name
        if not prompt_path.exists():
            return self.agent_name
        return prompt_path.read_text(encoding="utf-8")

