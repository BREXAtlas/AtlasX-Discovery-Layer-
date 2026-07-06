"""Project document loading."""

from __future__ import annotations

from pathlib import Path

from atlasx.config import ProjectConfig
from atlasx.io.manifest_loader import load_source_manifest
from atlasx.io.pdf_loader import load_pdf_text
from atlasx.io.text_loader import load_text_file
from atlasx.models.paper import PaperDocument, PaperMetadata, PaperTextChunk
from atlasx.utils.hashing import slugify, stable_id

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def load_project_documents(config: ProjectConfig) -> list[PaperDocument]:
    """Load all manifest sources into paper documents."""

    manifest_records = load_source_manifest(config.manifest_path)
    metadata_records = manifest_records or _infer_metadata_from_papers(config.papers_dir)
    documents: list[PaperDocument] = []
    for metadata in metadata_records:
        path = _resolve_source_path(config.project_dir, config.papers_dir, metadata.file_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Source file for {metadata.paper_id!r} does not exist: {path}"
            )
        text = _load_source_text(path)
        chunks = chunk_text(metadata.paper_id, text, source_name=path.name)
        documents.append(PaperDocument(metadata=metadata, text=text, chunks=chunks))
    return documents


def chunk_text(
    paper_id: str,
    text: str,
    source_name: str,
    max_chars: int = 3500,
) -> list[PaperTextChunk]:
    """Chunk text while preserving source trace labels."""

    clean = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if not clean:
        clean = "not reported"
    chunks: list[PaperTextChunk] = []
    start = 0
    chunk_index = 1
    while start < len(clean):
        end = min(start + max_chars, len(clean))
        if end < len(clean):
            newline = clean.rfind("\n\n", start, end)
            if newline > start + 500:
                end = newline
        chunk_text_value = clean[start:end].strip()
        chunk_id = f"{paper_id}_chunk_{chunk_index:03d}"
        chunks.append(
            PaperTextChunk(
                paper_id=paper_id,
                chunk_id=chunk_id,
                text=chunk_text_value,
                source_trace=f"{source_name}; chunk {chunk_index}",
                section="unknown",
            )
        )
        start = end
        chunk_index += 1
    return chunks


def _infer_metadata_from_papers(papers_dir: Path) -> list[PaperMetadata]:
    if not papers_dir.exists():
        raise FileNotFoundError(f"Papers directory does not exist: {papers_dir}")
    records: list[PaperMetadata] = []
    for index, path in enumerate(sorted(papers_dir.iterdir()), start=1):
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        paper_id = slugify(path.stem, fallback=f"paper_{index:03d}")
        records.append(
            PaperMetadata(
                paper_id=paper_id,
                title=path.stem.replace("_", " ").title(),
                file=path.name,
                source_type=path.suffix.lower().lstrip("."),
                license_status="user-provided",
            )
        )
    if not records:
        raise ValueError(f"No supported paper files found in {papers_dir}")
    return records


def _resolve_source_path(project_dir: Path, papers_dir: Path, file_path: Path) -> Path:
    if file_path.is_absolute():
        return file_path
    direct = project_dir / file_path
    if direct.exists():
        return direct
    return papers_dir / file_path


def _load_source_text(path: Path) -> str:
    extension = path.suffix.lower()
    if extension in {".txt", ".md"}:
        return load_text_file(path)
    if extension == ".pdf":
        return load_pdf_text(path)
    raise ValueError(f"Unsupported source file extension for {path}")


def create_minimal_project(project_dir: Path) -> None:
    """Create a minimal AtlasX project in a target directory."""

    papers_dir = project_dir / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    _write_if_missing(
        project_dir / "atlasx.yaml",
        "project:\n"
        f"  name: {project_dir.name}\n"
        "  default_provider: offline\n\n"
        "input:\n"
        "  papers_dir: papers\n"
        "  manifest: source_manifest.yaml\n\n"
        "output:\n"
        "  outputs_dir: outputs\n\n"
        "runtime:\n"
        "  preserve_uncertainty: true\n"
        "  require_source_trace: true\n"
        "  human_review_required: true\n",
    )
    _write_if_missing(
        project_dir / "source_manifest.yaml",
        "project:\n"
        f"  name: {project_dir.name}\n"
        "sources:\n"
        "  - paper_id: example_001\n"
        "    title: Example Paper Title\n"
        "    authors: [Example Author]\n"
        "    year: 2026\n"
        "    journal: Example Journal\n"
        "    doi: null\n"
        "    source_type: user-provided text\n"
        "    file: example_001.txt\n"
        "    tags: [demo]\n"
        "    license_status: user-provided\n",
    )
    _write_if_missing(
        papers_dir / "example_001.txt",
        "Fictional demo source. Replace this file with lawful source text, "
        "abstracts, or notes. AtlasX will preserve uncertainty when information "
        "is not reported.\n",
    )


def _write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")
