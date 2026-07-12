"""Versioned data contracts and strict, dependency-free validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
PROVENANCE_FIELDS = {
    "source_id",
    "title",
    "source_url",
    "license",
    "checksum_sha256",
    "ingested_at",
    "permitted_use",
    "processed_path",
}


class ContractError(ValueError):
    """Raised when a versioned artifact violates its contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"Expected a JSON object in {path}")
    return value


def require_version(data: dict[str, Any], kind: str) -> None:
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ContractError(f"{kind} schema_version must be {SCHEMA_VERSION!r}")


def validate_manifest(data: dict[str, Any], root: Path, *, verify_checksum: bool = True) -> None:
    require_version(data, "manifest")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ContractError("manifest.sources must be a non-empty list")
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ContractError(f"sources[{index}] must be an object")
        missing = sorted(PROVENANCE_FIELDS - source.keys())
        if missing:
            raise ContractError(f"sources[{index}] missing provenance: {', '.join(missing)}")
        if not all(isinstance(source[field], str) and source[field].strip() for field in PROVENANCE_FIELDS):
            raise ContractError(f"sources[{index}] provenance fields must be non-empty strings")
        checksum = source["checksum_sha256"]
        if len(checksum) != 64 or any(char not in "0123456789abcdef" for char in checksum):
            raise ContractError(f"sources[{index}].checksum_sha256 is malformed")
        path = root / source["processed_path"]
        if verify_checksum and (not path.is_file() or sha256_file(path) != checksum):
            raise ContractError(f"source checksum mismatch or file missing: {path}")


def validate_corpus(data: dict[str, Any]) -> None:
    require_version(data, "corpus")
    chunks = data.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        raise ContractError("corpus.chunks must be a non-empty list")
    seen: set[str] = set()
    for chunk in chunks:
        required = {"chunk_id", "source_id", "text", "start_line", "end_line", "word_count"}
        if not isinstance(chunk, dict) or not required <= chunk.keys():
            raise ContractError("every chunk must contain the documented corpus fields")
        if chunk["chunk_id"] in seen or not chunk["text"].strip():
            raise ContractError("chunk IDs must be unique and text must be non-empty")
        seen.add(chunk["chunk_id"])


def validate_questions(data: dict[str, Any], chunk_ids: set[str] | None = None) -> None:
    require_version(data, "questions")
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ContractError("questions must be a non-empty list")
    ids: set[str] = set()
    splits: set[str] = set()
    for item in questions:
        required = {"question_id", "question", "split", "question_type", "relevance"}
        if not isinstance(item, dict) or not required <= item.keys():
            raise ContractError("question missing required fields")
        if item["question_id"] in ids or item["split"] not in {"dev", "test"}:
            raise ContractError("question IDs must be unique and split must be dev or test")
        if not isinstance(item["relevance"], dict) or not item["relevance"]:
            raise ContractError("each question needs graded relevance judgments")
        if chunk_ids is not None and not set(item["relevance"]) <= chunk_ids:
            raise ContractError(f"unknown chunk in relevance for {item['question_id']}")
        if any(grade not in {1, 2, 3} for grade in item["relevance"].values()):
            raise ContractError("relevance grades must be 1, 2, or 3")
        ids.add(item["question_id"])
        splits.add(item["split"])
    if splits != {"dev", "test"}:
        raise ContractError("dataset must contain both dev and held-out test splits")

