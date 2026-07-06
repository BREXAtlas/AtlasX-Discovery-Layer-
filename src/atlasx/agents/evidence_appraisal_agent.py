"""Evidence appraisal agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.evidence import EvidenceAppraisal
from atlasx.models.knowledge_atom import KnowledgeAtom


class EvidenceAppraisalAgent(BaseAgent):
    """Assess evidence type, limitations, and overclaiming risk."""

    agent_name = "evidence_appraisal_agent"
    prompt_name = "07_evidence_appraisal_agent.md"

    def run(self, atoms_by_paper: dict[str, list[KnowledgeAtom]]) -> list[EvidenceAppraisal]:
        appraisals: list[EvidenceAppraisal] = []
        for paper_id, atoms in atoms_by_paper.items():
            for atom in atoms:
                limitations = ["human review required"]
                if atom.evidence_type in {"unknown", "user-provided text"}:
                    limitations.append("evidence type is not fully specified")
                if "not reported" in atom.condition.lower():
                    limitations.append("conditions are not reported")
                appraisals.append(
                    EvidenceAppraisal(
                        paper_id=paper_id,
                        atom_id=atom.atom_id,
                        evidence_type=atom.evidence_type,
                        sample_size="not reported",
                        replication_status="not reported",
                        measurement_quality="unknown",
                        limitations=limitations,
                        risk_of_overclaiming="high if used without source verification",
                        confidence=min(atom.confidence, 0.6),
                        source_trace=atom.source_trace,
                    )
                )
        return appraisals

