---
name: atlasx-setup-project
description: Scaffold a new AtlasX research project folder (papers/, source_manifest.yaml, notes/, outputs/) so a user can add lawfully supplied papers and run the Discovery Layer. Use when a user wants to start a new project or organize sources.
---

# Skill: atlasx-setup-project

Invoke this skill by asking Claude Code to use the `atlasx-setup-project` skill,
or by using the slash command if your Claude Code version exposes project skills
as slash commands.

## When to use

- The user is starting a new research project and needs a folder structure.
- The user has papers to analyze but no project to put them in.

## Target structure

```
my_project/
  papers/              # lawfully supplied .txt/.md (and, locally, .pdf) sources
  source_manifest.yaml # citation metadata: DOI, title, authors, year, journal, type, tags
  notes/               # human notes (kept local; do not commit private notes)
  outputs/             # generated artifacts (gitignored)
```

## Steps

1. Ask the user for a project path (default `my_research_project`).
2. Create the project scaffold. Prefer the CLI:
   ```bash
   atlasx init --project my_research_project
   ```
   If the CLI is unavailable, create the folders and files above by hand,
   including an empty `source_manifest.yaml` with commented example fields.
3. Explain how to add sources: place lawful text files in `papers/`, then fill
   in `source_manifest.yaml` with DOI, title, authors, year, journal, source
   type, and tags. Use `"unknown"` / `"not reported"` for any field not known.
4. Confirm `.gitignore` excludes `outputs/`, `*.pdf`, `*.docx`, `*.epub`, and
   `.env`.

## Expected outputs

- A project folder with `papers/`, `source_manifest.yaml`, `notes/`, `outputs/`.

## Safety constraints

- Never place copyrighted PDFs or full article text under version control.
- Never invent citation metadata; use `"unknown"` / `"not reported"`.
- Keep private notes local.

## Example

> Use the atlasx-setup-project skill to create a project at
> `projects/bioelectricity_review`, then tell me how to add my papers.
