# AtlasX Discovery Notebook

AtlasX Discovery Notebook is the future local-first app layer for AtlasX
Discovery Layer. The current repository provides the CLI engine that processes
user-owned sources locally, routes them by source type, extracts knowledge atoms
or source atoms, and writes app-ready outputs for reports, graphs, evidence
maps, gaps, contradictions, and future notebook interfaces.

## Product Concept

AtlasX Discovery Notebook is an open-source, local-first AI notebook and
discovery layer. It helps users process scholarly papers, general documents,
PDFs, Markdown files, text files, reports, essays, policy documents,
educational material, transcripts, and future source types.

Notebook-style tools help users talk to their sources. AtlasX Discovery
Notebook should help users own, inspect, extend, and reason over their sources
locally.

## Current State

The repository is CLI-first. The CLI is the processing engine. The desktop and
mobile apps come later as wrappers around the CLI and its stable output files.

Current outputs include:

- Knowledge atoms.
- Source atoms.
- Evidence maps.
- Concept maps.
- Gap maps.
- Contradiction maps.
- Discovery reports.
- Study-guide-ready notes.
- App-readable JSON, CSV, and Markdown outputs.

## Product Modes

### Research Mode

Research Mode uses the existing AtlasX research discovery pipeline. It is best
for scholarly papers, literature reviews, research reports, scientific articles,
and academic PDFs.

Outputs include knowledge atoms, evidence appraisals, ontology mappings, gaps,
contradictions, and discovery directions.

### General Notebook Mode

General Notebook Mode uses `SourceAtom`. It is best for ordinary PDFs, articles,
essays, reports, notes, and transcripts.

Outputs include summaries, key ideas, claims, evidence or examples, open
questions, action items, study notes, and user takeaways.

### Learning Mode

Learning Mode is a route now and can become a specialized agent later. It is
best for lessons, textbook chapters, curriculum, and study material.

Future outputs may include study guides, quizzes, flashcards, learning
objectives, and simplified explanations.

### Strategic Brief Mode

Strategic Brief Mode is a route now and can become a specialized agent later.
It is best for policy documents, business reports, proposals, and organizational
documents.

Future outputs may include stakeholders, risks, decisions, recommendations, and
implementation steps.

### Source Collection Mode

Source Collection Mode is reserved for bundled notebooks, database exports, or
future multi-source workspace manifests.

## Local-First Commitments

- No required cloud upload.
- Source documents stay on the user's machine.
- Cloud providers are optional.
- Local models are supported through Ollama, LM Studio, vLLM, LocalAI, and other
  OpenAI-compatible endpoints.
- Human review is required.
- AtlasX does not replace peer review, expert judgment, or source reading.

## Future Output Types

The app layer may later add cited chat answers, audio overview script
generation, flashcard generation, study guide generation, literature review
builders, concept map views, source comparison views, contradiction dashboards,
and research gap dashboards.

