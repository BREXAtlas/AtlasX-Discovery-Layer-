"""Gap and contradiction agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.utils.hashing import stable_id


class GapContradictionAgent(BaseAgent):
    """Identify underreported variables, contradictions, and weak evidence areas."""

    agent_name = "gap_contradiction_agent"
    prompt_name = "09_gap_contradiction_agent.md"

    def run(self, atoms_by_paper: dict[str, list[KnowledgeAtom]]) -> list[dict[str, object]]:
        gaps: list[dict[str, object]] = []
        for paper_id, atoms in atoms_by_paper.items():
            for atom in atoms:
                flags: list[str] = []
                if "not reported" in atom.condition.lower():
                    flags.append("condition not reported")
                if "not reported" in atom.boundary_conditions.lower():
                    flags.append("boundary conditions not reported")
                if atom.evidence_type in {"unknown", "user-provided text"}:
                    flags.append("evidence type needs verification")
                if atom.gap and atom.gap != "unknown":
                    flags.append(atom.gap)
                gaps.append(
                    {
                        "gap_id": stable_id("gap", paper_id, atom.atom_id, atom.gap),
                        "paper_id": paper_id,
                        "atom_id": atom.atom_id,
                        "gap": atom.gap,
                        "flags": flags or ["no explicit gap extracted; review source"],
                        "contradiction": "not detected in this project run",
                        "source_trace": atom.source_trace,
                        "confidence": min(atom.confidence, 0.55),
                        "human_review_required": True,
                    }
                )
        return gaps

