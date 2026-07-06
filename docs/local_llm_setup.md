# Local LLM Setup

AtlasX can use local models through any OpenAI-compatible endpoint.

## Environment Variables

```bash
LOCAL_LLM_BASE_URL=http://localhost:11434/v1
LOCAL_LLM_API_KEY=
LOCAL_LLM_MODEL=llama3.1
```

`LOCAL_LLM_API_KEY` is optional for many local servers. If your server requires
a key, set it in `.env` or your shell environment.

## Example

```bash
atlasx run --project examples/sample_project --provider local --model llama3.1
```

## Notes

- Local model quality varies. Review outputs carefully.
- Prefer models that can follow JSON instructions.
- Keep temperature low when reproducibility matters.
- Use offline mode first to verify the project folder and outputs.

