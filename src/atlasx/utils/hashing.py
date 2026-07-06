"""Stable identifiers for generated artifacts."""

from __future__ import annotations

import hashlib
import re


def slugify(value: str, fallback: str = "item") -> str:
    """Convert text into a conservative identifier."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return slug or fallback


def short_hash(*parts: object, length: int = 10) -> str:
    """Return a short deterministic hash for ID creation."""

    payload = "|".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length]


def stable_id(prefix: str, *parts: object) -> str:
    """Create a stable identifier with a readable prefix."""

    return f"{prefix}_{short_hash(*parts)}"

