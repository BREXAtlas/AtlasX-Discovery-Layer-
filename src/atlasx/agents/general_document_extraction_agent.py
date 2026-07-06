"""General document extraction agent for notebook mode."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.source import SourceDocument
from atlasx.models.source_atom import SourceAtom
from atlasx.models.source_route import SourceRouteDecision
from atlasx.providers.base import BaseProvider
from atlasx.utils.hashing import stable_id


class GeneralDocumentExtractionAgent(BaseAgent):
    """Extract flexible source atoms from non-research sources."""

    agent_name = "general_document_extraction_agent"
    prompt_name = "general_document_extraction_agent.md"

    def run(
        self,
        documents: list[SourceDocument],
        route_decisions: list[SourceRouteDecision],
        provider: BaseProvider,
    ) -> dict[str, list[SourceAtom]]:
        route_by_source = {decision.source_id: decision for decision in route_decisions}
        results: dict[str, list[SourceAtom]] = {}
        for document in documents:
            decision = route_by_source.get(document.source_id)
            route = decision.route if decision else "general"
            raw = provider.generate_json(
                schema_name="source_atoms",
                system_prompt=self.prompt_text(),
                user_payload={
                    "source": document.metadata.model_dump(mode="json"),
                    "route": route,
                    "chunks": [chunk.model_dump(mode="json") for chunk in document.chunks],
                },
            )
            items = raw.get("source_atoms") or raw.get("atoms") or []
            if not isinstance(items, list):
                raise ValueError("Provider returned `source_atoms` that was not a list.")
            atoms: list[SourceAtom] = []
            for index, item in enumerate(items, start=1):
                if not isinstance(item, dict):
                    raise ValueError("Each source atom must be a JSON object.")
                item.setdefault("source_id", document.source_id)
                item.setdefault("route", route)
                item.setdefault("source_type", document.metadata.source_type)
                item.setdefault(
                    "source_trace",
                    document.chunks[0].source_trace if document.chunks else "user-provided text chunk",
                )
                item.setdefault("atom_id", stable_id("source_atom", document.source_id, index, item))
                atoms.append(SourceAtom.model_validate(item))
            results[document.source_id] = atoms
        return results

