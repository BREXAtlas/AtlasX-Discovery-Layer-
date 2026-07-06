# Contributing to AtlasX Discovery Layer

Thank you for helping improve AtlasX. This project is experimental research
infrastructure for turning papers into structured knowledge atoms, connections,
gaps, and responsible discovery directions.

## Ways to contribute

- Improve extraction schemas and validation.
- Add loaders for lawful source formats.
- Improve local LLM prompts and parsing.
- Add graph exports and visualization options.
- Add tests for new agent behavior.
- Improve documentation around provenance, bias, and copyright-safe use.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,pdf]"
pytest
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,pdf]"
pytest
```

## Contribution standards

- Preserve source traceability for every generated claim.
- Preserve uncertainty instead of forcing certainty.
- Do not add copyrighted article text to examples or tests.
- Keep offline mode deterministic.
- Add or update tests for behavior changes.
- Prefer small, reviewable changes.

## Pull request checklist

- Tests pass with `pytest`.
- Public examples contain fictional, public-domain-style text only.
- No API keys, PDFs, or licensed sources are committed.
- Documentation explains any new output fields or agent behavior.

