"""Tests that the committed Claude Code project files exist and are well-formed.

These tests require neither Claude nor an Anthropic API key.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_AGENTS = [
    "atlasx-orchestrator",
    "atlasx-intake",
    "atlasx-source-integrity",
    "atlasx-text-preparation",
    "atlasx-first-principles-extractor",
    "atlasx-stemd-analyst",
    "atlasx-ontology-mapper",
    "atlasx-evidence-appraiser",
    "atlasx-connection-reasoner",
    "atlasx-gap-contradiction-detector",
    "atlasx-discovery-director",
    "atlasx-visualization-reporter",
    "atlasx-bias-ethics-reviewer",
    "atlasx-code-maintainer",
]

EXPECTED_RULES = [
    "atlasx-research-integrity",
    "atlasx-source-provenance",
    "atlasx-python-quality",
    "atlasx-paywall-copyright",
    "atlasx-no-hallucination",
    "atlasx-human-review",
]

EXPECTED_SKILLS = [
    "atlasx-setup-project",
    "atlasx-run-discovery",
    "atlasx-extract-knowledge-atoms",
    "atlasx-build-knowledge-graph",
    "atlasx-write-discovery-report",
    "atlasx-review-bias-ethics",
    "atlasx-prepare-public-repo",
]


def _parse_frontmatter(path: Path) -> dict:
    """Return the YAML frontmatter of a Markdown file as a dict."""

    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} is missing YAML frontmatter"
    end = text.index("\n---", 4)
    block = text[4:end]
    data = yaml.safe_load(block)
    assert isinstance(data, dict), f"{path} frontmatter did not parse to a mapping"
    return data


def test_memory_files_exist() -> None:
    assert (REPO_ROOT / "CLAUDE.md").is_file()
    assert (REPO_ROOT / ".claude" / "CLAUDE.md").is_file()


def test_rule_files_exist() -> None:
    for rule in EXPECTED_RULES:
        assert (REPO_ROOT / ".claude" / "rules" / f"{rule}.md").is_file(), rule


def test_subagents_have_required_frontmatter() -> None:
    agents_dir = REPO_ROOT / ".claude" / "agents"
    for agent in EXPECTED_AGENTS:
        path = agents_dir / f"{agent}.md"
        assert path.is_file(), agent
        data = _parse_frontmatter(path)
        assert data.get("name") == agent, f"{agent}: name mismatch ({data.get('name')})"
        assert data.get("description"), f"{agent}: missing description"


def test_skills_have_skill_md_with_frontmatter() -> None:
    skills_dir = REPO_ROOT / ".claude" / "skills"
    for skill in EXPECTED_SKILLS:
        path = skills_dir / skill / "SKILL.md"
        assert path.is_file(), skill
        data = _parse_frontmatter(path)
        assert data.get("name") == skill, f"{skill}: name mismatch ({data.get('name')})"
        assert data.get("description"), f"{skill}: missing description"


def test_settings_example_is_valid_json() -> None:
    path = REPO_ROOT / ".claude" / "settings.example.json"
    assert path.is_file()
    json.loads(path.read_text(encoding="utf-8"))


def test_gitignore_excludes_secrets_and_pdfs() -> None:
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in [".env", "*.pdf"]:
        assert pattern in gitignore, f".gitignore should exclude {pattern}"


def test_claude_docs_exist() -> None:
    docs_dir = REPO_ROOT / "docs" / "claude"
    for name in [
        "README.md",
        "claude_code_quickstart.md",
        "claude_subagent_team.md",
        "claude_skills_workflows.md",
        "claude_memory_and_rules.md",
        "anthropic_api_provider.md",
        "safe_research_workflows_with_claude.md",
    ]:
        assert (docs_dir / name).is_file(), name
