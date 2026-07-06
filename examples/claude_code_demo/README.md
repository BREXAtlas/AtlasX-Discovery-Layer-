# Claude Code demo project

A tiny, **fictional** demo project for the AtlasX Claude Code workflow. The two
sources under `papers/` are fictional, public-domain-style demo texts, clearly
marked as fictional. They contain **no copyrighted article text**.

The two demo papers are designed to connect at the level of a shared
**membrane-voltage mechanism** — one studies frequency exposure, the other
direct voltage perturbation — so the connection reasoner has something meaningful
(not keyword-based) to find.

## Run it offline

```bash
atlasx run    --project examples/claude_code_demo --provider offline
atlasx graph  --project examples/claude_code_demo
atlasx report --project examples/claude_code_demo
```

Outputs are written to `examples/claude_code_demo/outputs/` (gitignored).

## Or ask the Claude agent team

In Claude Code:

> Use the AtlasX Claude agent team to process `examples/claude_code_demo` in
> offline mode. Then show:
>
> 1. extracted knowledge atoms
> 2. STEMd analysis
> 3. graph nodes and edges
> 4. research gaps
> 5. bias/ethics review

## Reminder

These files are fictional demonstrations only. AtlasX outputs are
research-support artifacts and require human review. Never place real
copyrighted PDFs or article text in this folder.
