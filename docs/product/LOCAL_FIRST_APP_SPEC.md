# Local-First App Spec

The future AtlasX Discovery Notebook app should wrap the CLI, not replace it.
The Python CLI remains the engine for source loading, routing, extraction,
graphing, reporting, and audit output.

## Desktop Stack

Tauri is preferred for the desktop app because it can provide a small,
local-first wrapper around the CLI. Electron is acceptable if the product needs
broader JavaScript ecosystem support.

## Engine

- Local Python CLI package.
- Existing AtlasX agents.
- Existing provider system.
- Offline deterministic mode.
- Local LLM mode.
- Optional OpenAI and Anthropic providers.

## Local Model Support

The app should expose local LLM configuration for OpenAI-compatible endpoints:

- Ollama.
- LM Studio.
- vLLM.
- LocalAI.

## Storage

Start with workspace folders. Later, add SQLite for notebook metadata.

Optional vector stores may be evaluated later:

- sqlite-vec.
- Chroma.
- LanceDB.
- Similar local-first stores.

No vector store should become mandatory for the base CLI.

## Local-First Rules

- No required cloud upload.
- Source documents stay on the user's machine.
- The UI writes notebook/project manifests.
- The UI invokes CLI commands.
- The UI reads stable JSON, CSV, and Markdown outputs.
- The UI clearly shows which provider was used.
- The UI warns when a cloud provider is selected.
- Human review messages remain visible.

