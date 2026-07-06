import builtins
from pathlib import Path

import pytest

from atlasx.io import loaders
from atlasx.io.pdf_loader import load_pdf_pages


def test_pdf_missing_dependency_error(monkeypatch: pytest.MonkeyPatch) -> None:
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "pypdf":
            raise ImportError("missing pypdf")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match="pdf extra"):
        load_pdf_pages(Path("demo.pdf"))


def test_pdf_chunks_preserve_page_trace(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        loaders,
        "load_pdf_pages",
        lambda path: [(1, "Page one text."), (2, "Page two text.")],
    )

    text, chunks = loaders._load_paper_text_and_chunks("pdf_source", Path("demo.pdf"))

    assert "[page 1]" in text
    assert chunks[0].page == 1
    assert chunks[0].source_trace == "demo.pdf; page 1"
    assert chunks[1].chunk_id == "pdf_source_page_002"

