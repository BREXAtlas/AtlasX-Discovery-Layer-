"""JSON helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def write_json(path: Path, payload: Any) -> None:
    """Write dictionaries, lists, or Pydantic models as pretty JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, BaseModel):
        data = payload.model_dump(mode="json")
    elif isinstance(payload, list):
        data = [
            item.model_dump(mode="json") if isinstance(item, BaseModel) else item
            for item in payload
        ]
    else:
        data = payload
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    """Read JSON from disk."""

    return json.loads(path.read_text(encoding="utf-8"))


def extract_json_payload(text: str) -> Any:
    """Parse a JSON response, tolerating fenced code blocks."""

    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        stripped = "\n".join(line for line in lines[1:] if line.strip() != "```")
    return json.loads(stripped)

