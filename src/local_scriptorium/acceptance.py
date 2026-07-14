"""Controlled promotion of reviewed v0.3 question candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import ContractError, validate_questions_v2


def accept_reviewed_questions(
    candidate_path: Path,
    reconciliation_paths: list[Path],
    adjudication_path: Path | None,
    output_path: Path,
) -> dict[str, Any]:
    """Promote only agreement/adjudicated items; never silently relabel candidates."""
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    questions = candidate.get("questions")
    if not isinstance(questions, list):
        raise ContractError("candidate question file has no questions list")
    reconciled: dict[str, str] = {}
    for path in reconciliation_paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        for item in record.get("items", []):
            if item.get("item_id"):
                reconciled[item["item_id"]] = item.get("status", "")
    adjudications: dict[str, str] = {}
    if adjudication_path:
        record = json.loads(adjudication_path.read_text(encoding="utf-8"))
        for item in record.get("items", []):
            if item.get("item_id"):
                adjudications[item["item_id"]] = item.get("decision", "")
    promoted = []
    unresolved = []
    for item in questions:
        copy = dict(item)
        item_id = item["question_id"]
        status = reconciled.get(item_id)
        decision = adjudications.get(item_id)
        if decision == "exclude":
            copy["curation_state"] = "excluded"
        elif decision == "accept" or status in {"agreement", "compatible_caveat"}:
            copy["curation_state"] = "accepted"
        else:
            copy["curation_state"] = "candidate"
            unresolved.append(item_id)
        promoted.append(copy)
    accepted_count = sum(item["curation_state"] == "accepted" for item in promoted)
    excluded_count = sum(item["curation_state"] == "excluded" for item in promoted)
    if unresolved:
        state = "review_incomplete"
    elif accepted_count + excluded_count == len(promoted):
        state = "accepted" if accepted_count else "excluded"
    else:
        state = "review_incomplete"
    result = {"schema_version": "2.0", "dataset_id": candidate.get("dataset_id"), "status": state, "accepted_count": accepted_count, "excluded_count": excluded_count, "unresolved_item_ids": unresolved, "questions": promoted}
    validate_questions_v2(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"status": state, "accepted_count": accepted_count, "excluded_count": excluded_count, "unresolved_item_ids": unresolved}
