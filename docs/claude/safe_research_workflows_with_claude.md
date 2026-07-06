# Safe research workflows with Claude

AtlasX is designed for lawful, responsible sensemaking over published and
licensed sources. Modern research does not only suffer from lack of access. It
suffers from too much information, too little synthesis, inconsistent
terminology, too many disconnected concepts, and too much cognitive burden on
researchers. AtlasX helps — within clear safety limits.

## Do

- Process papers you can **lawfully access** (your own downloads, licensed
  copies, open-access articles).
- Keep source files in **local, gitignored folders** (`papers/`, `data/input/`,
  `outputs/`). `*.pdf`, `*.docx`, `*.epub` are gitignored.
- Preserve **DOI, citation, and source trace** for every extraction so a human
  can verify the original.
- Store **metadata and extracted knowledge atoms**, which are structured facts
  with provenance — not reproductions of the article.
- Run **offline mode first**; it is deterministic and needs no API key.

## Do not

- Do **not** commit PDFs or copyrighted article text to the repository.
- Do **not** paste, publish, or regenerate copyrighted full text.
- Do **not** use AtlasX to bypass paywalls or misuse licensed content — when
  evidence is inaccessible, record it as a gap.
- Do **not** treat AI output as final scientific proof.
- Do **not** expose API keys; read them from the environment only.

## Human review is required

AtlasX outputs are research-support artifacts, not final scientific claims,
medical advice, legal advice, or automated editorial decisions. Route outputs
through the `atlasx-review-bias-ethics` skill and then through domain experts and
peer review before any decision.

## Before publishing the repo

Use the `atlasx-prepare-public-repo` skill (or run
`python scripts/claude/check_public_safety.py`) to confirm no secrets, PDFs,
copyrighted text, private notes, or generated outputs are staged.
