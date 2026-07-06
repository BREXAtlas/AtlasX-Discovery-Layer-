from pathlib import Path

from atlasx.io.manifest_loader import load_source_manifest


def test_manifest_loader_reads_sample_project() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = repo_root / "examples" / "sample_project" / "source_manifest.yaml"

    records = load_source_manifest(manifest)

    assert len(records) == 2
    assert records[0].paper_id == "toy_bioelectric_frequency_001"
    assert records[0].file == "sample_paper_001.txt"
    assert "bioelectricity" in records[0].tags


def test_manifest_loader_accepts_source_id_alias(tmp_path) -> None:
    manifest = tmp_path / "source_manifest.yaml"
    manifest.write_text(
        "sources:\n"
        "  - source_id: source_001\n"
        "    title: Example Source\n"
        "    file: example.txt\n",
        encoding="utf-8",
    )

    records = load_source_manifest(manifest)

    assert records[0].paper_id == "source_001"
