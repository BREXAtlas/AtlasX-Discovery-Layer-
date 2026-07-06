# How To Use AtlasX Discovery Layer

Once the repo is installed, the Discovery Layer is activated by running the
pipeline on an AtlasX project folder. The basic trigger is:

```bash
atlasx run --project examples/sample_project --provider offline
```

That tells AtlasX:

> Take the papers and source manifest in this folder, run the agent pipeline,
> extract knowledge atoms, apply STEMd, build the graph, and generate reports.

AtlasX is not something you turn on in the background. You activate it by
pointing it at a project folder and running the pipeline.

## 1. Install AtlasX

```bash
git clone https://github.com/BREXAtlas/AtlasX-Discovery-Layer-.git
cd AtlasX-Discovery-Layer-
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
git clone https://github.com/BREXAtlas/AtlasX-Discovery-Layer-.git
cd AtlasX-Discovery-Layer-
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## 2. Test The Demo

Run the offline demo first. It needs no API key and proves the Discovery Layer
is working before connecting OpenAI, Claude, or a local LLM.

```bash
atlasx run --project examples/sample_project --provider offline
atlasx graph --project examples/sample_project
atlasx report --project examples/sample_project
```

That creates an `outputs/` folder inside the project:

```text
outputs/
  extractions/
  stemd/
  graph/
  reports/
  audit/
```

## 3. Main Commands

Create a named project folder:

```bash
atlasx init --project my_project
```

Run the Discovery Layer in offline demo mode:

```bash
atlasx run --project my_project --provider offline
```

Run with OpenAI:

```bash
atlasx run --project my_project --provider openai --model gpt-4.1-mini
```

Run with a local OpenAI-compatible LLM:

```bash
atlasx run --project my_project --provider local --model llama3.1
```

Run with Anthropic Claude:

```bash
atlasx run --project my_project --provider anthropic --model claude-opus-4-8
```

Use `atlasx graph` and `atlasx report` when you want to regenerate graph CSVs
or Markdown reports from existing extraction outputs:

```bash
atlasx graph --project my_project
atlasx report --project my_project
```

## 4. What Activates The Agents?

The agents are triggered by `atlasx run`.

The run command starts the orchestrator, then the orchestrator calls the agents
in order:

```text
Intake Agent
-> Source Integrity Agent
-> Text Preparation Agent
-> First-Principles Extraction Agent
-> STEMd Analysis Agent
-> Ontology Mapping Agent
-> Evidence Appraisal Agent
-> Connection Reasoning Agent
-> Gap + Contradiction Agent
-> Discovery Direction Agent
-> Visualization + Reporting Agent
-> Bias + Ethics Review Agent
```

## 5. What Goes Inside A Project Folder?

Example:

```text
my_project/
  papers/
    paper_001.txt
    paper_002.pdf
    article_notes.md
  source_manifest.yaml
  outputs/
```

Put lawful source text, abstracts, notes, or local files in `papers/`. Do not
commit copyrighted PDFs or licensed full text to a public repository.

The `source_manifest.yaml` tells AtlasX what the sources are:

```yaml
project:
  name: bioelectricity_test
sources:
  - paper_id: BIO-001
    title: "Bioelectricity, Moving On...."
    authors:
      - M. Levin
      - M. B. A. Djamgoz
    year: 2025
    journal: "Bioelectricity"
    doi: "10.1089/bioe.2025.0035"
    source_type: "user-provided notes"
    file: "levin_notes.txt"
    tags:
      - bioelectricity
    license_status: "user-provided notes; full article not committed"
```

Then run:

```bash
atlasx run --project my_project --provider openai --model gpt-4.1-mini
```

## 6. What Outputs Does AtlasX Create?

After running, you should get files like:

```text
outputs/extractions/BIO-001.json
outputs/stemd/BIO-001_stemd.json
outputs/graph/nodes.csv
outputs/graph/edges.csv
outputs/reports/discovery_report.md
outputs/reports/executive_summary.md
outputs/audit/agent_runs.jsonl
```

Those outputs are the Discovery Layer results: extracted knowledge atoms, STEMd
analysis, graph files, reports, and an audit trail.

## 7. Using AtlasX In Claude Code

Open the repo in Claude Code and ask:

```text
Use the atlasx-run-discovery skill to process examples/sample_project in offline
mode, then summarize the generated outputs.
```

Or:

```text
Use the AtlasX agent team to process my_project. Start with source integrity,
then first-principles extraction, STEMd analysis, graph building, and bias
review.
```

In Claude Code, the trigger is either the command-line pipeline:

```bash
atlasx run --project my_project --provider offline
```

or asking Claude to use one of the project skills or subagents under `.claude/`.

## 8. Three Ways To Use The Discovery Layer

**Command line:** run `atlasx run`.

**Claude Code:** ask Claude to use the AtlasX skills and subagents.

**Prompt library:** copy the agent prompts from `prompts/agents/` or
`.claude/agents/` into another AI tool.

Start with offline mode. Once that works, connect OpenAI, Claude, or a local LLM
only when you are ready.

