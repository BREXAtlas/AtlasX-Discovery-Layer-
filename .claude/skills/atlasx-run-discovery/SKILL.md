---
name: atlasx-run-discovery
description: Run the full AtlasX Discovery Layer pipeline over a project (offline by default, or a provider the user selects) and summarize the generated outputs. Use when a user wants end-to-end processing of a project.
---

# Skill: atlasx-run-discovery

Invoke this skill by asking Claude Code to use the `atlasx-run-discovery` skill,
or by using the slash command if your Claude Code version exposes project skills
as slash commands.

## When to use

- The user wants to process a project into atoms, graph, and reports.
- The user asks to "run discovery" or "process this project".

## Steps

1. Confirm the project path and provider. Default to `offline` (deterministic,
   no API key). Providers: `offline`, `local`, `openai`, `anthropic`.
2. Run the pipeline:
   ```bash
   atlasx run --project <project_path> --provider offline
   ```
   For another provider, for example Anthropic:
   ```bash
   atlasx run --project <project_path> --provider anthropic --model $ANTHROPIC_MODEL
   ```
3. Regenerate graph and reports if needed:
   ```bash
   atlasx graph  --project <project_path>
   atlasx report --project <project_path>
   ```
4. Summarize what was produced (see Expected outputs), preserving uncertainty
   and noting that outputs require human review.

## Expected outputs

Under `<project_path>/outputs/`:
- `extractions/{paper_id}.json` — knowledge atoms
- `stemd/{paper_id}_stemd.json` — STEMd analysis
- `graph/nodes.csv`, `graph/edges.csv` — knowledge graph
- `reports/discovery_report.md`, `reports/executive_summary.md`
- `audit/agent_runs.jsonl` — run audit trail

## Safety constraints

- Prefer offline mode first; it needs no API key and no network.
- Never expose API keys; read them from the environment only.
- Do not commit outputs or copyrighted source text.
- Treat all outputs as research-support artifacts requiring human review.

## Example

> Use the atlasx-run-discovery skill to process `examples/sample_project` in
> offline mode, then summarize the generated outputs.
