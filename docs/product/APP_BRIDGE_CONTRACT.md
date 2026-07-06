# App Bridge Contract

The future AtlasX Discovery Notebook desktop/mobile app will call the CLI and
read stable outputs. The app should not replace the CLI engine.

## CLI Commands The App Can Call

```bash
atlasx init --project <workspace>
atlasx run --project <workspace> --provider offline
atlasx run --project <workspace> --provider local --model <model>
atlasx run --project <workspace> --route auto
atlasx graph --project <workspace>
atlasx report --project <workspace>
```

Cloud providers remain optional:

```bash
atlasx run --project <workspace> --provider openai --model <model>
atlasx run --project <workspace> --provider anthropic --model <model>
```

## App-Readable Outputs

- `outputs/notebook/source_routes.json`
- `outputs/notebook/source_atoms.json`
- `outputs/notebook/source_index.json`
- `outputs/notebook/notebook_summary.md`
- `outputs/reports/discovery_report.md`
- `outputs/reports/executive_summary.md`
- `outputs/graph/nodes.csv`
- `outputs/graph/edges.csv`
- `outputs/audit/agent_runs.jsonl`

## Future App Panels

- Source list.
- Chat/Q&A panel.
- Extracted atoms.
- Connections.
- Gaps and open questions.
- Evidence/source trace drawer.
- Reports.
- Exports.
- Settings for local model provider.

## Local-First Behavior

- The app should not upload files by default.
- The app should use local workspace paths.
- The app should show the provider used.
- The app should warn when a cloud provider is selected.
- The app should preserve human review messages.

## Notebook Workspace Format

A workspace should include:

```text
atlasx.yaml
source_manifest.yaml or notebook_manifest.yaml
sources/ or papers/
outputs/
  notebook/
  reports/
  graph/
  audit/
```

`papers/` remains supported as the legacy folder name. `sources/` is the broader
product concept for future notebook workspaces.

