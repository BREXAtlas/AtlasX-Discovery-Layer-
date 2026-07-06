---
name: atlasx-review-bias-ethics
description: Run a bias and ethics review over AtlasX outputs before they inform any decision — checking for confirmation, citation, paywall, and prestige bias, overclaiming, missing source traces, and overreliance on AI. Use before outputs are used for editorial or research decisions.
---

# Skill: atlasx-review-bias-ethics

Invoke this skill by asking Claude Code to use the `atlasx-review-bias-ethics`
skill, or by using the slash command if your Claude Code version exposes project
skills as slash commands.

## When to use

- Before AtlasX outputs inform a decision (review topic, special issue, call for
  papers, replication, funding, editorial).
- Whenever a user asks whether the outputs are trustworthy enough to act on.

## Steps

1. Identify the outputs to review (atoms, STEMd, graph, gaps, directions,
   reports).
2. Delegate to the `atlasx-bias-ethics-reviewer` subagent to check for:
   confirmation, field-selection, citation, paywall/access, and prestige bias;
   overclaiming; missing source traces; author harm through poor attribution;
   overreliance on AI; and where expert review is required.
3. Produce a findings list by category with severity and a recommended remedy
   (correct, qualify, or withhold).
4. End with an explicit statement that expert review is required before any
   decision.

## Expected outputs

- A bias/ethics review report with categorized findings and remedies.

## Safety constraints

- The review constrains outputs; it does not add new claims.
- Prefer withholding unsupported output over shipping it with a buried
  disclaimer.
- Protect authors from unfair ranking or misattribution.

## Example

> Use the atlasx-review-bias-ethics skill on the outputs in
> `examples/sample_project/outputs` before I consider a special-issue topic.
