"""First-principles extraction agent."""

from __future__ import annotations

from atlasx.agents.base_agent import BaseAgent
from atlasx.models.knowledge_atom import KnowledgeAtom
from atlasx.models.paper import PaperDocument
from atlasx.providers.base import BaseProvider
from atlasx.utils.hashing import stable_id


class FirstPrinciplesExtractionAgent(BaseAgent):
    """Break each paper into traceable knowledge atoms."""

    agent_name = "first_principles_extraction_agent"
    prompt_name = "04_first_principles_extraction_agent.md"

    def run(
        self,
        documents: list[PaperDocument],
        provider: BaseProvider,
    ) -> dict[str, list[KnowledgeAtom]]:
        results: dict[str, list[KnowledgeAtom]] = {}
        for document in documents:
            raw = provider.generate_json(
                schema_name="knowledge_atoms",
                system_prompt=self.prompt_text(),
                user_payload={
                    "paper": document.metadata.model_dump(mode="json"),
                    "chunks": [chunk.model_dump(mode="json") for chunk in document.chunks],
                },
            )
            items = raw.get("knowledge_atoms") or raw.get("atoms") or []
            if not isinstance(items, list):
                raise ValueError("Provider returned `knowledge_atoms` that was not a list.")
            atoms: list[KnowledgeAtom] = []
            for index, item in enumerate(items, start=1):
                if not isinstance(item, dict):
                    raise ValueError("Each knowledge atom must be a JSON object.")
                item.setdefault("paper_id", document.paper_id)
                item.setdefault(
                    "source_trace",
                    document.chunks[0].source_trace if document.chunks else "user-provided text chunk",
                )
                item.setdefault("atom_id", stable_id("atom", document.paper_id, index, item))
                atoms.append(KnowledgeAtom.model_validate(item))
            results[document.paper_id] = atoms
        return results

