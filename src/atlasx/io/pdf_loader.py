"""Optional PDF loading."""

from __future__ import annotations

from pathlib import Path


def load_pdf_text(path: Path) -> str:
    """Extract text from a PDF when pypdf is installed."""

    pages = load_pdf_pages(path)
    return "\n\n".join(f"[page {page_number}]\n{text}" for page_number, text in pages)


def load_pdf_pages(path: Path) -> list[tuple[int, str]]:
    """Extract page-numbered text from a PDF when pypdf is installed."""

    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "PDF support requires installing AtlasX with the pdf extra: "
            "pip install -e '.[pdf]'"
        ) from exc

    reader = PdfReader(str(path))
    pages: list[tuple[int, str]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append((index, text.strip()))
    if not any(text for _, text in pages):
        raise RuntimeError(
            f"No extractable text found in {path.name}. Scanned/OCR-only PDFs "
            "are not yet supported by the base PDF loader."
        )
    return pages
