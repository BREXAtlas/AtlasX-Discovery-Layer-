#!/usr/bin/env bash
# Run the AtlasX Claude Code demo project offline (no API key required).
#
# Usage:
#   bash scripts/claude/run_claude_demo.sh
#
# Runs the full pipeline over examples/claude_code_demo in offline mode, then
# regenerates the graph and reports. Outputs land in
# examples/claude_code_demo/outputs/ (gitignored).

set -euo pipefail

PROJECT="examples/claude_code_demo"

echo "==> Running AtlasX offline pipeline on ${PROJECT}"
atlasx run --project "${PROJECT}" --provider offline

echo "==> Regenerating knowledge graph"
atlasx graph --project "${PROJECT}"

echo "==> Regenerating reports"
atlasx report --project "${PROJECT}"

echo "==> Done. See ${PROJECT}/outputs/"
echo "    Remember: outputs are research-support artifacts and require human review."
