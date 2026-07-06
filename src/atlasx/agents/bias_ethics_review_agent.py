"""Bias and ethics review agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.knowledge_atom import KnowledgeAtom


class BiasEthicsReviewAgent(BaseAgent):
    """Review outputs for bias, overclaiming, and provenance gaps."""

    agent_name = "bias_ethics_review_agent"
    prompt_name = "12_bias_ethics_review_agent.md"

    def run(self, atoms_by_paper: dict[str, list[KnowledgeAtom]]) -> list[dict[str, object]]:
        checks: list[dict[str, object]] = []
        for paper_id, atoms in atoms_by_paper.items():
            missing_traces = [atom.atom_id for atom in atoms if not atom.source_trace]
            low_confidence = [atom.atom_id for atom in atoms if atom.confidence < 0.6]
            checks.append(
                {
                    "paper_id": paper_id,
                    "confirmation_bias": "review whether project purpose shaped extraction emphasis",
                    "field_selection_bias": "review whether source set excludes relevant minority or emerging work",
                    "citation_bias": "do not overvalue prestige or citation count without evidence review",
                    "paywall_access_bias": "note sources unavailable to users without institutional access",
                    "overclaiming": "all discovery directions require expert validation",
                    "missing_source_traces": missing_traces,
                    "low_confidence_atoms": low_confidence,
                    "human_review_required": True,
                }
            )
        return checks

