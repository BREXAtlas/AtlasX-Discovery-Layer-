"""LLM provider implementations."""

from atlasx.providers.base import BaseProvider
from atlasx.providers.local_openai_compatible_provider import LocalOpenAICompatibleProvider
from atlasx.providers.offline_stub_provider import OfflineStubProvider
from atlasx.providers.openai_provider import OpenAIProvider

__all__ = [
    "BaseProvider",
    "LocalOpenAICompatibleProvider",
    "OfflineStubProvider",
    "OpenAIProvider",
    "get_provider",
]


def get_provider(provider: str, model: str | None = None) -> BaseProvider:
    """Return a provider by CLI name."""

    normalized = provider.lower().strip()
    if normalized == "offline":
        return OfflineStubProvider(model=model)
    if normalized == "openai":
        return OpenAIProvider(model=model)
    if normalized == "local":
        return LocalOpenAICompatibleProvider(model=model)
    raise ValueError(f"Unknown provider {provider!r}. Choose offline, local, or openai.")

