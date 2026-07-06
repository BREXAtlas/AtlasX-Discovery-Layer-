---
name: atlasx-build-knowledge-graph
description: Build or explain the AtlasX knowledge graph (nodes and edges) from existing extractions, connecting atoms by mechanism/variable/condition/evidence rather than keywords. Use when a user wants the graph or wants to inspect connections.
---

# Skill: atlasx-build-knowledge-graph

Invoke this skill by asking Claude Code to use the
`atlasx-build-knowledge-graph` skill, or by using the slash command if your
Claude Code version exposes project skills as slash commands.

## When to use

- The user wants a knowledge graph of nodes and edges.
- The user wants to inspect how sources connect.

## Steps

1. Ensure extractions exist (run discovery first if needed).
2. Build the graph:
   ```bash
   atlasx graph --project <project_path>
   ```
3. For connection quality, delegate to the `atlasx-connection-reasoner`
   subagent, which classifies each edge as shared mechanism / variable / method
   / outcome / gap / contradictory evidence / replication opportunity /
   translational pathway — never a bare keyword overlap.
4. Summarize the nodes and edges, and optionally produce a simple Mermaid
   diagram via `atlasx-visualization-reporter`.

## Expected outputs

- `<project_path>/outputs/graph/nodes.csv`
- `<project_path>/outputs/graph/edges.csv`
- Optional Markdown/Mermaid graph summary.

## Safety constraints

- Every edge must name the specific shared mechanism/variable/condition, with
  source traces for both endpoints.
- Do not assert connections that rest only on shared keywords.
- Preserve uncertainty; flag weak edges for human review.

## Example

> Use the atlasx-build-knowledge-graph skill on `examples/sample_project` and
> explain the strongest mechanism-level connections.
