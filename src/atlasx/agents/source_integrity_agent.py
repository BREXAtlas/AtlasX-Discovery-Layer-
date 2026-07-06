"""Source integrity agent."""

from __future__ import annotations

from collections import Counter

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.paper import PaperMetadata


class SourceIntegrityAgent(BaseAgent):
    """Check citation completeness, duplicates, and source-use warnings."""

    agent_name = "source_integrity_agent"
    prompt_name = "02_source_integrity_agent.md"

    def run(self, metadata: list[PaperMetadata]) -> list[dict[str, object]]:
        titles = Counter(item.title.lower() for item in metadata if item.title != "unknown")
        dois = Counter(item.doi.lower() for item in metadata if item.doi)
        results: list[dict[str, object]] = []
        for item in metadata:
            warnings: list[str] = []
            if item.title == "unknown":
                warnings.append("missing title")
            if not item.authors:
                warnings.append("missing authors")
            if item.year is None:
                warnings.append("missing year")
            if not item.doi:
                warnings.append("missing DOI")
            if item.title != "unknown" and titles[item.title.lower()] > 1:
                warnings.append("possible duplicate title")
            if item.doi and dois[item.doi.lower()] > 1:
                warnings.append("possible duplicate DOI")
            if item.file.lower().endswith(".pdf"):
                warnings.append("do not commit copyrighted PDFs to public repositories")
            if "licensed" in item.license_status.lower() or "paywall" in item.license_status.lower():
                warnings.append("verify license terms before processing or sharing outputs")
            results.append(
                {
                    "paper_id": item.paper_id,
                    "status": "review" if warnings else "ok",
                    "warnings": warnings,
                    "source_traceability": "metadata and local file path recorded",
                    "human_review_required": True,
                }
            )
        return results

