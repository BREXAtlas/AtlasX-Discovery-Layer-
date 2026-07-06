"""OpenAI provider."""

from __future__ import annotations

import os
import json
from typing import Any

from openai import OpenAI

from atlasx.providers.base import BaseProvider
from atlasx.utils.json_tools import extract_json_payload


class OpenAIProvider(BaseProvider):
    """JSON generation through the OpenAI Python SDK."""

    name = "openai"

    def __init__(self, model: str | None = None) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for --provider openai.")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(api_key=api_key)

    def generate_json(
        self,
        *,
        schema_name: str,
        system_prompt: str,
        user_payload: dict[str, Any],
    ) -> dict[str, Any]:
        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Return JSON for schema `{schema_name}`. "
                        f"Payload:\n{json.dumps(user_payload, indent=2)}"
                    ),
                },
            ],
        )
        content = response.choices[0].message.content or "{}"
        data = extract_json_payload(content)
        if not isinstance(data, dict):
            raise ValueError("OpenAI provider returned JSON that was not an object.")
        return data
