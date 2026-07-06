from pydantic import ValidationError

from atlasx.models.source import SourceMetadata
from atlasx.models.source_atom import SourceAtom
from atlasx.models.source_route import SourceRouteDecision


def test_source_metadata_preserves_unknown_defaults() -> None:
    metadata = SourceMetadata(source_id="src1", title="", source_type="", file="note.txt")

    assert metadata.title == "unknown"
    assert metadata.source_type == "unknown"
    assert metadata.journal == "unknown"


def test_source_atom_preserves_unknowns_and_bounds_confidence() -> None:
    atom = SourceAtom(atom_id="a1", source_id="src1", source_trace="note.txt; chunk 1", main_topic="")

    assert atom.main_topic == "unknown"
    assert atom.method_or_process == "not applicable"
    assert atom.human_review_required is True

    try:
        SourceAtom(
            atom_id="a2",
            source_id="src1",
            source_trace="note.txt; chunk 1",
            confidence=2,
        )
    except ValidationError as exc:
        assert "less than or equal to 1" in str(exc)
    else:
        raise AssertionError("Expected confidence validation to fail")


def test_source_route_unknowns_invalid_route() -> None:
    decision = SourceRouteDecision(
        source_id="src1",
        route="not-a-route",
        source_kind="",
        confidence=0.3,
    )

    assert decision.route == "unknown"
    assert decision.source_kind == "unknown"

