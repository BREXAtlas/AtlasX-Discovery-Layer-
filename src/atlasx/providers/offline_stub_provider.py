"""Deterministic offline provider for demos and tests."""

from __future__ import annotations

import re
from typing import Any

from atlasx.providers.base import BaseProvider
from atlasx.utils.hashing import stable_id


class OfflineStubProvider(BaseProvider):
    """Return deterministic sample JSON without network or API keys."""

    name = "offline"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or "offline-stub"

    def generate_json(
        self,
        *,
        schema_name: str,
        system_prompt: str,
        user_payload: dict[str, Any],
    ) -> dict[str, Any]:
        if schema_name == "knowledge_atoms":
            return {"knowledge_atoms": self._knowledge_atoms(user_payload)}
        if schema_name == "generic_review":
            return {"review": "offline deterministic review", "confidence": 0.5}
        return {"result": "offline deterministic result"}

    def _knowledge_atoms(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        paper = payload["paper"]
        chunks = payload.get("chunks", [])
        text = "\n".join(chunk.get("text", "") for chunk in chunks)
        first_trace = chunks[0].get("source_trace", "user-provided text chunk") if chunks else "user-provided text chunk"
        paper_id = paper["paper_id"]
        question = _label(text, "Research question") or _label(text, "Question") or "unknown"
        entity = _label(text, "Entity") or _infer_entity(text)
        intervention = _label(text, "Input") or _label(text, "Intervention") or _infer_input(text)
        condition = _label(text, "Condition") or _infer_condition(text)
        mechanism = _label(text, "Mechanism") or _infer_mechanism(text)
        outcome = _label(text, "Outcome") or _infer_outcome(text)
        gap = _label(text, "Gap") or "replication status and boundary conditions require human review"
        next_step = _label(text, "Next step") or "compare with related mechanisms and identify replication needs"
        evidence_type = _infer_evidence_type(text, paper.get("source_type", "unknown"))
        evidence_strength = "toy evidence for pipeline demonstration; not a real scientific claim"
        candidates = _connection_candidates(text)

        base = {
            "paper_id": paper_id,
            "source_trace": first_trace,
            "paper_question": question,
            "field_question": "How do specific variables, mechanisms, and evidence units connect across related studies?",
            "discovery_question": "Which gaps or next experiments become visible when claims are compared at the mechanism level?",
            "entity": entity,
            "input_signal_or_intervention": intervention,
            "condition": condition,
            "mechanism": mechanism,
            "outcome": outcome,
            "evidence_type": evidence_type,
            "evidence_strength": evidence_strength,
            "boundary_conditions": condition if condition != "not reported" else "not reported",
            "assumptions": "offline stub extracts from fictional or user-provided text and requires review",
            "gap": gap,
            "connection_candidates": candidates,
            "next_step": next_step,
            "confidence": 0.62,
            "human_review_required": True,
        }
        return [
            {
                **base,
                "atom_id": stable_id("atom", paper_id, "question", question),
                "atom_type": "research_question",
                "evidence_statement": f"The source asks: {question}",
            },
            {
                **base,
                "atom_id": stable_id("atom", paper_id, "claim", outcome, mechanism),
                "atom_type": "evidence_claim",
                "evidence_statement": f"The source links {intervention} to {outcome} through {mechanism}.",
            },
        ]


def _label(text: str, label: str) -> str | None:
    pattern = rf"^{re.escape(label)}\s*:\s*(.+)$"
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else None


def _infer_entity(text: str) -> str:
    lowered = text.lower()
    if "cell" in lowered:
        return "cell model"
    if "editor" in lowered or "conference" in lowered:
        return "research community"
    return "not reported"


def _infer_input(text: str) -> str:
    lowered = text.lower()
    if "electric" in lowered or "frequency" in lowered or "field" in lowered:
        return "bioelectric or electromagnetic exposure"
    if "review" in lowered:
        return "research synthesis"
    return "not reported"


def _infer_condition(text: str) -> str:
    lowered = text.lower()
    if "72 hour" in lowered:
        return "72 hour exposure window"
    if "low intensity" in lowered:
        return "low intensity condition"
    return "not reported"


def _infer_mechanism(text: str) -> str:
    lowered = text.lower()
    mechanisms = []
    if "calcium" in lowered:
        mechanisms.append("calcium signaling")
    if "membrane" in lowered or "voltage" in lowered:
        mechanisms.append("membrane voltage")
    if "ion channel" in lowered:
        mechanisms.append("ion channel activity")
    if mechanisms:
        return ", ".join(mechanisms)
    return "mechanism not directly reported"


def _infer_outcome(text: str) -> str:
    lowered = text.lower()
    if "proliferation" in lowered:
        return "cell proliferation changed in the reported toy setup"
    if "migration" in lowered:
        return "cell migration changed in the reported toy setup"
    if "agenda" in lowered or "research direction" in lowered:
        return "research priorities were organized"
    return "outcome not reported"


def _infer_evidence_type(text: str, source_type: str) -> str:
    lowered = f"{text} {source_type}".lower()
    if "in vitro" in lowered or "cell culture" in lowered:
        return "in vitro"
    if "review" in lowered:
        return "review"
    if "conference" in lowered:
        return "conference review"
    return "user-provided text"


def _connection_candidates(text: str) -> list[str]:
    lowered = text.lower()
    candidates = []
    for term in [
        "bioelectric signaling",
        "membrane voltage",
        "calcium signaling",
        "ion channels",
        "frequency exposure",
        "cell proliferation",
        "cell migration",
        "replication",
    ]:
        if term in lowered:
            candidates.append(term)
    return candidates or ["mechanism-level comparison"]

