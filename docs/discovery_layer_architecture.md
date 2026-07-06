# Discovery Layer Architecture

AtlasX is organized around a multi-agent pipeline. Each agent has a Markdown
prompt and a Python class. The prompts can be reused in another AI tool, while
the Python classes provide a working local pipeline.

## Pipeline

1. Intake loads source metadata and files.
2. Source integrity checks provenance, missing fields, duplicates, and access
   warnings.
3. Text preparation turns source files into traceable chunks.
4. First-principles extraction converts chunks into knowledge atoms.
5. STEMd analysis reframes atoms through Specificity, Translatability, Evidence,
   Mechanism/Systems, and Discovery Direction.
6. Ontology mapping identifies concepts, synonyms, related terms, and
   uncertainty.
7. Evidence appraisal records evidence type, limitations, and overclaiming risk.
8. Connection reasoning links papers through underlying variables, mechanisms,
   conditions, outcomes, and gaps.
9. Gap and contradiction detection records missing variables and unresolved
   evidence.
10. Discovery direction generation creates responsible next-step possibilities.
11. Visualization and reporting writes JSON, CSV, and Markdown artifacts.
12. Bias and ethics review flags bias, access, citation, and attribution risks.

## Providers

AtlasX supports three provider modes:

- `offline`: deterministic demo output, no API key.
- `local`: OpenAI-compatible local endpoint such as Ollama, LM Studio, vLLM, or
  LocalAI.
- `openai`: OpenAI Python SDK with `OPENAI_API_KEY`.

## Design Rules

- Preserve source traces for every generated claim.
- Use `unknown` or `not reported` rather than inventing missing details.
- Distinguish direct source statements from agent inference.
- Mark outputs as requiring human review.
- Keep private PDFs and licensed content outside public Git.

