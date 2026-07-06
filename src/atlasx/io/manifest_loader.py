"""Load and validate source manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from atlasx.models.paper import PaperMetadata
from atlasx.utils.hashing import slugify


def load_source_manifest(manifest_path: Path) -> list[PaperMetadata]:
    """Load `source_manifest.yaml` into paper metadata records."""

    if not manifest_path.exists():
        return []
    raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    sources = raw.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError(f"{manifest_path} must contain a list under `sources`.")
    return [_metadata_from_source(item, index) for index, item in enumerate(sources, start=1)]


def _metadata_from_source(source: dict[str, Any], index: int) -> PaperMetadata:
    title = source.get("title") or "unknown"
    file_name = source.get("file") or source.get("path")
    if not file_name:
        raise ValueError(f"Manifest source #{index} is missing `file`.")
    paper_id = source.get("paper_id") or slugify(title, fallback=f"paper_{index:03d}")
    authors = source.get("authors") or []
    if isinstance(authors, str):
        authors = [authors]
    return PaperMetadata(
        paper_id=paper_id,
        title=title,
        authors=authors,
        year=source.get("year"),
        journal=source.get("journal") or "unknown",
        doi=source.get("doi"),
        source_type=source.get("source_type") or "unknown",
        file=file_name,
        tags=source.get("tags") or [],
        abstract=source.get("abstract"),
        notes=source.get("notes"),
        license_status=source.get("license_status") or "user-provided",
    )

