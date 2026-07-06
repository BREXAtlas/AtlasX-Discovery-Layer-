"""Discovery report generation."""

from __future__ import annotations

from atlasx.models.evidence import EvidenceAppraisal
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.paper import PaperDocument
from atlasx.models.stemd import STEMdAnalysis


def generate_discovery_report(
    *,
    documents: list[PaperDocument],
    atoms_by_paper: dict[str, list[KnowledgeAtom]],
    stemd_by_paper: dict[str, list[STEMdAnalysis]],
    evidence_appraisals: list[EvidenceAppraisal],
    connections: list[dict[str, object]],
    gaps: list[dict[str, object]],
    directions: list[dict[str, object]],
    bias_reviews: list[dict[str, object]],
) -> str:
    """Create a source-traceable Markdown discovery report."""

    lines = [
        "# AtlasX Discovery Report",
        "",
        "> Human review required. This report is a research-support artifact, not a final scientific conclusion.",
        "",
        "## Source Set",
        "",
    ]
    for document in documents:
        meta = document.metadata
        authors = ", ".join(meta.authors) if meta.authors else "not reported"
        lines.append(f"- **{meta.paper_id}**: {meta.title} ({meta.year or 'not reported'}), {authors}. DOI: {meta.doi or 'not reported'}.")
    lines.extend(["", "## Knowledge Atoms", ""])
    for paper_id, atoms in atoms_by_paper.items():
        lines.append(f"### {paper_id}")
        for atom in atoms:
            lines.extend(
                [
                    f"- **{atom.atom_type}** `{atom.atom_id}`",
                    f"  - Question: {atom.paper_question}",
                    f"  - Entity/Input/Condition: {atom.entity}; {atom.input_signal_or_intervention}; {atom.condition}",
                    f"  - Mechanism/Outcome: {atom.mechanism}; {atom.outcome}",
                    f"  - Evidence: {atom.evidence_statement}",
                    f"  - Gap: {atom.gap}",
                    f"  - Source trace: {atom.source_trace}",
                    f"  - Confidence: {atom.confidence:.2f}; human review required: {atom.human_review_required}",
                ]
            )
        lines.append("")

    lines.extend(["## STEMd Summary", ""])
    for paper_id, analyses in stemd_by_paper.items():
        lines.append(f"### {paper_id}")
        for item in analyses:
            lines.extend(
                [
                    f"- Atom `{item.atom_id}`",
                    f"  - Specificity: {item.specificity.value}",
                    f"  - Translatability: {item.translatability.value}",
                    f"  - Evidence: {item.evidence.value}",
                    f"  - Mechanism/Systems: {item.mechanism_systems.value}",
                    f"  - Discovery Direction: {item.discovery_direction.value}",
                ]
            )
        lines.append("")

    lines.extend(["## Evidence Appraisal", ""])
    for appraisal in evidence_appraisals:
        lines.append(
            f"- `{appraisal.atom_id}`: {appraisal.evidence_type}; limitations: "
            f"{'; '.join(appraisal.limitations)}; overclaiming risk: {appraisal.risk_of_overclaiming}."
        )

    lines.extend(["", "## Connections", ""])
    if connections:
        for connection in connections:
            lines.append(
                f"- {connection['source_paper_id']} -> {connection['target_paper_id']}: "
                f"{connection['connection_type']} via {', '.join(connection['shared_terms'])}."
            )
    else:
        lines.append("- No cross-paper connections met the current deterministic threshold.")

    lines.extend(["", "## Gap Table", ""])
    for gap in gaps:
        lines.append(f"- `{gap['atom_id']}`: {gap['gap']} Flags: {', '.join(gap['flags'])}.")

    lines.extend(["", "## Discovery Directions", ""])
    for direction in directions:
        lines.append(
            f"- {direction['candidate_review_topic']} "
            f"Replication angle: {direction['replication_study']} "
            f"Caution: {direction['do_not_overclaim']}"
        )

    lines.extend(["", "## Bias and Ethics Review", ""])
    for review in bias_reviews:
        lines.append(
            f"- {review['paper_id']}: {review['overclaiming']} "
            f"Source trace gaps: {review['missing_source_traces']}."
        )

    lines.extend(
        [
            "",
            "## Provenance and Use",
            "",
            "Every extraction should be checked against the source text, DOI, or citation record. "
            "Do not use this report to replace the original article, misrepresent authors, or make automated decisions.",
            "",
        ]
    )
    return "\n".join(lines)

