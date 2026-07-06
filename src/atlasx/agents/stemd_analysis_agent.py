"""STEMd analysis agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.stemd import STEMdAnalysis, STEMdDimension


class STEMdAnalysisAgent(BaseAgent):
    """Apply Specificity, Translatability, Evidence, Mechanism, Discovery direction."""

    agent_name = "stemd_analysis_agent"
    prompt_name = "05_stemd_analysis_agent.md"

    def run(self, atoms_by_paper: dict[str, list[KnowledgeAtom]]) -> dict[str, list[STEMdAnalysis]]:
        output: dict[str, list[STEMdAnalysis]] = {}
        for paper_id, atoms in atoms_by_paper.items():
            analyses: list[STEMdAnalysis] = []
            for atom in atoms:
                analyses.append(
                    STEMdAnalysis(
                        paper_id=paper_id,
                        atom_id=atom.atom_id,
                        specificity=STEMdDimension(
                            value=f"{atom.entity}; {atom.input_signal_or_intervention}; {atom.condition}",
                            rationale="Specificity is taken from the entity, input, and condition fields.",
                            confidence=atom.confidence,
                            source_trace=atom.source_trace,
                        ),
                        translatability=STEMdDimension(
                            value=atom.next_step,
                            rationale="The next-step field is used as a translational planning signal.",
                            confidence=min(atom.confidence, 0.6),
                            source_trace=atom.source_trace,
                        ),
                        evidence=STEMdDimension(
                            value=f"{atom.evidence_type}; {atom.evidence_strength}",
                            rationale="Evidence type and strength are preserved without upgrading certainty.",
                            confidence=atom.confidence,
                            source_trace=atom.source_trace,
                        ),
                        mechanism_systems=STEMdDimension(
                            value=atom.mechanism,
                            rationale="Mechanism/system language is extracted from the atom.",
                            confidence=atom.confidence,
                            source_trace=atom.source_trace,
                        ),
                        discovery_direction=STEMdDimension(
                            value=atom.discovery_question,
                            rationale="Discovery direction is framed as a question requiring review.",
                            confidence=min(atom.confidence, 0.6),
                            source_trace=atom.source_trace,
                        ),
                    )
                )
            output[paper_id] = analyses
        return output

