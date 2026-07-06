# Claude memory and rules

Claude Code reads project memory and rules automatically when you open this
repository. This document explains what each file does.

## Root `CLAUDE.md`

[`CLAUDE.md`](../../CLAUDE.md) at the repository root is the primary project
memory. It is concise and states the project purpose, key commands, coding
conventions, testing commands, and the load-bearing safety and provenance rules.
Claude Code loads it on startup.

If an `AGENTS.md` is later added for public multi-agent compatibility, import it
at the top of `CLAUDE.md` with `@AGENTS.md` and keep the Claude-specific
instructions below it. There is no `AGENTS.md` today, so none is imported.

## `.claude/CLAUDE.md`

[`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) holds Claude-specific behavior:
prefer plan-first changes for architecture or provider updates, always run tests
after code changes, never run destructive shell commands without confirmation,
never expose API keys, never add copyrighted full text, and keep docs accessible
to nontechnical research users.

## `.claude/rules/`

Modular integrity constraints, each in its own file:

| Rule | Focus |
| --- | --- |
| `atlasx-research-integrity.md` | Evidence, uncertainty, no overclaiming. |
| `atlasx-source-provenance.md` | Source traces: DOI, citation, file path, chunk reference. |
| `atlasx-python-quality.md` | Python 3.11+, type hints, docstrings, Pydantic, Typer, Rich. |
| `atlasx-paywall-copyright.md` | Lawful local copies only; no PDFs or full text committed. |
| `atlasx-no-hallucination.md` | If unknown, say unknown; never invent detail. |
| `atlasx-human-review.md` | Outputs are research support, not final decisions. |

## Local, uncommitted settings

- `CLAUDE.local.md` — your personal, uncommitted notes (gitignored).
- `.claude/settings.local.json` — local Claude Code settings (gitignored).

Copy `.claude/settings.example.json` to `.claude/settings.local.json` if you
want local Claude Code settings. Do not commit `settings.local.json`. JSON has no
comments, so any explanation of the settings lives here in the docs.
