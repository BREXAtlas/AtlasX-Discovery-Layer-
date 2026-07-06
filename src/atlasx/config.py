"""Project and runtime configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    """Resolved AtlasX project configuration."""

    project_dir: Path
    name: str
    papers_dir: Path
    manifest_path: Path
    outputs_dir: Path
    preserve_uncertainty: bool = True
    require_source_trace: bool = True
    human_review_required: bool = True
    raw: dict[str, Any] = Field(default_factory=dict)


def load_project_config(project_dir: Path) -> ProjectConfig:
    """Load project config with sensible defaults."""

    load_dotenv()
    project_dir = project_dir.resolve()
    config_path = project_dir / "atlasx.yaml"
    raw: dict[str, Any] = {}
    if config_path.exists():
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    project_section = raw.get("project", {})
    input_section = raw.get("input", {})
    output_section = raw.get("output", {})
    runtime_section = raw.get("runtime", {})

    papers_dir = project_dir / input_section.get("papers_dir", "papers")
    manifest_path = project_dir / input_section.get("manifest", "source_manifest.yaml")
    outputs_dir = project_dir / output_section.get("outputs_dir", "outputs")

    return ProjectConfig(
        project_dir=project_dir,
        name=project_section.get("name", project_dir.name),
        papers_dir=papers_dir,
        manifest_path=manifest_path,
        outputs_dir=outputs_dir,
        preserve_uncertainty=runtime_section.get("preserve_uncertainty", True),
        require_source_trace=runtime_section.get("require_source_trace", True),
        human_review_required=runtime_section.get("human_review_required", True),
        raw=raw,
    )

