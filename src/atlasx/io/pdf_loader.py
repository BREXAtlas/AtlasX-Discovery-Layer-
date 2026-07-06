"""Optional PDF loading."""

from __future__ import annotations

from pathlib import Path


def load_pdf_text(path: Path) -> str:
    """Extract text from a PDF when pypdf is installed."""

    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "PDF loading requires the optional dependency: pip install -e '.[pdf]'"
        ) from exc

    reader = PdfReader(str(path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"[page {index}]\n{text}")
    return "\n\n".join(pages)

