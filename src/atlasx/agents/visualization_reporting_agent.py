"""Visualization and reporting agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.graph import GraphEdge, GraphNode


class VisualizationReportingAgent(BaseAgent):
    """Summarize generated JSON, CSV, and Markdown outputs."""

    agent_name = "visualization_reporting_agent"
    prompt_name = "11_visualization_reporting_agent.md"

    def run(self, nodes: list[GraphNode], edges: list[GraphEdge]) -> dict[str, object]:
        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "outputs": [
                "JSON extractions",
                "STEMd JSON",
                "CSV graph nodes",
                "CSV graph edges",
                "Markdown discovery report",
                "Markdown executive summary",
            ],
            "human_review_required": True,
        }

