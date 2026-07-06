# OpenAI Setup

AtlasX can call OpenAI through the official Python SDK.

## Environment Variables

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Do not commit `.env`.

## Example

```bash
atlasx run --project examples/sample_project --provider openai --model gpt-4.1-mini
```

## Output Validation

AtlasX validates provider output with Pydantic models. If a model omits required
fields, the pipeline fills safe defaults where possible and fails with a clear
error where validation cannot be satisfied.

## Review

OpenAI output is still AI-generated. Preserve source traces, review extracted
claims against the original source, and avoid overclaiming.

