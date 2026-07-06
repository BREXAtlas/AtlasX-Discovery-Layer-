"""Anthropic (Claude) provider.

Optional provider that generates JSON for AtlasX agents through the official
`anthropic` Python SDK. It is not required for offline tests: the missing-key
error is raised before the SDK is imported, and the client is injectable so
tests can mock it without installing `anthropic` or setting a key.
"""

from __future__ import annotations

import json
import os
from typing import Any

from atlasx.providers.base import BaseProvider
from atlasx.utils.json_tools import extract_json_payload

# Default model when ANTHROPIC_MODEL is not set. Kept as an alias (no date
# suffix) so it tracks the current Claude release.
DEFAULT_ANTHROPIC_MODEL = "claude-opus-4-8"
DEFAULT_MAX_TOKENS = 4096


class AnthropicProvider(BaseProvider):
    """JSON generation through the Anthropic Messages API.

    The provider asks Claude to return a JSON object for a named schema and
    extracts the JSON payload from the response text, mirroring the OpenAI and
    local providers so the rest of the pipeline is provider-agnostic.
    """

    name = "anthropic"

    def __init__(
        self,
        model: str | None = None,
        *,
        client: Any | None = None,
        api_key: str | None = None,
    ) -> None:
        """Configure the provider.

        Args:
            model: Model id; falls back to ``ANTHROPIC_MODEL`` then the default.
            client: Pre-built Anthropic client, mainly for tests/mocking. When
                provided, no API key is required and the SDK is not imported.
            api_key: Explicit key; falls back to ``ANTHROPIC_API_KEY``.
        """

        self.model = model or os.getenv("ANTHROPIC_MODEL") or DEFAULT_ANTHROPIC_MODEL
        self.max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", str(DEFAULT_MAX_TOKENS)))

        temperature = os.getenv("ANTHROPIC_TEMPERATURE")
        # Temperature is only accepted by older Claude models; newer models
        # reject it. Only send it when the user explicitly opts in.
        self.temperature: float | None = (
            float(temperature) if temperature not in (None, "") else None
        )

        if client is not None:
            self.client = client
            return

        # Raise the missing-key error before importing the SDK so offline tests
        # (which may not have `anthropic` installed) still get a clear message.
        resolved_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not resolved_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is required for --provider anthropic."
            )

        try:
            from anthropic import Anthropic
        except ImportError as exc:  # pragma: no cover - exercised only without extra
            raise RuntimeError(
                "The 'anthropic' package is required for --provider anthropic. "
                "Install it with: pip install 'atlasx-discovery-layer[anthropic]'"
            ) from exc

        self.client = Anthropic(api_key=resolved_key)

    def generate_json(
        self,
        *,
        schema_name: str,
        system_prompt: str,
        user_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a JSON object for ``schema_name`` produced by Claude."""

        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Return a single JSON object for schema `{schema_name}`. "
                        "Respond with JSON only, no prose. "
                        f"Payload:\n{json.dumps(user_payload, indent=2)}"
                    ),
                }
            ],
        }
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature

        message = self.client.messages.create(**kwargs)
        text = _text_from_message(message)
        data = extract_json_payload(text)
        if not isinstance(data, dict):
            raise ValueError("Anthropic provider returned JSON that was not an object.")
        return data


def _text_from_message(message: Any) -> str:
    """Concatenate text from an Anthropic Messages API response.

    Handles the SDK's content-block list (blocks with ``type == "text"``) and a
    plain string, so both the real client and simple test doubles work.
    """

    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content

    parts: list[str] = []
    for block in content or []:
        block_type = getattr(block, "type", None)
        text = getattr(block, "text", None)
        if text is not None and (block_type in (None, "text")):
            parts.append(text)
    return "".join(parts)
