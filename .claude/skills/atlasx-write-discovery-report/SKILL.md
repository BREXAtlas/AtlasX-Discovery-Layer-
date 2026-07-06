---
name: atlasx-write-discovery-report
description: Generate or explain AtlasX discovery reports and executive summaries from existing extractions, preserving uncertainty and provenance. Use when a user wants a readable report of a project's findings, gaps, and directions.
---

# Skill: atlasx-write-discovery-report

Invoke this skill by asking Claude Code to use the
`atlasx-write-discovery-report` skill, or by using the slash command if your
Claude Code version exposes project skills as slash commands.

## When to use

- The user wants a human-readable report of what a project contains.
- The user wants an executive summary for editors, students, or publishers.

## Steps

1. Ensure extractions exist (run discovery first if needed).
2. Generate reports:
   ```bash
   atlasx report --project <project_path>
   ```
3. For a richer narrative, delegate to `atlasx-visualization-reporter`, which can
   add gap tables, knowledge-graph summaries, and optional Mermaid diagrams.
4. Review the report so it: preserves uncertainty, distinguishes source claims
   from inference, carries source traces, and states the human-review
   requirement.

## Expected outputs

- `<project_path>/outputs/reports/discovery_report.md`
- `<project_path>/outputs/reports/executive_summary.md`

## Safety constraints

- Report only what the atoms support; never invent findings.
- Do not embed copyrighted full text; use citations and extracted atoms.
- Every report states that outputs are research-support artifacts requiring
  human review.

## Example

> Use the atlasx-write-discovery-report skill on `examples/sample_project` and
> give me an executive summary suitable for a nontechnical editor.
