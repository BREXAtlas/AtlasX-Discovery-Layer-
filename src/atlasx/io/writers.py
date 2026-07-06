"""Output writers."""

from __future__ import annotations

import json
from pathlib import Path

from atlasx.models.agent_run import AgentRunRecord
from atlasx.models.graph import GraphEdge, GraphNode
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.stemd import STEMdAnalysis
from atlasx.utils.json_tools import write_json


def ensure_output_dirs(outputs_dir: Path) -> dict[str, Path]:
    """Create and return standard output directories."""

    paths = {
        "extractions": outputs_dir / "extractions",
        "stemd": outputs_dir / "stemd",
        "graph": outputs_dir / "graph",
        "reports": outputs_dir / "reports",
        "audit": outputs_dir / "audit",
        "notebook": outputs_dir / "notebook",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def write_extraction(paths: dict[str, Path], paper_id: str, atoms: list[KnowledgeAtom]) -> None:
    write_json(paths["extractions"] / f"{paper_id}.json", atoms)


def write_stemd(paths: dict[str, Path], paper_id: str, analyses: list[STEMdAnalysis]) -> None:
    write_json(paths["stemd"] / f"{paper_id}_stemd.json", analyses)


def append_agent_run(paths: dict[str, Path], record: AgentRunRecord) -> None:
    audit_path = paths["audit"] / "agent_runs.jsonl"
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.model_dump(mode="json"), sort_keys=True) + "\n")


def write_graph_csv(paths: dict[str, Path], nodes: list[GraphNode], edges: list[GraphEdge]) -> None:
    import pandas as pd

    node_rows = [node.model_dump(mode="json") for node in nodes]
    edge_rows = [edge.model_dump(mode="json") for edge in edges]
    pd.DataFrame(node_rows).to_csv(paths["graph"] / "nodes.csv", index=False)
    pd.DataFrame(edge_rows).to_csv(paths["graph"] / "edges.csv", index=False)


def write_report(paths: dict[str, Path], name: str, content: str) -> None:
    (paths["reports"] / name).write_text(content, encoding="utf-8")
