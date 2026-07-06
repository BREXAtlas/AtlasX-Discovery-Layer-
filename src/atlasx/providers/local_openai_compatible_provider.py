"""Local OpenAI-compatible provider."""

from __future__ import annotations

import os
import json
from typing import Any

from openai import OpenAI

from atlasx.providers.base import BaseProvider
from atlasx.utils.json_tools import extract_json_payload


class LocalOpenAICompatibleProvider(BaseProvider):
    """Use Ollama, LM Studio, vLLM, LocalAI, or any compatible endpoint."""

    name = "local"

    def __init__(self, model: str | None = None) -> None:
        base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
        api_key = os.getenv("LOCAL_LLM_API_KEY") or "local-not-required"
        self.model = model or os.getenv("LOCAL_LLM_MODEL", "llama3.1")
        self.client = OpenAI(base_url=base_url, api_key=api_key)

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
            raise ValueError("Local provider returned JSON that was not an object.")
        return data
