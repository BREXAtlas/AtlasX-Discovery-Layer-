"""Provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    """Minimal JSON-generation interface for AtlasX agents."""

    name: str
    model: str | None

    @abstractmethod
    def generate_json(
        self,
        *,
        schema_name: str,
        system_prompt: str,
        user_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a JSON-like dictionary for a named schema."""

