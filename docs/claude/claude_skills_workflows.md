# Claude skills and workflows

The skills in [`.claude/skills/`](../../.claude/skills/) are reusable workflows.
Invoke a skill by asking Claude Code to use it by name, or by using the slash
command if your Claude Code version exposes project skills as slash commands.

## The skills

| Skill | When to use |
| --- | --- |
| `atlasx-setup-project` | Start a new research project folder (`papers/`, `source_manifest.yaml`, `notes/`, `outputs/`). |
| `atlasx-run-discovery` | Run the full pipeline over a project (offline by default). |
| `atlasx-extract-knowledge-atoms` | Produce and validate first-principles knowledge atoms. |
| `atlasx-build-knowledge-graph` | Build or explain the knowledge graph (nodes and edges). |
| `atlasx-write-discovery-report` | Generate or explain discovery reports and executive summaries. |
| `atlasx-review-bias-ethics` | Review outputs for bias and ethics before any decision. |
| `atlasx-prepare-public-repo` | Check nothing sensitive is staged before a public release. |

## Typical sequence

```
atlasx-setup-project
  → atlasx-run-discovery
  → atlasx-extract-knowledge-atoms
  → atlasx-build-knowledge-graph
  → atlasx-write-discovery-report
  → atlasx-review-bias-ethics
  → atlasx-prepare-public-repo   (before publishing)
```

## Examples

```
Use the atlasx-setup-project skill to create a project at projects/my_review.
Use the atlasx-run-discovery skill to process examples/sample_project offline.
Use the atlasx-build-knowledge-graph skill and explain the strongest connections.
Use the atlasx-review-bias-ethics skill before I choose a special-issue topic.
```

Each skill documents its steps, commands, expected outputs, and safety
constraints in its own `SKILL.md`. Every skill preserves uncertainty and
provenance and ends by reminding you that outputs require human review.
