from pathlib import Path
from shutil import copytree, ignore_patterns

from atlasx.lifecycle import run_pipeline


def test_offline_pipeline_creates_expected_outputs_without_api_key(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    repo_root = Path(__file__).resolve().parents[1]
    source_project = repo_root / "examples" / "sample_project"
    project = tmp_path / "sample_project"
    copytree(source_project, project, ignore=ignore_patterns("outputs"))

    result = run_pipeline(project, provider_name="offline")

    assert result["papers"] == 2
    assert result["atoms"] >= 2
    assert (project / "outputs" / "extractions" / "toy_bioelectric_frequency_001.json").exists()
    assert (project / "outputs" / "graph" / "nodes.csv").exists()
    assert (project / "outputs" / "graph" / "edges.csv").exists()
    assert (project / "outputs" / "reports" / "discovery_report.md").exists()
    assert (project / "outputs" / "audit" / "agent_runs.jsonl").exists()

