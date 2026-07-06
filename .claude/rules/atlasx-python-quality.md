# Rule: Python quality

The AtlasX package targets clarity and reviewability so nonspecialist
contributors can trust and extend it.

- **Python 3.11+.** Use modern typing (`list[str]`, `str | None`).
- **Type hints** on public functions and methods.
- **Docstrings** on modules, public classes, and public functions.
- **Small functions.** Prefer several focused functions over one large one.
- **Pydantic v2** for data validation and models (`src/atlasx/models/`).
- **Typer** for the CLI (`src/atlasx/cli.py`); **Rich** for terminal output.
- **Deterministic where possible.** The offline provider must stay deterministic
  so tests and demos are reproducible without network access.
- **Match existing style.** Mirror the conventions already in `src/atlasx/`
  (naming, imports, `from __future__ import annotations`) rather than
  introducing a new style.
- **Tests must not require API keys.** New code paths that call a paid provider
  must be mockable and covered by tests that mock the client.

Run `pytest` after changes. Do not claim a change works until it has been run.
