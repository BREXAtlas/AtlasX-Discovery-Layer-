---
name: atlasx-extract-knowledge-atoms
description: Guide first-principles extraction of knowledge atoms from a project's sources and validate them against the knowledge_atom schema. Use when a user wants atoms specifically, or wants to check extraction quality.
---

# Skill: atlasx-extract-knowledge-atoms

Invoke this skill by asking Claude Code to use the
`atlasx-extract-knowledge-atoms` skill, or by using the slash command if your
Claude Code version exposes project skills as slash commands.

## When to use

- The user wants knowledge atoms (not the whole pipeline).
- The user wants to review or validate extraction output.

## Steps

1. Identify the project and its prepared sources/chunks.
2. Delegate extraction to the `atlasx-first-principles-extractor` subagent, which
   breaks each source into atoms: paper/field/discovery questions, entities,
   inputs, conditions, mechanisms, outcomes, evidence units, boundaries,
   assumptions, gaps, connection candidates, and next steps.
3. Validate atoms against `schemas/knowledge_atom.schema.json`. Confirm each atom
   has a `source_trace`, distinguishes source claim from inference, and carries a
   confidence and `human_review_required` flag.
4. Report any atoms that fail validation or lack provenance.

## Relevant commands

Atoms are produced by the pipeline and written to
`<project_path>/outputs/extractions/{paper_id}.json`:
```bash
atlasx run --project <project_path> --provider offline
```

## Expected outputs

- Schema-valid knowledge atoms with source traces, or a list of validation
  failures to fix.

## Safety constraints

- Use `"unknown"` / `"not reported"` — never invent detail.
- Every atom must be traceable to a source.
- Do not reproduce copyrighted full text; work from lawfully supplied material.

## Example

> Use the atlasx-extract-knowledge-atoms skill on `examples/sample_project` and
> show me atoms that lack a source trace or fail schema validation.
