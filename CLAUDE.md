# CLAUDE.md — AtlasX Discovery Layer

Guidance for Claude Code (and other agents that read `CLAUDE.md`) when working in
this repository. This file is committed and public. It adds Claude-native support
on top of the existing Codex-created project — it does not replace it.

## Project purpose

AtlasX Discovery Layer is an open-source, first-principles, multi-agent research
sensemaking system. It turns papers into structured **knowledge atoms**, STEMd
analysis, ontology mappings, evidence appraisals, knowledge graphs, gaps,
contradictions, and responsible discovery directions.

AtlasX does not treat a paper as the smallest unit of knowledge. The smallest
unit is the fundamental **claim, mechanism, variable, question, or evidence
unit**. Papers connect when they touch the same underlying mechanism, variable,
condition, evidence type, or unanswered question — not merely because they share
a keyword.

AtlasX does not replace reading or peer review. It helps users see the structure
of a research field.

## Key commands

```bash
# Install (with dev + optional PDF support)
pip install -e ".[dev,pdf]"

# Run the full pipeline offline (no API key)
atlasx run --project examples/sample_project --provider offline

# Regenerate graph / reports from existing extractions
atlasx graph  --project examples/sample_project
atlasx report --project examples/sample_project

# Create a new project scaffold
atlasx init --project my_research_project
```

Providers: `offline` (deterministic, default), `local` (OpenAI-compatible
endpoints), `openai`, and `anthropic` (optional — see
[docs/claude/anthropic_api_provider.md](docs/claude/anthropic_api_provider.md)).

## Testing

```bash
pytest
```

Tests must not require an Anthropic or OpenAI API key. The offline provider and
mocked provider tests cover the pipeline without network access.

## Coding conventions

- Python 3.11+, type hints on public functions, docstrings, small functions.
- Pydantic v2 for validation, Typer for the CLI, Rich for output.
- Preserve the existing Codex architecture: agent prompts in `prompts/agents/`,
  agent classes in `src/atlasx/agents/`, schemas in `schemas/`.
- Add Claude-specific material under `.claude/` and `docs/claude/`; do not
  duplicate the generic material unnecessarily — cross-link instead.

## Safety and integrity rules (load-bearing)

- **Never invent source details.** If a value cannot be extracted, write
  `"unknown"` or `"not reported"` — never a plausible-looking DOI, page number,
  author, journal, statistic, or finding.
- **Separate paper claims from model inference.** Every output must distinguish
  what the source directly says from what an agent inferred.
- **Preserve uncertainty.** Do not turn weak evidence into strong evidence.
- **Preserve source provenance.** Every extraction carries a source trace (file
  path, chunk reference, DOI, or citation).
- **Never commit copyrighted PDFs or full article text.** Users may process
  lawful local copies; the repo stores only metadata and extracted knowledge
  atoms with proper citation. `*.pdf`, `*.docx`, `*.epub` are gitignored.
- **Human review required.** AtlasX outputs are research-support artifacts, not
  final scientific claims, medical advice, legal advice, or automated editorial
  decisions.
- **Never expose API keys.** `.env` is gitignored; only `.env.example` is
  committed.

Modular rules live in [.claude/rules/](.claude/rules/). Claude-specific behavior
is in [.claude/CLAUDE.md](.claude/CLAUDE.md). The Discovery Layer agent team is
in [.claude/agents/](.claude/agents/); reusable workflows are in
[.claude/skills/](.claude/skills/).
