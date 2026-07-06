"""Connection reasoning agent."""

from __future__ import annotations

from itertools import combinations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.utils.hashing import stable_id


class ConnectionReasoningAgent(BaseAgent):
    """Connect papers through mechanisms, variables, conditions, and gaps."""

    agent_name = "connection_reasoning_agent"
    prompt_name = "08_connection_reasoning_agent.md"

    def run(self, atoms_by_paper: dict[str, list[KnowledgeAtom]]) -> list[dict[str, object]]:
        connections: list[dict[str, object]] = []
        for left_id, right_id in combinations(sorted(atoms_by_paper), 2):
            left_terms = _paper_terms(atoms_by_paper[left_id])
            right_terms = _paper_terms(atoms_by_paper[right_id])
            shared = sorted(left_terms & right_terms)
            if not shared:
                continue
            connection_type = _classify_connection(shared)
            connections.append(
                {
                    "connection_id": stable_id("connection", left_id, right_id, ",".join(shared)),
                    "source_paper_id": left_id,
                    "target_paper_id": right_id,
                    "connection_type": connection_type,
                    "shared_terms": shared,
                    "rationale": (
                        "Connection is based on shared mechanisms, variables, outcomes, "
                        "or gaps rather than paper-level keyword similarity."
                    ),
                    "source_trace": "derived from knowledge atom connection candidates",
                    "confidence": 0.58,
                    "human_review_required": True,
                }
            )
        return connections


def _paper_terms(atoms: list[KnowledgeAtom]) -> set[str]:
    terms: set[str] = set()
    for atom in atoms:
        for value in [atom.mechanism, atom.entity, atom.outcome, atom.gap, *atom.connection_candidates]:
            normalized = value.lower().strip()
            if normalized and normalized not in {"unknown", "not reported"}:
                terms.add(normalized)
    return terms


def _classify_connection(shared: list[str]) -> str:
    joined = " ".join(shared)
    if "mechanism" in joined or "calcium" in joined or "membrane" in joined:
        return "shared mechanism"
    if "proliferation" in joined or "migration" in joined:
        return "shared outcome"
    if "replication" in joined or "gap" in joined:
        return "shared gap"
    return "mechanism-level relatedness"

