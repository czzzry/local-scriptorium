"""Fail-closed release audit for the v0.3 milestone."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--pack", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--review-policy", type=Path, required=True)
    parser.add_argument("--reconciliation", type=Path, action="append", default=[])
    args = parser.parse_args()
    register = json.loads(args.register.read_text())
    pack = json.loads(args.pack.read_text())
    questions = json.loads(args.questions.read_text())
    policy = json.loads(args.review_policy.read_text())
    blockers = []
    pending = [source["source_id"] for source in register["sources"] if source["status"] == "approved" and not source.get("normalized_checksum_sha256")]
    if pending:
        blockers.append({"code": "PENDING_SOURCE_CHECKSUMS", "source_ids": pending})
    if len(pack.get("active_source_ids", [])) != 9:
        blockers.append({"code": "PACK_SCOPE_NOT_FROZEN", "active_source_count": len(pack.get("active_source_ids", []))})
    # A released benchmark may contain explicitly excluded items; exclusions
    # are resolved review outcomes and must not be mistaken for unresolved
    # candidates. Only candidate/reviewed items block release.
    if questions.get("status") != "accepted" or any(
        item.get("curation_state") not in {"accepted", "excluded"}
        for item in questions.get("questions", [])
    ):
        blockers.append({"code": "BENCHMARK_NOT_ACCEPTED", "dataset_status": questions.get("status")})
    accepted_ids = [item["question_id"] for item in questions.get("questions", []) if item.get("curation_state") == "accepted"]
    if accepted_ids and args.reconciliation:
        reconciled = {item.get("item_id") for path in args.reconciliation for item in json.loads(path.read_text()).get("items", [])}
        missing = sorted(set(accepted_ids) - reconciled)
        if missing:
            blockers.append({"code": "MISSING_REVIEW_COVERAGE", "item_ids": missing})
    if not policy.get("release_rules", {}).get("all_accepted_questions_reviewed"):
        blockers.append({"code": "REVIEW_POLICY_INCOMPLETE"})
    result = {"schema_version": "v0.3-release-audit-1.0", "ready": not blockers, "blockers": blockers}
    print(json.dumps(result, indent=2))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
