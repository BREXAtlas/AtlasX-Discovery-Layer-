"""General source models for notebook-style projects."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


def _unknown(value: object) -> str:
    if value is None:
        return "unknown"
    text = str(value).strip()
    return text if text else "unknown"


class SourceMetadata(BaseModel):
    """Metadata for any user-provided source document."""

    source_id: str
    title: str = "unknown"
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    source_type: str = "unknown"
    file: str
    tags: list[str] = Field(default_factory=list)
    abstract: str | None = None
    notes: str | None = None
    license_status: str = "user-provided"
    doi: str | None = None
    journal: str = "unknown"
    url: str | None = None
    route_hint: str | None = None

    @field_validator("source_id", "file")
    @classmethod
    def required_text(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("source_id and file are required")
        return value.strip()

    @field_validator("title", "source_type", "journal", mode="before")
    @classmethod
    def preserve_unknowns(cls, value: object) -> str:
        return _unknown(value)

    @property
    def file_path(self) -> Path:
        return Path(self.file)


class SourceTextChunk(BaseModel):
    """Traceable text chunk for a general source."""

    source_id: str
    chunk_id: str
    text: str
    source_trace: str
    section: str = "unknown"
    page: int | None = None


class SourceDocument(BaseModel):
    """Loaded source text plus metadata and chunks."""

    metadata: SourceMetadata
    text: str
    chunks: list[SourceTextChunk] = Field(default_factory=list)

    @property
    def source_id(self) -> str:
        return self.metadata.source_id

