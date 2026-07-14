"""Deterministic validation for blinded review packets and second-pass results."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any


REVIEW_SCHEMA_VERSION = "1.0"
REVIEW_KINDS = {
    "chunk_quality",
    "question_evidence",
    "source_scope_check",
    "answer_claim",
}
INDEPENDENCE_LEVELS = {"I1", "I2", "I3"}
REVIEW_ACTIONS = {
    "accept",
    "accept_with_caveat",
    "revise",
    "reject",
    "insufficient_internal_evidence",
    "needs_external_specialist",
    "invalid_packet",
}
CONFIDENCE_LEVELS = {"high", "medium", "low"}
FORBIDDEN_PACKET_KEYS = {
    "expected_answer",
    "gold_answer",
    "first_pass_verdict",
    "first_pass_grade",
    "first_pass_rationale",
    "retrieval_method",
    "retrieval_rank",
    "retrieval_score",
    "split",
    "threshold",
    "benchmark_result",
    "previous_review",
    "control_mapping",
    "chain_of_thought",
    "analysis",
}


class ReviewContractError(ValueError):
    """Raised when a review packet or result violates its contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewContractError(f"cannot read JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ReviewContractError(f"expected JSON object: {path}")
    return value


def _forbidden_keys(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_PACKET_KEYS:
                found.append(f"{path}.{key}")
            found.extend(_forbidden_keys(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_forbidden_keys(child, f"{path}[{index}]"))
    return found


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ReviewContractError(f"cannot read JSONL: {path}") from exc
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ReviewContractError(f"invalid JSONL at {path}:{line_number}") from exc
        if not isinstance(value, dict):
            raise ReviewContractError(f"JSONL record is not an object: {path}:{line_number}")
        records.append(value)
    return records


def validate_packet(packet_dir: Path) -> dict[str, Any]:
    """Validate a packet and return its opaque item IDs and manifest checksum."""
    if not packet_dir.is_dir():
        raise ReviewContractError(f"packet directory does not exist: {packet_dir}")
    request_path = packet_dir / "request.json"
    items_path = packet_dir / "items.jsonl"
    evidence_path = packet_dir / "evidence.jsonl"
    manifest_path = packet_dir / "manifest.json"
    request = _read_json(request_path)
    items = _read_jsonl(items_path)
    evidence = _read_jsonl(evidence_path)
    manifest = _read_json(manifest_path)

    if request.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ReviewContractError("request schema_version is invalid")
    if request.get("review_kind") not in REVIEW_KINDS:
        raise ReviewContractError("request review_kind is invalid")
    if request.get("independence_level") not in INDEPENDENCE_LEVELS:
        raise ReviewContractError("request independence_level is invalid")
    if not isinstance(request.get("review_id"), str) or not request["review_id"].strip():
        raise ReviewContractError("request review_id is missing")
    if not isinstance(request.get("randomization_seed"), int):
        raise ReviewContractError("request randomization_seed is missing")
    if not isinstance(request.get("external_context_allowed"), bool):
        raise ReviewContractError("request external_context_allowed is missing")
    if not isinstance(request.get("allowed_input_files"), list):
        raise ReviewContractError("request allowed_input_files is missing")
    if not isinstance(request.get("opaque_item_ids"), list):
        raise ReviewContractError("request opaque_item_ids is missing")

    item_ids = [item.get("item_id") for item in items]
    if not item_ids or any(not isinstance(item_id, str) or not item_id.strip() for item_id in item_ids):
        raise ReviewContractError("items must have non-empty item_id values")
    if len(item_ids) != len(set(item_ids)):
        raise ReviewContractError("packet item IDs must be unique")
    if set(request["opaque_item_ids"]) != set(item_ids):
        raise ReviewContractError("request opaque_item_ids do not match packet items")
    if any(not isinstance(item_id, str) or not item_id.strip() for item_id in request["opaque_item_ids"]):
        raise ReviewContractError("request opaque_item_ids are invalid")
    if any(not isinstance(item.get("evidence_refs", []), list) for item in evidence):
        raise ReviewContractError("evidence records must use evidence_refs lists")

    forbidden = _forbidden_keys(request) + _forbidden_keys(items) + _forbidden_keys(evidence)
    if forbidden:
        raise ReviewContractError(f"packet contains forbidden fields: {', '.join(forbidden)}")

    if manifest.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ReviewContractError("manifest schema_version is invalid")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise ReviewContractError("manifest files are missing")
    required_files = {"request.json", "items.jsonl", "evidence.jsonl"}
    if not required_files <= set(files):
        raise ReviewContractError("manifest does not cover required packet files")
    for relative_name, expected in files.items():
        relative_path = Path(relative_name)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ReviewContractError(f"manifest path is not portable: {relative_name}")
        path = packet_dir / relative_path
        if not path.is_file() or not isinstance(expected, str) or sha256_file(path) != expected:
            raise ReviewContractError(f"manifest checksum mismatch: {relative_name}")

    return {
        "review_id": request["review_id"],
        "review_kind": request["review_kind"],
        "independence_level": request["independence_level"],
        "item_ids": item_ids,
        "manifest_sha256": sha256_file(manifest_path),
    }


def validate_result(packet_dir: Path, result_path: Path) -> dict[str, Any]:
    """Validate a second-pass result against its packet."""
    packet = validate_packet(packet_dir)
    result = _read_json(result_path)
    if result.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ReviewContractError("result schema_version is invalid")
    if result.get("review_id") != packet["review_id"]:
        raise ReviewContractError("result review_id does not match packet")
    if result.get("protocol_version") != REVIEW_SCHEMA_VERSION:
        raise ReviewContractError("result protocol_version is invalid")
    if result.get("input_manifest_sha256") != packet["manifest_sha256"]:
        raise ReviewContractError("result input manifest checksum does not match packet")
    if result.get("independence_level") not in INDEPENDENCE_LEVELS:
        raise ReviewContractError("result independence_level is invalid")
    if not isinstance(result.get("external_context_used"), bool):
        raise ReviewContractError("result external_context_used is missing")
    if not isinstance(result.get("items"), list):
        raise ReviewContractError("result items are missing")

    item_ids = [item.get("item_id") for item in result["items"]]
    if set(item_ids) != set(packet["item_ids"]) or len(item_ids) != len(set(item_ids)):
        raise ReviewContractError("result item IDs do not match packet")
    for item in result["items"]:
        required = {
            "item_id",
            "action",
            "reason_codes",
            "confidence",
            "evidence_refs",
            "rationale",
            "external_review_required",
        }
        if not required <= item.keys():
            raise ReviewContractError(f"result item is missing fields: {item.get('item_id')}")
        if item["action"] not in REVIEW_ACTIONS:
            raise ReviewContractError(f"result action is invalid: {item['item_id']}")
        if item["confidence"] not in CONFIDENCE_LEVELS:
            raise ReviewContractError(f"result confidence is invalid: {item['item_id']}")
        if not isinstance(item["reason_codes"], list) or not all(
            isinstance(code, str) and code.strip() for code in item["reason_codes"]
        ):
            raise ReviewContractError(f"result reason_codes are invalid: {item['item_id']}")
        if not isinstance(item["evidence_refs"], list) or not all(
            isinstance(ref, str) and ref.strip() for ref in item["evidence_refs"]
        ):
            raise ReviewContractError(f"result evidence_refs are invalid: {item['item_id']}")
        if not isinstance(item["rationale"], str) or not item["rationale"].strip():
            raise ReviewContractError(f"result rationale is missing: {item['item_id']}")
        if not isinstance(item["external_review_required"], bool):
            raise ReviewContractError(
                f"result external_review_required is invalid: {item['item_id']}"
            )

    forbidden = _forbidden_keys(result)
    if forbidden:
        raise ReviewContractError(f"result contains forbidden fields: {', '.join(forbidden)}")
    return {"review_id": result["review_id"], "item_count": len(item_ids)}


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(value, sort_keys=True) + "\n" for value in values),
        encoding="utf-8",
    )


def export_review_packet(
    output_dir: Path,
    request: dict[str, Any],
    items: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write a blinded randomized packet and validate it before returning."""
    if request.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ReviewContractError("packet export request schema_version is invalid")
    if not isinstance(request.get("randomization_seed"), int):
        raise ReviewContractError("packet export requires a randomization_seed")
    item_copy = [dict(item) for item in items]
    evidence_copy = [dict(record) for record in evidence]
    randomizer = random.Random(request["randomization_seed"])
    randomizer.shuffle(item_copy)
    randomizer.shuffle(evidence_copy)
    request_copy = dict(request)
    request_copy["opaque_item_ids"] = [item.get("item_id") for item in item_copy]
    request_copy.setdefault("allowed_input_files", ["items.jsonl", "evidence.jsonl"])

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "request.json", request_copy)
    _write_jsonl(output_dir / "items.jsonl", item_copy)
    _write_jsonl(output_dir / "evidence.jsonl", evidence_copy)
    files = {
        filename: sha256_file(output_dir / filename)
        for filename in ("request.json", "items.jsonl", "evidence.jsonl")
    }
    _write_json(output_dir / "manifest.json", {"schema_version": REVIEW_SCHEMA_VERSION, "files": files})
    return validate_packet(output_dir)


def reconcile_review(
    control_path: Path,
    packet_dir: Path,
    result_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Compare a hidden first pass with a validated second pass."""
    control = _read_json(control_path)
    if control.get("schema_version") != REVIEW_SCHEMA_VERSION:
        raise ReviewContractError("control schema_version is invalid")
    packet = validate_packet(packet_dir)
    validate_result(packet_dir, result_path)
    result = _read_json(result_path)
    if control.get("review_id") != packet["review_id"]:
        raise ReviewContractError("control review_id does not match packet")
    control_items = control.get("items")
    if not isinstance(control_items, list):
        raise ReviewContractError("control items are missing")
    control_by_id = {item.get("item_id"): item for item in control_items}
    result_by_id = {item["item_id"]: item for item in result["items"]}
    if set(control_by_id) != set(packet["item_ids"]):
        raise ReviewContractError("control items do not match packet")

    reconciled: list[dict[str, Any]] = []
    for item_id in packet["item_ids"]:
        first = control_by_id[item_id]
        second = result_by_id[item_id]
        first_action = first.get("first_pass_action")
        second_action = second["action"]
        if first_action == second_action:
            status = "agreement"
        elif {first_action, second_action} <= {"accept", "accept_with_caveat"}:
            status = "compatible_caveat"
        else:
            status = "material_disagreement"
        reconciled.append(
            {
                "item_id": item_id,
                "status": status,
                "first_pass_action": first_action,
                "second_pass_action": second_action,
            }
        )

    output = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "review_id": packet["review_id"],
        "second_pass_result": str(result_path.name),
        "items": reconciled,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(output_path, output)
    return output


def stale_dependencies(
    recorded_dependencies: dict[str, str],
    current_dependencies: dict[str, str],
) -> list[str]:
    """Return dependency names whose recorded checksum is missing or changed."""
    if not isinstance(recorded_dependencies, dict) or not isinstance(current_dependencies, dict):
        raise ReviewContractError("dependency maps must be objects")
    return sorted(
        name
        for name, checksum in recorded_dependencies.items()
        if current_dependencies.get(name) != checksum
    )


def audit_review_coverage(
    accepted_item_ids: list[str],
    reconciliation_paths: list[Path],
    *,
    stale_item_ids: set[str] | None = None,
    required_human_spot_check_fraction: float = 0.15,
) -> dict[str, Any]:
    """Report release blockers without mutating canonical questions or reviews."""
    expected = set(accepted_item_ids)
    seen: set[str] = set()
    disagreements: list[str] = []
    for path in reconciliation_paths:
        record = _read_json(path)
        for item in record.get("items", []):
            item_id = item.get("item_id")
            if item_id in expected:
                seen.add(item_id)
                if item.get("status") == "material_disagreement":
                    disagreements.append(item_id)
    stale = sorted((stale_item_ids or set()) & expected)
    missing = sorted(expected - seen)
    blockers = []
    if missing:
        blockers.append({"code": "MISSING_REVIEW_COVERAGE", "item_ids": missing})
    if disagreements:
        blockers.append({"code": "UNRESOLVED_DISAGREEMENTS", "item_ids": sorted(set(disagreements))})
    if stale:
        blockers.append({"code": "STALE_REVIEWS", "item_ids": stale})
    return {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "accepted_item_count": len(expected),
        "reviewed_item_count": len(seen),
        "human_spot_check_fraction": required_human_spot_check_fraction,
        "ready": not blockers,
        "blockers": blockers,
    }
