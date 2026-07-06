"""Ontology mapping agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.utils.hashing import stable_id


class OntologyMappingAgent(BaseAgent):
    """Map terms to concepts while preserving uncertainty."""

    agent_name = "ontology_mapping_agent"
    prompt_name = "06_ontology_mapping_agent.md"

    def run(self, atoms_by_paper: dict[str, list[KnowledgeAtom]]) -> list[dict[str, object]]:
        concepts: dict[str, dict[str, object]] = {}
        for atoms in atoms_by_paper.values():
            for atom in atoms:
                terms = [atom.entity, atom.mechanism, atom.outcome, *atom.connection_candidates]
                for term in terms:
                    normalized = term.strip().lower()
                    if normalized in {"unknown", "not reported", ""}:
                        continue
                    concept_id = stable_id("concept", normalized)
                    concepts.setdefault(
                        concept_id,
                        {
                            "concept_id": concept_id,
                            "canonical_concept": term,
                            "synonyms": [term],
                            "related_terms": [],
                            "broader": "unknown",
                            "narrower": "unknown",
                            "uncertainty": "related terms are not collapsed without human review",
                            "source_trace": atom.source_trace,
                            "confidence": min(atom.confidence, 0.6),
                        },
                    )
        return list(concepts.values())

