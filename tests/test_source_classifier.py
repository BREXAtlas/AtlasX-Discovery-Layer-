from atlasx.models.source import SourceDocument, SourceMetadata
from atlasx.routing.source_classifier import classify_source


def _doc(
    text: str,
    *,
    source_id: str = "src1",
    source_type: str = "unknown",
    title: str = "Test Source",
    doi: str | None = None,
    journal: str = "unknown",
    tags: list[str] | None = None,
    route_hint: str | None = None,
) -> SourceDocument:
    return SourceDocument(
        metadata=SourceMetadata(
            source_id=source_id,
            title=title,
            source_type=source_type,
            file="source.txt",
            doi=doi,
            journal=journal,
            tags=tags or [],
            route_hint=route_hint,
        ),
        text=text,
        chunks=[],
    )


def test_research_classification() -> None:
    decision = classify_source(
        _doc(
            "Abstract\nMethods\nResults\nThe study used participants and a dataset.",
            doi="10.1234/example",
            journal="Example Journal",
        )
    )

    assert decision.route == "research"
    assert decision.source_kind == "research_article"


def test_general_document_classification() -> None:
    decision = classify_source(_doc("A short reflective note about local source ownership."))

    assert decision.route == "general"
    assert decision.source_kind == "general_document"


def test_learning_classification() -> None:
    decision = classify_source(
        _doc("Learning objectives: students will define key terms. Quiz follows.")
    )

    assert decision.route == "learning"
    assert decision.source_kind == "curriculum_lesson"


def test_strategic_brief_classification() -> None:
    decision = classify_source(
        _doc("Policy strategy recommendation with stakeholder risk and budget decisions.")
    )

    assert decision.route == "strategic_brief"
    assert decision.source_kind == "policy_document"


def test_route_hint_override() -> None:
    decision = classify_source(_doc("ordinary text", route_hint="learning"))

    assert decision.route == "learning"
    assert any("route_hint" in reason for reason in decision.reasons)


def test_unknown_fallback() -> None:
    decision = classify_source(_doc("", title="", source_type=""))

    assert decision.route == "unknown"
    assert decision.confidence < 0.5
