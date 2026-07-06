"""Executive summary generation."""

from __future__ import annotations

from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.paper import PaperDocument


def generate_executive_summary(
    *,
    documents: list[PaperDocument],
    atoms_by_paper: dict[str, list[KnowledgeAtom]],
    connections: list[dict[str, object]],
    gaps: list[dict[str, object]],
    directions: list[dict[str, object]],
) -> str:
    """Create a compact Markdown summary."""

    atom_count = sum(len(atoms) for atoms in atoms_by_paper.values())
    lines = [
        "# AtlasX Executive Summary",
        "",
        "> Experimental research-support artifact. Human review required.",
        "",
        f"- Sources processed: {len(documents)}",
        f"- Knowledge atoms extracted: {atom_count}",
        f"- Cross-paper connections: {len(connections)}",
        f"- Gap records: {len(gaps)}",
        f"- Discovery direction records: {len(directions)}",
        "",
        "## Highest-Signal Themes",
        "",
    ]
    mechanisms = sorted(
        {
            atom.mechanism
            for atoms in atoms_by_paper.values()
            for atom in atoms
            if atom.mechanism not in {"unknown", "not reported"}
        }
    )
    if mechanisms:
        for mechanism in mechanisms[:6]:
            lines.append(f"- {mechanism}")
    else:
        lines.append("- No mechanism terms were confidently extracted.")

    lines.extend(["", "## Responsible Next Use", ""])
    lines.append(
        "Use the JSON and CSV outputs to support review planning, calls for papers, "
        "special issue scoping, replication planning, and source-traceable synthesis. "
        "Do not treat generated directions as final conclusions."
    )
    return "\n".join(lines) + "\n"

