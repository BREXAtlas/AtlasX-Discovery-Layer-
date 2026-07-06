# Anthropic (Claude) API provider

AtlasX ships an optional provider that runs the pipeline through Claude via the
official `anthropic` Python SDK. Offline mode remains the default and needs no
key; use the Anthropic provider when you want Claude-quality extraction.

## Install

```bash
pip install -e ".[anthropic]"
```

## Configure

Copy `.env.example` to `.env` and set the Anthropic variables (or export them):

```bash
ANTHROPIC_API_KEY=your_key_here
# Leave blank to use the provider default (claude-opus-4-8).
ANTHROPIC_MODEL=
ANTHROPIC_MAX_TOKENS=4096
# Optional; only older Claude models accept temperature. Leave blank otherwise.
ANTHROPIC_TEMPERATURE=
```

Never hard-code secrets and never commit `.env` (it is gitignored). An Anthropic
API key is **not** required for offline tests or the offline pipeline.

## Run

```bash
atlasx run --project examples/sample_project --provider anthropic --model $ANTHROPIC_MODEL
```

If `--model` is omitted, the provider uses `ANTHROPIC_MODEL`, then the default
`claude-opus-4-8`.

## Behavior

- Accepts a system prompt and a user payload, and returns a JSON object for a
  named schema (the same `BaseProvider.generate_json` interface as the offline,
  local, and OpenAI providers).
- Extracts the JSON payload from Claude's response, so the rest of the pipeline
  is provider-agnostic.
- Raises a clear error when `ANTHROPIC_API_KEY` is missing.
- Has a mockable interface: `AnthropicProvider(client=...)` accepts an injected
  client, so tests never need the SDK, a key, or the network.

## A note on `temperature`

Newer Claude models (Opus 4.6+, Opus 4.7/4.8, Sonnet 5, Fable) reject the
`temperature` parameter. The provider therefore sends `temperature` **only** when
`ANTHROPIC_TEMPERATURE` is explicitly set. Leave it blank unless you are using an
older model that accepts it.

## Human review still required

Claude-backed outputs are research-support artifacts, not final scientific,
medical, legal, or editorial decisions. Review them with domain experts.
