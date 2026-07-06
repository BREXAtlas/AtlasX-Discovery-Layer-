# .claude/CLAUDE.md — Claude Code behavior in this repository

This file tunes how Claude Code should behave when working inside AtlasX. It
complements the concise root [CLAUDE.md](../CLAUDE.md) and the modular rules in
[rules/](rules/).

## How to work here

- **Prefer plan-first changes** for anything that touches architecture, the
  agent pipeline (`src/atlasx/`), the schemas (`schemas/`), or the provider
  layer (`src/atlasx/providers/`). Propose the plan, then implement.
- **Always run `pytest` after code changes.** Do not report success on code you
  have not tested. If tests fail, say so with the output.
- **Never run destructive shell commands without user confirmation** (no
  `rm -rf`, no force-push, no history rewrites, no bulk deletes).
- **Never expose or print API keys.** Read secrets from environment variables
  only. Never write a key into a committed file.
- **Never add full copyrighted article text to the repo.** Process lawful local
  copies from gitignored folders; commit only metadata and extracted knowledge
  atoms with citations.
- **Keep documentation accessible to nontechnical research users** — editors,
  students, publishers, and researchers, not only programmers.

## Research reasoning discipline

When Claude itself acts as part of the Discovery Layer (for example, when a user
asks Claude to process a project), Claude must:

- Break papers into first-principles knowledge atoms, not paper-level summaries.
- Distinguish direct source claims from inference in every output.
- Preserve uncertainty and require a source trace for every atom.
- Warn when evidence is incomplete; never overclaim.
- Never fetch or reproduce paywalled or copyrighted article text.
- Defer final judgment to human experts and peer review.

## The Claude-native Discovery Layer

Claude Code users can use this repository as a codebase, a prompt library, a
subagent library, and a research workflow template:

- **Subagents** ([agents/](agents/)) mirror the research data life cycle:
  source intake → source integrity → text preparation → first-principles
  extraction → STEMd analysis → ontology mapping → evidence appraisal →
  connection reasoning → gap/contradiction detection → discovery direction →
  reporting → bias/ethics review.
- **Skills** ([skills/](skills/)) are reusable workflows for setup, running
  discovery, extracting atoms, building the graph, writing reports, reviewing
  bias/ethics, and preparing the repo for public release.
- **Rules** ([rules/](rules/)) are modular integrity constraints that apply to
  every task.

## Local settings

Copy `.claude/settings.example.json` to `.claude/settings.local.json` if you
want local Claude Code settings. Do **not** commit `settings.local.json` — it is
gitignored.
