"""Deterministic source route classification."""

from __future__ import annotations

from atlasx.models.source import SourceDocument, SourceMetadata
from atlasx.models.source_route import ROUTES, SourceRouteDecision

ROUTE_HINTS = ROUTES - {"unknown"}

RESEARCH_SIGNALS = {
    "abstract",
    "methods",
    "methodology",
    "results",
    "discussion",
    "conclusion",
    "study",
    "sample",
    "participants",
    "findings",
    "statistically significant",
    "literature review",
    "experiment",
    "clinical",
    "in vitro",
    "in vivo",
    "dataset",
}

LEARNING_SIGNALS = {
    "learning objectives",
    "lesson",
    "chapter",
    "quiz",
    "students will",
    "key terms",
    "curriculum",
    "study guide",
}

STRATEGIC_SIGNALS = {
    "policy",
    "strategy",
    "stakeholder",
    "recommendation",
    "risk",
    "implementation",
    "budget",
    "operations",
    "proposal",
    "decision",
}


def classify_sources(documents: list[SourceDocument]) -> list[SourceRouteDecision]:
    """Classify all source documents."""

    return [classify_source(document) for document in documents]


def classify_source(document: SourceDocument) -> SourceRouteDecision:
    """Classify one source document into a notebook route."""

    metadata = document.metadata
    route_hint = (metadata.route_hint or "").strip().lower()
    if route_hint == "auto":
        route_hint = ""
    if route_hint in ROUTE_HINTS:
        return SourceRouteDecision(
            source_id=metadata.source_id,
            route=route_hint,
            source_kind=_source_kind(metadata, document.text, route_hint),
            confidence=0.95,
            reasons=[f"route_hint requested {route_hint}"],
            warnings=["route hint should be reviewed against source content"],
        )

    evidence = _evidence_text(metadata, document.text)
    reasons: list[str] = []
    warnings: list[str] = []

    if not document.text.strip() and not _has_meaningful_metadata(metadata):
        return SourceRouteDecision(
            source_id=metadata.source_id,
            route="unknown",
            source_kind="unknown",
            confidence=0.2,
            reasons=["no source text or meaningful metadata available"],
            warnings=["not enough source text or metadata to classify confidently"],
        )

    research_score = _score(evidence, RESEARCH_SIGNALS)
    learning_score = _score(evidence, LEARNING_SIGNALS)
    strategic_score = _score(evidence, STRATEGIC_SIGNALS)

    if metadata.doi:
        research_score += 3
        reasons.append("DOI present")
    if metadata.journal and metadata.journal.lower() != "unknown":
        research_score += 2
        reasons.append("journal present")
    if metadata.abstract:
        research_score += 1
        reasons.append("abstract present")

    for route_name, score in [
        ("research", research_score),
        ("learning", learning_score),
        ("strategic_brief", strategic_score),
    ]:
        if score > 0:
            reasons.append(f"{route_name} signals: {score}")

    if research_score >= max(learning_score, strategic_score, 2):
        route = "research"
        confidence = _confidence(research_score)
    elif learning_score >= max(strategic_score, 2):
        route = "learning"
        confidence = _confidence(learning_score)
    elif strategic_score >= 2:
        route = "strategic_brief"
        confidence = _confidence(strategic_score)
    elif not evidence.strip():
        route = "unknown"
        confidence = 0.2
        warnings.append("not enough source text or metadata to classify confidently")
    else:
        route = "general"
        confidence = 0.55
        reasons.append("no specialized route threshold met; using general route")

    return SourceRouteDecision(
        source_id=metadata.source_id,
        route=route,
        source_kind=_source_kind(metadata, document.text, route),
        confidence=confidence,
        reasons=reasons or ["classification used deterministic fallback"],
        warnings=warnings,
    )


def _evidence_text(metadata: SourceMetadata, text: str) -> str:
    parts = [
        metadata.title,
        metadata.source_type,
        metadata.journal,
        metadata.abstract or "",
        metadata.notes or "",
        metadata.file,
        " ".join(metadata.tags),
        text[:5000],
    ]
    return "\n".join(parts).lower()


def _has_meaningful_metadata(metadata: SourceMetadata) -> bool:
    return any(
        [
            metadata.title and metadata.title.lower() != "unknown",
            metadata.source_type and metadata.source_type.lower() != "unknown",
            metadata.journal and metadata.journal.lower() != "unknown",
            metadata.abstract,
            metadata.notes,
            metadata.doi,
            metadata.tags,
            metadata.url,
        ]
    )


def _score(text: str, signals: set[str]) -> int:
    return sum(1 for signal in signals if signal in text)


def _confidence(score: int) -> float:
    return min(0.9, 0.5 + (score * 0.08))


def _source_kind(metadata: SourceMetadata, text: str, route: str) -> str:
    evidence = _evidence_text(metadata, text)
    source_type = metadata.source_type.lower()
    if "thesis" in evidence or "dissertation" in evidence:
        return "thesis_dissertation"
    if "literature review" in evidence or "review" in source_type:
        return "literature_review"
    if route == "research":
        return "research_article"
    if "whitepaper" in evidence or "white paper" in evidence or "report" in source_type:
        return "report_whitepaper"
    if "book chapter" in evidence or "chapter" in source_type:
        return "book_chapter"
    if "essay" in evidence or "essay" in source_type:
        return "essay"
    if "policy" in evidence:
        return "policy_document"
    if "legal" in evidence or "statute" in evidence:
        return "legal_document"
    if route == "learning":
        return "curriculum_lesson"
    if "transcript" in evidence:
        return "transcript"
    if "meeting" in evidence or "minutes" in evidence:
        return "meeting_notes"
    if metadata.url:
        return "website_article"
    if route == "unknown":
        return "unknown"
    return "general_document"
