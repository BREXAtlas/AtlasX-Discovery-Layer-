# Outputs and Visualizations

AtlasX writes structured outputs under each project's `outputs/` folder.

## JSON

- `outputs/extractions/{paper_id}.json`
- `outputs/stemd/{paper_id}_stemd.json`
- `outputs/extractions/ontology_concepts.json`
- `outputs/extractions/evidence_appraisals.json`
- `outputs/extractions/connections.json`
- `outputs/extractions/gaps.json`
- `outputs/extractions/discovery_directions.json`
- `outputs/extractions/bias_ethics_review.json`
- `outputs/audit/agent_runs.jsonl`

## CSV

- `outputs/graph/nodes.csv`
- `outputs/graph/edges.csv`

The graph schema supports papers, authors, journals, research questions,
entities, inputs, conditions, mechanisms, outcomes, evidence units, gaps,
discovery directions, concepts, and claims.

## Markdown

- `outputs/reports/discovery_report.md`
- `outputs/reports/executive_summary.md`

These reports are designed for human review. They can support research planning,
special issue scoping, calls for papers, replication planning, and synthesis,
but they are not final conclusions.

