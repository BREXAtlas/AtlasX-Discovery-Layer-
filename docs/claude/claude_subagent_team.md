# The Claude subagent team

The subagents in [`.claude/agents/`](../../.claude/agents/) mirror the research
data life cycle. Most research databases stop at storage, indexing, retrieval,
and presentation. AtlasX adds a post-publication sensemaking layer. In Claude
Code, that layer is a coordinated team of Claude subagents that follow the life
cycle.

## The life cycle

```
Source intake
  → source integrity
  → text preparation
  → first-principles extraction
  → STEMd analysis
  → ontology mapping
  → evidence appraisal
  → connection reasoning
  → gap/contradiction detection
  → discovery direction
  → reporting
  → bias/ethics review
```

## The agents

| Subagent | Role |
| --- | --- |
| `atlasx-orchestrator` | Coordinates the workflow; delegates rather than doing all extraction. |
| `atlasx-intake` | Identifies input files and source metadata (DOI, title, authors, year, journal, type, tags). |
| `atlasx-source-integrity` | Checks provenance, duplicates, copyright/paywall, traceability. |
| `atlasx-text-preparation` | Cleans and chunks sources; preserves page/section references without inventing them. |
| `atlasx-first-principles-extractor` | Breaks papers into knowledge atoms. |
| `atlasx-stemd-analyst` | Specificity, Translatability, Evidence, Mechanism/Systems, Discovery Direction. |
| `atlasx-ontology-mapper` | Maps inconsistent terms to shared concepts without collapsing distinctions. |
| `atlasx-evidence-appraiser` | Evidence type, sample size, replication, confidence, overclaiming risk. |
| `atlasx-connection-reasoner` | Connects atoms by mechanism/variable/condition/evidence, not keywords. |
| `atlasx-gap-contradiction-detector` | Finds gaps, conflicts, missing conditions, access barriers. |
| `atlasx-discovery-director` | Proposes responsible next steps with "do not overclaim" cautions. |
| `atlasx-visualization-reporter` | Writes JSON/CSV/Markdown/Mermaid artifacts. |
| `atlasx-bias-ethics-reviewer` | Reviews outputs for bias, overclaiming, missing provenance. |
| `atlasx-code-maintainer` | Maintains the Python package; makes no research claims. |

## How to invoke the team

Ask the orchestrator to run the pipeline, or name a specific agent:

> Use the AtlasX Claude agent team to process `examples/claude_code_demo` in
> offline mode. Then show:
> 1. extracted knowledge atoms
> 2. STEMd analysis
> 3. graph nodes and edges
> 4. research gaps
> 5. bias/ethics review

Every agent preserves uncertainty, distinguishes source claims from inference,
requires source traces, avoids hallucination, avoids replacing peer review,
warns on incomplete evidence, and never reproduces paywalled/copyrighted text.

## Cross-links to the Codex architecture

The subagents complement — they do not replace — the existing prompt files in
`prompts/agents/` and the Python agent classes in `src/atlasx/agents/`. Use the
subagents for interactive, Claude-native work and the Python pipeline for
reproducible batch runs.
