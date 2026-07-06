"""Text and Markdown loading."""

from __future__ import annotations

from pathlib import Path


def load_text_file(path: Path) -> str:
    """Load UTF-8 text with a helpful error message."""

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")

