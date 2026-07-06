"""Paper and text chunk models."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class PaperMetadata(BaseModel):
    """Citation and source metadata for one paper or source."""

    paper_id: str
    title: str = "unknown"
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    journal: str = "unknown"
    doi: str | None = None
    source_type: str = "unknown"
    file: str
    tags: list[str] = Field(default_factory=list)
    abstract: str | None = None
    notes: str | None = None
    license_status: str = "user-provided"

    @field_validator("paper_id", "file")
    @classmethod
    def required_text(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("paper_id and file are required")
        return value.strip()

    @field_validator("title", "journal", "source_type", mode="before")
    @classmethod
    def default_unknown(cls, value: str | None) -> str:
        if value is None or str(value).strip() == "":
            return "unknown"
        return str(value).strip()

    @property
    def file_path(self) -> Path:
        return Path(self.file)


class PaperTextChunk(BaseModel):
    """Traceable text segment used for extraction."""

    paper_id: str
    chunk_id: str
    text: str
    source_trace: str
    section: str = "unknown"
    page: int | None = None


class PaperDocument(BaseModel):
    """Loaded paper text plus metadata."""

    metadata: PaperMetadata
    text: str
    chunks: list[PaperTextChunk] = Field(default_factory=list)

    @property
    def paper_id(self) -> str:
        return self.metadata.paper_id

