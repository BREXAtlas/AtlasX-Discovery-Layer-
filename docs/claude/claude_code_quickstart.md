# Claude Code quickstart

Use AtlasX with Claude Code in a few minutes. Start offline — no API key needed.

## 1. Clone and install

```bash
git clone https://github.com/BREXAtlas/AtlasX-Discovery-Layer-.git
cd atlasx-discovery-layer
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
claude
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` instead of
`source .venv/bin/activate`.

When you launch `claude` in this directory, Claude Code automatically reads
[`CLAUDE.md`](../../CLAUDE.md) and the Claude project files under `.claude/`.

## 2. Ask Claude to run the sample project

In Claude Code:

> Use the AtlasX Discovery Layer to process `examples/sample_project` in offline
> mode, run tests, and show me the generated report.

Or drive it with a skill:

> Use the atlasx-run-discovery skill to process `examples/sample_project` in
> offline mode, then summarize the generated outputs.

## 3. Run it yourself

```bash
atlasx run --project examples/sample_project --provider offline
atlasx graph  --project examples/sample_project
atlasx report --project examples/sample_project
pytest
```

Outputs are written to `examples/sample_project/outputs/`.

## 4. Optional: use the Anthropic provider

```bash
pip install -e ".[anthropic]"
export ANTHROPIC_API_KEY=your_key_here
atlasx run --project examples/sample_project --provider anthropic --model $ANTHROPIC_MODEL
```

See [anthropic_api_provider.md](anthropic_api_provider.md). Prefer offline mode
first; it is deterministic and needs no key.

## Safety reminders

- Do not commit PDFs or copyrighted article text.
- Do not expose API keys; `.env` is gitignored.
- All outputs require human review.
