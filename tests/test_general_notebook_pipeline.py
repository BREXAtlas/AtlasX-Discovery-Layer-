from pathlib import Path
from shutil import copytree, ignore_patterns

from atlasx.lifecycle import run_pipeline
from atlasx.utils.json_tools import read_json


def test_general_notebook_route_writes_app_ready_outputs(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    source_project = repo_root / "examples" / "general_notebook_project"
    project = tmp_path / "general_notebook_project"
    copytree(source_project, project, ignore=ignore_patterns("outputs"))

    result = run_pipeline(project, provider_name="offline", route="auto")

    assert result["route"] == "auto"
    assert result["source_atoms"] >= 1
    routes_path = project / "outputs" / "notebook" / "source_routes.json"
    atoms_path = project / "outputs" / "notebook" / "source_atoms.json"
    index_path = project / "outputs" / "notebook" / "source_index.json"
    summary_path = project / "outputs" / "notebook" / "notebook_summary.md"
    assert routes_path.exists()
    assert atoms_path.exists()
    assert index_path.exists()
    assert summary_path.exists()
    routes = read_json(routes_path)
    atoms = read_json(atoms_path)
    assert routes[0]["route"] == "general"
    assert atoms[0]["route"] == "general"

