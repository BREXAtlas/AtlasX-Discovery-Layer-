#!/usr/bin/env python3
"""Public-safety scan for the AtlasX repository.

Checks that no secrets, PDFs, copyrighted source files, generated outputs, or
obvious secret patterns are present before a public release. Intended to be run
before committing, pushing, or publishing:

    python scripts/claude/check_public_safety.py

Exits non-zero if any high-severity issue is found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Directories we never scan into.
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "outputs",
    "dist",
    "build",
}

# File extensions that must never be committed.
FORBIDDEN_EXTS = {".pdf", ".docx", ".epub"}

# Only these files may look like a .env file.
ALLOWED_ENV_NAMES = {".env.example"}

LARGE_FILE_BYTES = 5_000_000  # flag large files that may be copyrighted sources

# Obvious secret patterns. Kept deliberately conservative.
SECRET_PATTERNS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"), "Anthropic-style API key"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI-style API key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
]
API_KEY_ASSIGNMENT_PATTERN = re.compile(
    r"(?:ANTHROPIC|OPENAI)_API_KEY\s*=\s*['\"]?(?P<value>[^'\"\s`]+)['\"]?"
)
PLACEHOLDER_SECRET_VALUES = {
    "",
    "your_key_here",
    "your_anthropic_key_here",
    "your_openai_key_here",
    "example",
    "placeholder",
    "null",
    "none",
}

TEXT_EXTS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".cfg",
    ".ini",
    ".sh",
    ".env",
    "",
}


def _iter_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        if any(part.endswith(".egg-info") for part in path.relative_to(REPO_ROOT).parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def main() -> int:
    high: list[str] = []
    warn: list[str] = []

    for path in _iter_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        name = path.name
        ext = path.suffix.lower()

        # .env files (only .env.example is allowed).
        if (name == ".env" or name.startswith(".env.")) and name not in ALLOWED_ENV_NAMES:
            high.append(f"env file present: {rel}")

        # Forbidden binary/document types.
        if ext in FORBIDDEN_EXTS:
            high.append(f"forbidden file type ({ext}): {rel}")

        # Local Claude settings should not be committed.
        if rel == ".claude/settings.local.json":
            high.append(f"local settings present: {rel}")

        # Generated outputs accidentally left in place.
        parts = path.relative_to(REPO_ROOT).parts
        if "outputs" in parts:
            warn.append(f"generated output present (should be gitignored): {rel}")

        # Large files that may be copyrighted sources.
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        if size > LARGE_FILE_BYTES:
            warn.append(f"large file ({size} bytes) may be a copyrighted source: {rel}")

        # Secret pattern scan for reasonably sized text files.
        if ext in TEXT_EXTS and size <= LARGE_FILE_BYTES and name not in ALLOWED_ENV_NAMES:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(content):
                    high.append(f"possible {label} in {rel}")
                    break
            for match in API_KEY_ASSIGNMENT_PATTERN.finditer(content):
                value = match.group("value").strip()
                if value.lower() not in PLACEHOLDER_SECRET_VALUES:
                    high.append(f"possible populated API key var in {rel}")
                    break

    print("AtlasX public-safety scan")
    print(f"  scanned root: {REPO_ROOT}")

    if warn:
        print("\nWarnings:")
        for item in warn:
            print(f"  - {item}")

    if high:
        print("\nHigh-severity issues (do not publish until resolved):")
        for item in high:
            print(f"  - {item}")
        print("\nRESULT: FAIL")
        return 1

    print("\nRESULT: PASS — no high-severity issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
