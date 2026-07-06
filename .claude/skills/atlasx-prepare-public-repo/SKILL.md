---
name: atlasx-prepare-public-repo
description: Check that no secrets, PDFs, copyrighted article text, private notes, or generated outputs are staged before a public release of the AtlasX repository. Use before committing, pushing, or publishing.
---

# Skill: atlasx-prepare-public-repo

Invoke this skill by asking Claude Code to use the `atlasx-prepare-public-repo`
skill, or by using the slash command if your Claude Code version exposes project
skills as slash commands.

## When to use

- Before committing, pushing, or publishing the repository.
- Before sharing a project folder publicly.

## Steps

1. Run the public-safety scan if present:
   ```bash
   python scripts/claude/check_public_safety.py
   ```
2. Confirm `.gitignore` excludes: `.env` (and `.env.*` except `.env.example`),
   `CLAUDE.local.md`, `.claude/settings.local.json`, `outputs/`,
   `examples/**/outputs/`, `data/input/`, `data/output/`, `*.pdf`, `*.docx`,
   `*.epub`.
3. Confirm the committed Claude files are present and *not* ignored:
   `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, `.claude/agents/*.md`,
   `.claude/skills/**/SKILL.md`, `.claude/settings.example.json`.
4. Grep the staged changes for obvious secret patterns and copyrighted full
   text; stop and report if anything is found.

## Expected outputs

- A pass/fail report of what would be published, with any risky files listed.

## Safety constraints

- Never publish `.env`, API keys, PDFs, copyrighted article text, private notes,
  or generated outputs.
- If anything sensitive is staged, do not proceed — report and let the user
  decide.

## Example

> Use the atlasx-prepare-public-repo skill to check the repo is safe to push.
