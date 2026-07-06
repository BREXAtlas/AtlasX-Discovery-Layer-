"""AtlasX pipeline orchestration."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from atlasx.agents import (
    BiasEthicsReviewAgent,
    ConnectionReasoningAgent,
    DiscoveryDirectionAgent,
    EvidenceAppraisalAgent,
    FirstPrinciplesExtractionAgent,
    GapContradictionAgent,
    GeneralDocumentExtractionAgent,
    IntakeAgent,
    OntologyMappingAgent,
    SourceIntegrityAgent,
    STEMdAnalysisAgent,
    TextPreparationAgent,
    VisualizationReportingAgent,
)
from atlasx.config import ProjectConfig, load_project_config
from atlasx import __version__
from atlasx.graph.builder import build_graph
from atlasx.io.loaders import load_project_documents, load_project_source_documents
from atlasx.io.writers import (
    append_agent_run,
    ensure_output_dirs,
    write_extraction,
    write_graph_csv,
    write_report,
    write_stemd,
)
from atlasx.models.agent_run import AgentRunRecord
from atlasx.models.evidence import EvidenceAppraisal
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.source import SourceDocument
from atlasx.models.source_atom import SourceAtom
from atlasx.models.source_route import SourceRouteDecision
from atlasx.models.stemd import STEMdAnalysis
from atlasx.providers import get_provider
from atlasx.routing import classify_sources
from atlasx.reports.executive_summary import generate_executive_summary
from atlasx.reports.markdown_report import generate_discovery_report
from atlasx.utils.json_tools import read_json, write_json


def run_pipeline(
    project: Path,
    provider_name: str = "offline",
    model: str | None = None,
    route: str = "research",
) -> dict[str, object]:
    """Run the full AtlasX Discovery Layer pipeline."""

    config = load_project_config(project)
    output_paths = ensure_output_dirs(config.outputs_dir)
    audit_path = output_paths["audit"] / "agent_runs.jsonl"
    if audit_path.exists():
        audit_path.unlink()

    provider = get_provider(provider_name, model=model)
    source_documents = load_project_source_documents(config)
    route_decisions = _decide_routes(source_documents, route)

    if route.lower().strip() != "research" and not _all_research(route_decisions):
        return _run_notebook_pipeline(
            config=config,
            output_paths=output_paths,
            provider=provider,
            source_documents=source_documents,
            route_decisions=route_decisions,
            route=route,
        )

    documents = load_project_documents(config)

    intake_agent = IntakeAgent()
    metadata = intake_agent.run(documents)
    _audit(output_paths, intake_agent.agent_name, provider, f"{len(metadata)} sources")

    integrity_agent = SourceIntegrityAgent()
    integrity = integrity_agent.run(metadata)
    _audit(output_paths, integrity_agent.agent_name, provider, f"{len(integrity)} integrity records")

    text_agent = TextPreparationAgent()
    chunks_by_paper = text_agent.run(documents)
    _audit(output_paths, text_agent.agent_name, provider, f"{sum(len(v) for v in chunks_by_paper.values())} chunks")

    extraction_agent = FirstPrinciplesExtractionAgent()
    atoms_by_paper = extraction_agent.run(documents, provider)
    for paper_id, atoms in atoms_by_paper.items():
        write_extraction(output_paths, paper_id, atoms)
    _audit(output_paths, extraction_agent.agent_name, provider, f"{sum(len(v) for v in atoms_by_paper.values())} atoms")

    stemd_agent = STEMdAnalysisAgent()
    stemd_by_paper = stemd_agent.run(atoms_by_paper)
    for paper_id, analyses in stemd_by_paper.items():
        write_stemd(output_paths, paper_id, analyses)
    _audit(output_paths, stemd_agent.agent_name, provider, "STEMd analyses written")

    ontology_agent = OntologyMappingAgent()
    concepts = ontology_agent.run(atoms_by_paper)
    write_json(config.outputs_dir / "extractions" / "ontology_concepts.json", concepts)
    _audit(output_paths, ontology_agent.agent_name, provider, f"{len(concepts)} concepts")

    evidence_agent = EvidenceAppraisalAgent()
    evidence_appraisals = evidence_agent.run(atoms_by_paper)
    write_json(config.outputs_dir / "extractions" / "evidence_appraisals.json", evidence_appraisals)
    _audit(output_paths, evidence_agent.agent_name, provider, f"{len(evidence_appraisals)} appraisals")

    connection_agent = ConnectionReasoningAgent()
    connections = connection_agent.run(atoms_by_paper)
    write_json(config.outputs_dir / "extractions" / "connections.json", connections)
    _audit(output_paths, connection_agent.agent_name, provider, f"{len(connections)} connections")

    gap_agent = GapContradictionAgent()
    gaps = gap_agent.run(atoms_by_paper)
    write_json(config.outputs_dir / "extractions" / "gaps.json", gaps)
    _audit(output_paths, gap_agent.agent_name, provider, f"{len(gaps)} gaps")

    direction_agent = DiscoveryDirectionAgent()
    directions = direction_agent.run(atoms_by_paper)
    write_json(config.outputs_dir / "extractions" / "discovery_directions.json", directions)
    _audit(output_paths, direction_agent.agent_name, provider, f"{len(directions)} directions")

    nodes, edges = build_graph(
        documents=documents,
        atoms_by_paper=atoms_by_paper,
        concepts=concepts,
        evidence_appraisals=evidence_appraisals,
        connections=connections,
        gaps=gaps,
        directions=directions,
    )
    write_graph_csv(output_paths, nodes, edges)

    visualization_agent = VisualizationReportingAgent()
    visualization = visualization_agent.run(nodes, edges)
    _audit(output_paths, visualization_agent.agent_name, provider, f"{visualization['node_count']} nodes")

    bias_agent = BiasEthicsReviewAgent()
    bias_reviews = bias_agent.run(atoms_by_paper)
    write_json(config.outputs_dir / "extractions" / "bias_ethics_review.json", bias_reviews)
    _audit(output_paths, bias_agent.agent_name, provider, f"{len(bias_reviews)} reviews")

    report = generate_discovery_report(
        documents=documents,
        atoms_by_paper=atoms_by_paper,
        stemd_by_paper=stemd_by_paper,
        evidence_appraisals=evidence_appraisals,
        connections=connections,
        gaps=gaps,
        directions=directions,
        bias_reviews=bias_reviews,
    )
    summary = generate_executive_summary(
        documents=documents,
        atoms_by_paper=atoms_by_paper,
        connections=connections,
        gaps=gaps,
        directions=directions,
    )
    write_report(output_paths, "discovery_report.md", report)
    write_report(output_paths, "executive_summary.md", summary)
    _write_notebook_outputs(
        output_paths=output_paths,
        project_name=config.name,
        provider_name=provider.name,
        source_documents=source_documents,
        route_decisions=route_decisions,
        source_atoms=[],
        route=route,
        summary_markdown=_notebook_summary(
            config.name,
            route,
            route_decisions,
            [],
            "Research Mode used the existing knowledge-atom discovery pipeline.",
        ),
    )

    return {
        "project": str(config.project_dir),
        "outputs": str(config.outputs_dir),
        "route": route,
        "papers": len(documents),
        "atoms": sum(len(items) for items in atoms_by_paper.values()),
        "nodes": len(nodes),
        "edges": len(edges),
    }


def regenerate_graph(project: Path) -> dict[str, object]:
    """Regenerate graph CSV files from existing extraction outputs."""

    config = load_project_config(project)
    output_paths = ensure_output_dirs(config.outputs_dir)
    documents = load_project_documents(config)
    atoms_by_paper = _load_atoms(config.outputs_dir)
    concepts = _read_optional(config.outputs_dir / "extractions" / "ontology_concepts.json", [])
    evidence_appraisals = [
        EvidenceAppraisal.model_validate(item)
        for item in _read_optional(config.outputs_dir / "extractions" / "evidence_appraisals.json", [])
    ]
    connections = _read_optional(config.outputs_dir / "extractions" / "connections.json", [])
    gaps = _read_optional(config.outputs_dir / "extractions" / "gaps.json", [])
    directions = _read_optional(config.outputs_dir / "extractions" / "discovery_directions.json", [])
    nodes, edges = build_graph(
        documents=documents,
        atoms_by_paper=atoms_by_paper,
        concepts=concepts,
        evidence_appraisals=evidence_appraisals,
        connections=connections,
        gaps=gaps,
        directions=directions,
    )
    write_graph_csv(output_paths, nodes, edges)
    return {"nodes": len(nodes), "edges": len(edges), "outputs": str(output_paths["graph"])}


def regenerate_report(project: Path) -> dict[str, object]:
    """Regenerate Markdown reports from existing extraction outputs."""

    config = load_project_config(project)
    output_paths = ensure_output_dirs(config.outputs_dir)
    documents = load_project_documents(config)
    atoms_by_paper = _load_atoms(config.outputs_dir)
    stemd_by_paper = _load_stemd(config.outputs_dir)
    evidence_appraisals = [
        EvidenceAppraisal.model_validate(item)
        for item in _read_optional(config.outputs_dir / "extractions" / "evidence_appraisals.json", [])
    ]
    connections = _read_optional(config.outputs_dir / "extractions" / "connections.json", [])
    gaps = _read_optional(config.outputs_dir / "extractions" / "gaps.json", [])
    directions = _read_optional(config.outputs_dir / "extractions" / "discovery_directions.json", [])
    bias_reviews = _read_optional(config.outputs_dir / "extractions" / "bias_ethics_review.json", [])
    report = generate_discovery_report(
        documents=documents,
        atoms_by_paper=atoms_by_paper,
        stemd_by_paper=stemd_by_paper,
        evidence_appraisals=evidence_appraisals,
        connections=connections,
        gaps=gaps,
        directions=directions,
        bias_reviews=bias_reviews,
    )
    summary = generate_executive_summary(
        documents=documents,
        atoms_by_paper=atoms_by_paper,
        connections=connections,
        gaps=gaps,
        directions=directions,
    )
    write_report(output_paths, "discovery_report.md", report)
    write_report(output_paths, "executive_summary.md", summary)
    return {"reports": str(output_paths["reports"])}


def _audit(output_paths: dict[str, Path], agent_name: str, provider: object, summary: str) -> None:
    now = datetime.now(timezone.utc)
    append_agent_run(
        output_paths,
        AgentRunRecord(
            agent_name=agent_name,
            status="ok",
            provider=getattr(provider, "name", "unknown"),
            model=getattr(provider, "model", None),
            started_at=now,
            completed_at=now,
            output_summary=summary,
        ),
    )


def _load_atoms(outputs_dir: Path) -> dict[str, list[KnowledgeAtom]]:
    extraction_dir = outputs_dir / "extractions"
    atoms_by_paper: dict[str, list[KnowledgeAtom]] = {}
    for path in sorted(extraction_dir.glob("*.json")):
        if path.name in {
            "ontology_concepts.json",
            "evidence_appraisals.json",
            "connections.json",
            "gaps.json",
            "discovery_directions.json",
            "bias_ethics_review.json",
        }:
            continue
        data = read_json(path)
        atoms = [KnowledgeAtom.model_validate(item) for item in data]
        if atoms:
            atoms_by_paper[atoms[0].paper_id] = atoms
    if not atoms_by_paper:
        raise FileNotFoundError("No extraction JSON files found. Run `atlasx run` first.")
    return atoms_by_paper


def _load_stemd(outputs_dir: Path) -> dict[str, list[STEMdAnalysis]]:
    stemd_dir = outputs_dir / "stemd"
    analyses: dict[str, list[STEMdAnalysis]] = {}
    for path in sorted(stemd_dir.glob("*_stemd.json")):
        data = read_json(path)
        items = [STEMdAnalysis.model_validate(item) for item in data]
        if items:
            analyses[items[0].paper_id] = items
    return analyses


def _read_optional(path: Path, default: object) -> object:
    if not path.exists():
        return default
    return read_json(path)


def _decide_routes(
    source_documents: list[SourceDocument],
    route: str,
) -> list[SourceRouteDecision]:
    normalized = route.lower().strip()
    if normalized == "auto":
        return classify_sources(source_documents)
    if normalized == "research":
        decisions = classify_sources(source_documents)
        return [
            decision.model_copy(
                update={
                    "route": "research",
                    "reasons": ["explicit research route", *decision.reasons],
                    "confidence": max(decision.confidence, 0.8),
                }
            )
            for decision in decisions
        ]
    if normalized in {"general", "learning", "strategic_brief", "source_collection", "unknown"}:
        decisions = classify_sources(source_documents)
        return [
            decision.model_copy(
                update={
                    "route": normalized,
                    "reasons": [f"explicit {normalized} route", *decision.reasons],
                    "confidence": max(decision.confidence, 0.75),
                }
            )
            for decision in decisions
        ]
    decisions = classify_sources(source_documents)
    return [
        decision.model_copy(
            update={
                "route": "unknown",
                "warnings": [f"unsupported route {route!r}; used unknown fallback", *decision.warnings],
                "confidence": min(decision.confidence, 0.4),
            }
        )
        for decision in decisions
    ]


def _all_research(route_decisions: list[SourceRouteDecision]) -> bool:
    return bool(route_decisions) and all(decision.route == "research" for decision in route_decisions)


def _run_notebook_pipeline(
    *,
    config: ProjectConfig,
    output_paths: dict[str, Path],
    provider: object,
    source_documents: list[SourceDocument],
    route_decisions: list[SourceRouteDecision],
    route: str,
) -> dict[str, object]:
    general_agent = GeneralDocumentExtractionAgent()
    source_atoms_by_source = general_agent.run(source_documents, route_decisions, provider)
    source_atoms = [
        atom
        for atoms in source_atoms_by_source.values()
        for atom in atoms
    ]
    _audit(
        output_paths,
        general_agent.agent_name,
        provider,
        f"{len(source_atoms)} source atoms",
    )
    summary = _notebook_summary(
        config.name,
        route,
        route_decisions,
        source_atoms,
        "General Notebook Mode used flexible source atoms for app-ready outputs.",
    )
    _write_notebook_outputs(
        output_paths=output_paths,
        project_name=config.name,
        provider_name=provider.name,
        source_documents=source_documents,
        route_decisions=route_decisions,
        source_atoms=source_atoms,
        route=route,
        summary_markdown=summary,
    )
    return {
        "project": str(config.project_dir),
        "outputs": str(config.outputs_dir),
        "route": route,
        "sources": len(source_documents),
        "source_atoms": len(source_atoms),
        "notebook_outputs": str(output_paths["notebook"]),
    }


def _write_notebook_outputs(
    *,
    output_paths: dict[str, Path],
    project_name: str,
    provider_name: str,
    source_documents: list[SourceDocument],
    route_decisions: list[SourceRouteDecision],
    source_atoms: list[SourceAtom],
    route: str,
    summary_markdown: str,
) -> None:
    notebook_dir = output_paths["notebook"]
    write_json(notebook_dir / "source_routes.json", route_decisions)
    write_json(notebook_dir / "source_atoms.json", source_atoms)
    now = datetime.now(timezone.utc).isoformat()
    source_index = {
        "notebook_id": project_name,
        "title": project_name,
        "created_at": now,
        "updated_at": now,
        "sources": [document.metadata.model_dump(mode="json") for document in source_documents],
        "routes": [decision.model_dump(mode="json") for decision in route_decisions],
        "outputs": {
            "source_routes": "outputs/notebook/source_routes.json",
            "source_atoms": "outputs/notebook/source_atoms.json",
            "notebook_summary": "outputs/notebook/notebook_summary.md",
            "discovery_report": "outputs/reports/discovery_report.md",
            "executive_summary": "outputs/reports/executive_summary.md",
            "graph_nodes": "outputs/graph/nodes.csv",
            "graph_edges": "outputs/graph/edges.csv",
            "audit": "outputs/audit/agent_runs.jsonl",
        },
        "app_version": "future",
        "atlasx_version": __version__,
        "local_only": provider_name == "offline",
        "provider": provider_name,
        "requested_route": route,
        "human_review_required": True,
    }
    write_json(notebook_dir / "source_index.json", source_index)
    (notebook_dir / "notebook_summary.md").write_text(summary_markdown, encoding="utf-8")


def _notebook_summary(
    project_name: str,
    route: str,
    route_decisions: list[SourceRouteDecision],
    source_atoms: list[SourceAtom],
    note: str,
) -> str:
    lines = [
        f"# {project_name} Notebook Summary",
        "",
        "> Human review required. AtlasX outputs are research-support and learning-support artifacts.",
        "",
        f"- Requested route: `{route}`",
        f"- Sources routed: {len(route_decisions)}",
        f"- Source atoms: {len(source_atoms)}",
        f"- Note: {note}",
        "",
        "## Routes",
        "",
    ]
    for decision in route_decisions:
        lines.append(
            f"- `{decision.source_id}`: {decision.route} / {decision.source_kind} "
            f"(confidence {decision.confidence:.2f})"
        )
    if source_atoms:
        lines.extend(["", "## Source Atoms", ""])
        for atom in source_atoms:
            lines.append(f"- `{atom.atom_id}`: {atom.main_topic} - {atom.summary}")
    lines.append("")
    return "\n".join(lines)
