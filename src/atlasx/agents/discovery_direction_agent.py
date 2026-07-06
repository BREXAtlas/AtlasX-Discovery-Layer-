"""Discovery direction agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.utils.hashing import stable_id


class DiscoveryDirectionAgent(BaseAgent):
    """Generate responsible next-step research possibilities."""

    agent_name = "discovery_direction_agent"
    prompt_name = "10_discovery_direction_agent.md"

    def run(self, atoms_by_paper: dict[str, list[KnowledgeAtom]]) -> list[dict[str, object]]:
        directions: list[dict[str, object]] = []
        for paper_id, atoms in atoms_by_paper.items():
            for atom in atoms:
                directions.append(
                    {
                        "direction_id": stable_id("direction", paper_id, atom.atom_id, atom.next_step),
                        "paper_id": paper_id,
                        "atom_id": atom.atom_id,
                        "candidate_review_topic": atom.discovery_question,
                        "candidate_special_issue_topic": f"Mechanism-level studies of {atom.mechanism}",
                        "call_for_papers_angle": f"Replicable evidence on {atom.entity} under {atom.condition}",
                        "replication_study": atom.next_step,
                        "dataset_needed": "source-linked extraction table with conditions, variables, and outcomes",
                        "do_not_overclaim": "This is a planning artifact, not a final scientific conclusion.",
                        "source_trace": atom.source_trace,
                        "confidence": min(atom.confidence, 0.55),
                        "human_review_required": True,
                    }
                )
        return directions

