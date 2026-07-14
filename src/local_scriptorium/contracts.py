"""Versioned data contracts and strict, dependency-free validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
SOURCE_REGISTER_SCHEMA_VERSION = "2.0"
QUESTION_SCHEMA_VERSION = "2.0"
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


def validate_source_register(
    data: dict[str, Any],
    root: Path | None = None,
    *,
    verify_checksums: bool = False,
) -> None:
    """Validate the v2 planned/public source register."""
    if data.get("schema_version") != SOURCE_REGISTER_SCHEMA_VERSION:
        raise ContractError(
            f"source register schema_version must be {SOURCE_REGISTER_SCHEMA_VERSION!r}"
        )
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ContractError("source register sources must be a non-empty list")

    seen: set[str] = set()
    allowed_statuses = {"approved", "private_only", "blocked"}
    required = {
        "source_id",
        "author",
        "work",
        "title",
        "translator",
        "edition_year",
        "source_urls",
        "status",
        "verification_state",
        "permitted_use",
        "allowed_content_kinds",
        "excluded_content_kinds",
        "processed_path",
        "raw_checksum_sha256",
        "normalized_checksum_sha256",
    }

    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ContractError(f"source register sources[{index}] must be an object")
        missing = sorted(required - source.keys())
        if missing:
            raise ContractError(
                f"source register sources[{index}] missing: {', '.join(missing)}"
            )

        source_id = source["source_id"]
        if not isinstance(source_id, str) or not source_id.strip():
            raise ContractError(f"source register sources[{index}] has an invalid source_id")
        if source_id in seen:
            raise ContractError(f"source register source IDs must be unique: {source_id}")
        seen.add(source_id)

        if not isinstance(source["edition_year"], int) or source["edition_year"] < 1:
            raise ContractError(f"source register edition_year is invalid: {source_id}")
        if source["status"] not in allowed_statuses:
            raise ContractError(f"source register status is invalid: {source_id}")
        if not isinstance(source["source_urls"], list) or not source["source_urls"]:
            raise ContractError(f"source register source_urls is empty: {source_id}")
        if not all(isinstance(url, str) and url.strip() for url in source["source_urls"]):
            raise ContractError(f"source register source_urls are invalid: {source_id}")

        for field in ("allowed_content_kinds", "excluded_content_kinds"):
            values = source[field]
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value.strip() for value in values
            ):
                raise ContractError(f"source register {field} is invalid: {source_id}")

        processed_path = source["processed_path"]
        if processed_path is not None:
            if not isinstance(processed_path, str) or not processed_path.strip():
                raise ContractError(f"source register processed_path is invalid: {source_id}")
            relative_path = Path(processed_path)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                raise ContractError(
                    f"source register processed_path must be portable: {source_id}"
                )
            if root is not None and verify_checksums:
                normalized_checksum = source["normalized_checksum_sha256"]
                if not isinstance(normalized_checksum, str) or len(normalized_checksum) != 64:
                    raise ContractError(
                        f"source register normalized checksum is missing: {source_id}"
                    )
                path = root / relative_path
                if not path.is_file() or sha256_file(path) != normalized_checksum:
                    raise ContractError(
                        f"source register normalized checksum mismatch: {source_id}"
                    )

        for field in ("raw_checksum_sha256", "normalized_checksum_sha256"):
            value = source[field]
            if value is not None and (
                not isinstance(value, str)
                or len(value) != 64
                or any(char not in "0123456789abcdef" for char in value)
            ):
                raise ContractError(f"source register checksum is malformed: {source_id}")

        if source["status"] == "blocked" and source["processed_path"] is not None:
            raise ContractError(f"blocked source cannot have a processed path: {source_id}")


def validate_pack(data: dict[str, Any], source_register: dict[str, Any]) -> None:
    """Validate an explicit corpus-pack selection against the source register."""
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ContractError(f"pack schema_version must be {SCHEMA_VERSION!r}")
    if data.get("register_id") != source_register.get("register_id"):
        raise ContractError("pack register_id does not match the source register")

    sources = {
        source["source_id"]: source
        for source in source_register.get("sources", [])
        if isinstance(source, dict) and isinstance(source.get("source_id"), str)
    }
    active = data.get("active_source_ids")
    blocked = data.get("blocked_source_ids")
    if not isinstance(active, list) or not active:
        raise ContractError("pack active_source_ids must be a non-empty list")
    if len(active) != len(set(active)):
        raise ContractError("pack active_source_ids must be unique")
    if not isinstance(blocked, list) or len(blocked) != len(set(blocked)):
        raise ContractError("pack blocked_source_ids must be a unique list")

    overlap = set(active) & set(blocked)
    if overlap:
        raise ContractError(f"pack source cannot be both active and blocked: {sorted(overlap)}")
    for source_id in active:
        source = sources.get(source_id)
        if source is None:
            raise ContractError(f"pack references unknown active source: {source_id}")
        if source.get("status") != "approved":
            raise ContractError(f"pack active source is not approved: {source_id}")
    for source_id in blocked:
        source = sources.get(source_id)
        if source is None:
            raise ContractError(f"pack references unknown blocked source: {source_id}")
        if source.get("status") != "blocked":
            raise ContractError(f"pack blocked source is not blocked in register: {source_id}")


def validate_questions_v2(
    data: dict[str, Any],
    passage_ids: set[str] | None = None,
) -> None:
    """Validate passage-anchored v2 benchmark questions."""
    if data.get("schema_version") != QUESTION_SCHEMA_VERSION:
        raise ContractError(f"questions schema_version must be {QUESTION_SCHEMA_VERSION!r}")
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ContractError("v2 questions must be a non-empty list")

    allowed_answerability = {"answerable", "unanswerable", "excluded_pending_adjudication"}
    allowed_types = {
        "single_passage_textual",
        "within_work_synthesis",
        "attribution_source_scope",
        "cross_author_comparison",
        "concept_tracing",
        "unanswerable",
    }
    seen_ids: set[str] = set()
    splits: set[str] = set()
    for item in questions:
        required = {
            "question_id",
            "family_id",
            "question",
            "split",
            "question_type",
            "risk_tags",
            "answerability",
            "canonical_passage_ids",
            "acceptable_evidence_sets",
            "curation_state",
        }
        if not isinstance(item, dict) or not required <= item.keys():
            raise ContractError("v2 question is missing required fields")
        question_id = item["question_id"]
        if not isinstance(question_id, str) or not question_id.strip() or question_id in seen_ids:
            raise ContractError("v2 question IDs must be unique non-empty strings")
        family_id = item["family_id"]
        if not isinstance(family_id, str) or not family_id.strip():
            raise ContractError(f"v2 question family is invalid: {question_id}")
        if item["split"] not in {"dev", "test"}:
            raise ContractError(f"v2 question split is invalid: {question_id}")
        if item["question_type"] not in allowed_types:
            raise ContractError(f"v2 question type is invalid: {question_id}")
        if item["answerability"] not in allowed_answerability:
            raise ContractError(f"v2 answerability is invalid: {question_id}")
        if not isinstance(item["question"], str) or not item["question"].strip():
            raise ContractError(f"v2 question text is empty: {question_id}")
        if not isinstance(item["risk_tags"], list) or not all(
            isinstance(tag, str) and tag.strip() for tag in item["risk_tags"]
        ):
            raise ContractError(f"v2 risk_tags are invalid: {question_id}")
        if not isinstance(item["canonical_passage_ids"], list) or not all(
            isinstance(passage_id, str) and passage_id.strip()
            for passage_id in item["canonical_passage_ids"]
        ):
            raise ContractError(f"v2 canonical passage IDs are invalid: {question_id}")
        if passage_ids is not None and not set(item["canonical_passage_ids"]) <= passage_ids:
            raise ContractError(f"v2 question references an unknown passage: {question_id}")

        evidence_sets = item["acceptable_evidence_sets"]
        if not isinstance(evidence_sets, list):
            raise ContractError(f"v2 acceptable evidence sets are invalid: {question_id}")
        if item["answerability"] == "answerable" and not evidence_sets:
            raise ContractError(f"answerable v2 question needs evidence: {question_id}")
        if item["answerability"] == "unanswerable" and evidence_sets:
            raise ContractError(f"unanswerable v2 question cannot have evidence: {question_id}")
        for evidence_set in evidence_sets:
            if not isinstance(evidence_set, dict) or not isinstance(
                evidence_set.get("required_groups"), list
            ):
                raise ContractError(f"v2 evidence set is malformed: {question_id}")
            groups = evidence_set["required_groups"]
            if not groups or any(
                not isinstance(group, list)
                or not group
                or not all(isinstance(passage_id, str) and passage_id.strip() for passage_id in group)
                for group in groups
            ):
                raise ContractError(f"v2 required evidence groups are malformed: {question_id}")
            group_ids = {passage_id for group in groups for passage_id in group}
            if passage_ids is not None and not group_ids <= passage_ids:
                raise ContractError(f"v2 evidence set references an unknown passage: {question_id}")
            if not group_ids <= set(item["canonical_passage_ids"]):
                raise ContractError(f"v2 evidence is not listed on the question: {question_id}")

        if item["curation_state"] not in {"candidate", "reviewed", "accepted", "excluded"}:
            raise ContractError(f"v2 curation_state is invalid: {question_id}")
        seen_ids.add(question_id)
        splits.add(item["split"])

    if splits != {"dev", "test"}:
        raise ContractError("v2 question dataset must contain dev and test splits")


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
        relative_path = Path(source["processed_path"])
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ContractError(f"sources[{index}].processed_path must be a portable relative path")
        path = root / relative_path
        if verify_checksum and (not path.is_file() or sha256_file(path) != checksum):
            raise ContractError(f"source checksum mismatch or file missing: {path}")


def validate_corpus(data: dict[str, Any]) -> None:
    if data.get("schema_version") not in {SCHEMA_VERSION, "v0.3-corpus-1.0"}:
        raise ContractError("corpus schema_version must be '1.0' or 'v0.3-corpus-1.0'")
    chunks = data.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        raise ContractError("corpus.chunks must be a non-empty list")
    seen: set[str] = set()
    for chunk in chunks:
        required = {"chunk_id", "source_id", "text", "start_line", "end_line", "word_count"}
        if not isinstance(chunk, dict) or not required <= chunk.keys():
            raise ContractError("every chunk must contain the documented corpus fields")
        if not all(isinstance(chunk[field], str) and chunk[field].strip() for field in ("chunk_id", "source_id", "text")):
            raise ContractError("chunk identifiers and text must be non-empty strings")
        if not all(isinstance(chunk[field], int) and chunk[field] > 0 for field in ("start_line", "end_line", "word_count")):
            raise ContractError("chunk locations and word_count must be positive integers")
        if chunk["start_line"] > chunk["end_line"]:
            raise ContractError("chunk start_line cannot follow end_line")
        if chunk["chunk_id"] in seen:
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


def validate_answer_fixtures(data: dict[str, Any], chunk_ids: set[str] | None = None) -> None:
    """Validate deterministic answer-evaluation fixtures before scoring them."""
    require_version(data, "answer fixtures")
    answers = data.get("answers")
    if not isinstance(answers, list) or not answers:
        raise ContractError("answer fixtures must contain a non-empty answers list")
    seen: set[str] = set()
    for item in answers:
        required = {
            "answer_id", "question_id", "answerable", "retrieved_chunk_ids",
            "response_type", "answer", "citations", "unsupported_claims",
        }
        if not isinstance(item, dict) or not required <= item.keys():
            raise ContractError("answer fixture missing required fields")
        if item["answer_id"] in seen or item["response_type"] not in {"answer", "refusal"}:
            raise ContractError("answer IDs must be unique and response_type must be answer or refusal")
        if not isinstance(item["answerable"], bool) or not isinstance(item["answer"], str) or not item["answer"].strip():
            raise ContractError("answerability must be boolean and answer text non-empty")
        list_fields = ("retrieved_chunk_ids", "citations", "unsupported_claims")
        if any(not isinstance(item[field], list) or not all(isinstance(value, str) for value in item[field]) for field in list_fields):
            raise ContractError("retrieved chunks, citations, and unsupported claims must be string lists")
        referenced = set(item["retrieved_chunk_ids"]) | set(item["citations"])
        if chunk_ids is not None and not referenced <= chunk_ids:
            raise ContractError(f"unknown chunk in answer fixture {item['answer_id']}")
        seen.add(item["answer_id"])
