# Claude support for AtlasX Discovery Layer

This directory documents how to use AtlasX with **Claude Code** and, optionally,
the **Anthropic API provider**.

AtlasX does not replace reading or peer review. It helps users see the structure
of a research field. It does not ask only, "What papers match this keyword?" It
asks, "What fundamental questions has this body of literature answered, what
remains unknown, and what should be investigated next?"

Claude Code users can use this repository as a codebase, a prompt library, a
subagent library, and a research workflow template.

## What the Claude layer adds

- **Project memory** — [`CLAUDE.md`](../../CLAUDE.md) and
  [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md) tell Claude Code how to behave
  in this repo.
- **Rules** — modular integrity constraints in
  [`.claude/rules/`](../../.claude/rules/).
- **Subagents** — a Discovery Layer agent team in
  [`.claude/agents/`](../../.claude/agents/).
- **Skills** — reusable workflows in [`.claude/skills/`](../../.claude/skills/).
- **Anthropic provider** — an optional Claude-backed provider for the Python CLI.

## Read next

- [claude_code_quickstart.md](claude_code_quickstart.md) — clone, install, run.
- [claude_subagent_team.md](claude_subagent_team.md) — the agent team and life cycle.
- [claude_skills_workflows.md](claude_skills_workflows.md) — each skill and when to use it.
- [claude_memory_and_rules.md](claude_memory_and_rules.md) — memory files and rules.
- [anthropic_api_provider.md](anthropic_api_provider.md) — using Claude in the CLI.
- [safe_research_workflows_with_claude.md](safe_research_workflows_with_claude.md) — lawful, safe use.

## The one rule that matters most

AtlasX outputs are research-support artifacts, not final scientific claims,
medical advice, legal advice, or automated editorial decisions. **Human review
is required.**
