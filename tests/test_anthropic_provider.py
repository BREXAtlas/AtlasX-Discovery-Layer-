"""Tests for the optional Anthropic provider.

These tests do not require the `anthropic` package, an API key, or network
access — the client is injected as a mock and the missing-key error is raised
before the SDK is imported.
"""

from __future__ import annotations

import pytest

from atlasx.providers import AnthropicProvider, get_provider


class _FakeBlock:
    def __init__(self, text: str, block_type: str = "text") -> None:
        self.type = block_type
        self.text = text


class _FakeMessage:
    def __init__(self, text: str) -> None:
        self.content = [_FakeBlock(text)]


class _FakeMessages:
    def __init__(self, text: str) -> None:
        self._text = text
        self.calls: list[dict] = []

    def create(self, **kwargs) -> _FakeMessage:
        self.calls.append(kwargs)
        return _FakeMessage(self._text)


class _FakeClient:
    def __init__(self, text: str) -> None:
        self.messages = _FakeMessages(text)


def test_missing_key_raises_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        AnthropicProvider()


def test_generate_json_with_mock_client(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_TEMPERATURE", raising=False)
    client = _FakeClient('{"review": "ok", "confidence": 0.5}')
    provider = AnthropicProvider(model="claude-test", client=client)

    result = provider.generate_json(
        schema_name="generic_review",
        system_prompt="You are a reviewer.",
        user_payload={"paper": {"paper_id": "p1"}},
    )

    assert result == {"review": "ok", "confidence": 0.5}
    call = client.messages.calls[0]
    assert call["model"] == "claude-test"
    assert call["system"] == "You are a reviewer."
    # Temperature must be omitted by default (newer models reject it).
    assert "temperature" not in call


def test_generate_json_extracts_json_from_surrounding_text() -> None:
    client = _FakeClient('Here is the JSON:\n{"result": "x"}\nThanks.')
    provider = AnthropicProvider(model="claude-test", client=client)
    result = provider.generate_json(
        schema_name="anything",
        system_prompt="s",
        user_payload={},
    )
    assert result == {"result": "x"}


def test_temperature_included_when_env_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_TEMPERATURE", "0.2")
    client = _FakeClient('{"ok": true}')
    provider = AnthropicProvider(model="claude-test", client=client)
    provider.generate_json(schema_name="s", system_prompt="s", user_payload={})
    assert client.messages.calls[0]["temperature"] == 0.2


def test_non_object_json_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_TEMPERATURE", raising=False)
    client = _FakeClient("[1, 2, 3]")
    provider = AnthropicProvider(model="claude-test", client=client)
    with pytest.raises(ValueError):
        provider.generate_json(schema_name="s", system_prompt="s", user_payload={})


def test_get_provider_routes_to_anthropic(monkeypatch: pytest.MonkeyPatch) -> None:
    # No key configured, so routing to the anthropic provider should raise the
    # provider's RuntimeError (not the unknown-provider ValueError).
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        get_provider("anthropic")


def test_get_provider_unknown_raises_value_error() -> None:
    with pytest.raises(ValueError):
        get_provider("does-not-exist")
