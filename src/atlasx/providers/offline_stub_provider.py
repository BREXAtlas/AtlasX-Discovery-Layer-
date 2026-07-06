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
        if schema_name == "source_atoms":
            return {"source_atoms": self._source_atoms(user_payload)}
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

    def _source_atoms(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        source = payload["source"]
        chunks = payload.get("chunks", [])
        route = payload.get("route", "general")
        text = "\n".join(chunk.get("text", "") for chunk in chunks)
        first_trace = (
            chunks[0].get("source_trace", "user-provided text chunk")
            if chunks
            else "user-provided text chunk"
        )
        source_id = source["source_id"]
        title = source.get("title") or "unknown"
        main_topic = _label(text, "Main topic") or _label(text, "Title") or title
        core_claim = (
            _label(text, "Core claim")
            or _label(text, "Claim")
            or _first_sentence(text)
            or "unknown"
        )
        summary = _label(text, "Summary") or core_claim
        terms = _terms(text)
        return [
            {
                "atom_id": stable_id("source_atom", source_id, route, main_topic, core_claim),
                "source_id": source_id,
                "source_trace": first_trace,
                "route": route,
                "source_type": source.get("source_type", "unknown"),
                "atom_type": "source_summary",
                "main_topic": main_topic,
                "question_answered": _label(text, "Question") or "unknown",
                "core_claim": core_claim,
                "supporting_points": _bullet_like_lines(text)[:5],
                "evidence_or_examples": _sentences_with(text, ["example", "evidence", "because"])[:5],
                "key_terms": terms,
                "named_entities": _named_entities(text),
                "timeline_or_sequence": _sentences_with(text, ["first", "then", "next", "finally"])[:5],
                "method_or_process": _label(text, "Process") or "not applicable",
                "assumptions": _label(text, "Assumptions") or "unknown",
                "limitations": _label(text, "Limitations") or "unknown",
                "contradictions": _sentences_with(text, ["however", "contradiction", "conflict"])[:5],
                "connections": terms[:5] or ["not reported"],
                "open_questions": _sentences_with(text, ["question", "unclear", "unknown"])[:5],
                "action_items": _sentences_with(text, ["should", "recommend", "action", "next step"])[:5],
                "study_notes": [f"Review source trace: {first_trace}", "Human review required."],
                "user_takeaway": _label(text, "Takeaway") or summary,
                "summary": summary,
                "confidence": 0.58,
                "human_review_required": True,
            }
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


def _first_sentence(text: str) -> str | None:
    clean = " ".join(line.strip() for line in text.splitlines() if line.strip())
    if not clean:
        return None
    sentence = re.split(r"(?<=[.!?])\s+", clean)[0].strip()
    return sentence[:300] if sentence else None


def _bullet_like_lines(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip(" -\t")
        if stripped and (line.lstrip().startswith(("-", "*")) or ":" in line):
            lines.append(stripped)
    return lines


def _sentences_with(text: str, terms: list[str]) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(text.split()))
    output: list[str] = []
    for sentence in sentences:
        lowered = sentence.lower()
        if any(term in lowered for term in terms):
            output.append(sentence[:300])
    return output


def _terms(text: str) -> list[str]:
    lowered = text.lower()
    terms = []
    for term in [
        "source-grounded answers",
        "local-first",
        "policy",
        "strategy",
        "learning objectives",
        "key terms",
        "timeline",
        "evidence",
        "implementation",
        "risk",
    ]:
        if term in lowered:
            terms.append(term)
    return terms


def _named_entities(text: str) -> list[str]:
    matches = re.findall(r"\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3}\b", text)
    seen: list[str] = []
    for match in matches:
        if match not in seen and len(match) > 2:
            seen.append(match)
    return seen[:10]
