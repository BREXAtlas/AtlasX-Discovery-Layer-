from pydantic import ValidationError

from atlasx.models.knowledge_atom import KnowledgeAtom


def test_knowledge_atom_preserves_unknown_defaults() -> None:
    atom = KnowledgeAtom(
        atom_id="atom_1",
        paper_id="paper_1",
        source_trace="sample.txt; chunk 1",
        entity="",
        confidence=0.4,
    )

    assert atom.entity == "unknown"
    assert atom.input_signal_or_intervention == "not reported"
    assert atom.human_review_required is True


def test_knowledge_atom_confidence_bounds() -> None:
    try:
        KnowledgeAtom(
            atom_id="atom_1",
            paper_id="paper_1",
            source_trace="sample.txt; chunk 1",
            confidence=1.5,
        )
    except ValidationError as exc:
        assert "less than or equal to 1" in str(exc)
    else:
        raise AssertionError("Expected confidence validation to fail")

