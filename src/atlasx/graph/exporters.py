"""Graph export helpers."""

from __future__ import annotations

from pathlib import Path

from atlasx.models.graph import GraphEdge, GraphNode


def export_graph_csv(nodes: list[GraphNode], edges: list[GraphEdge], graph_dir: Path) -> None:
    """Write graph nodes and edges as CSV files."""

    import pandas as pd

    graph_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([node.model_dump(mode="json") for node in nodes]).to_csv(
        graph_dir / "nodes.csv",
        index=False,
    )
    pd.DataFrame([edge.model_dump(mode="json") for edge in edges]).to_csv(
        graph_dir / "edges.csv",
        index=False,
    )

