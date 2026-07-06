# AtlasX Prompts

Each prompt in this folder can be copied into another AI tool or used by the
Python orchestrator. Prompts are modular: the system prompts define global
behavior, and the agent prompts define one stage of the Discovery Layer.

## Use

1. Start with `system/atlasx_orchestrator.md`.
2. Add `system/governance_and_provenance.md`.
3. Run the agent prompts in numeric order.
4. Validate JSON outputs against files in `schemas/`.
5. Preserve source traces, uncertainty, and human review flags.

## Rules Shared by All Prompts

- Do not invent missing details.
- Use `unknown` or `not reported` when evidence is absent.
- Distinguish direct source statements from inference.
- Cite a source trace for every extracted claim.
- Do not use outputs as final medical, legal, editorial, or scientific advice.
- Require human review.

