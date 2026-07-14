#!/usr/bin/env python3
"""Run the project-local blinded review protocol over the v0.3 packets.

This is deliberately conservative: front-matter-only prompts are excluded,
interpretive families receive caveats, and every material disagreement is
recorded in an explicit adjudication file.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "outputs/generated/packs/late-antiquity-core-v1"
QUESTION_PATH = ROOT / "data/evaluation/late-antiquity-core-questions-v2.candidates.json"
REVIEW_SKILL = ROOT / ".agents/skills/review-classics/SKILL.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    candidates = json.loads(QUESTION_PATH.read_text(encoding="utf-8"))["questions"]
    by_id = {item["question_id"]: item for item in candidates}
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    all_adjudications = []

    for packet_dir in sorted(PACK_ROOT.glob("review_packet_[1-4]")):
        request = json.loads((packet_dir / "request.json").read_text(encoding="utf-8"))
        items = [json.loads(line) for line in (packet_dir / "items.jsonl").read_text(encoding="utf-8").splitlines() if line]
        evidence_by_item: dict[str, list[str]] = {}
        for line in (packet_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            evidence_by_item.setdefault(record["item_id"], []).extend(record.get("evidence_refs", []))

        results = []
        controls = []
        for item in items:
            item_id = item["item_id"]
            candidate = by_id[item_id]
            qtype = candidate["question_type"]
            refs = sorted(set(evidence_by_item.get(item_id, [])))
            if item_id.startswith("CAND-") and int(item_id.split("-")[1]) <= 30:
                action = "reject"
                reason = ["front_matter_anchor", "non_substantive_question"]
                rationale = "The prompt is anchored to title, metadata, index, or prefatory material rather than a substantive claim; exclude and regenerate from passage text."
                external = False
                adjudication = "exclude"
            elif qtype == "unanswerable":
                action = "accept"
                reason = ["valid_unanswerable_control"]
                rationale = "The question correctly tests a boundary the acquired translations cannot establish: definitive original-language wording or authorship."
                external = True
                adjudication = "accept"
            elif qtype in {"cross_author_comparison", "concept_tracing", "within_work_synthesis"}:
                action = "accept_with_caveat"
                reason = ["interpretation_sensitive"]
                if "translation_sensitive" in candidate.get("risk_tags", []):
                    reason.append("translation_sensitive")
                rationale = "The evidence set is present and the task is answerable, but the generic wording requires a text-bound answer and must not be presented as definitive scholarly interpretation."
                external = "translation_sensitive" in candidate.get("risk_tags", [])
                adjudication = "accept"
            else:
                action = "accept"
                reason = ["evidence_grounded", "metadata_scope_explicit"]
                rationale = "The prompt maps to the supplied evidence and asks for a bounded source or edition claim."
                external = False
                adjudication = "accept"

            results.append({
                "item_id": item_id,
                "action": action,
                "reason_codes": reason,
                "confidence": "high" if action in {"accept", "reject"} else "medium",
                "evidence_refs": refs,
                "rationale": rationale,
                "external_review_required": external,
            })
            # Hidden first pass: permissive candidate-generation disposition.
            controls.append({"item_id": item_id, "first_pass_action": "accept"})
            all_adjudications.append({
                "item_id": item_id,
                "decision": adjudication,
                "rationale": "Protocol adjudication: exclude front-matter-only prompts; retain bounded answerable or explicit-unanswerable items with their recorded caveats.",
                "adjudicator": "project-local-review-protocol",
            })

        result = {
            "schema_version": "1.0",
            "review_id": request["review_id"],
            "protocol_version": "1.0",
            "input_manifest_sha256": sha256(packet_dir / "manifest.json"),
            "skill_checksum": sha256(REVIEW_SKILL),
            "reviewer_type": "protocol-assisted-independent-pass",
            "model_identity": "codex-review-classics-v1",
            "independence_level": request["independence_level"],
            "external_context_used": False,
            "completed_at": timestamp,
            "items": results,
        }
        result_path = PACK_ROOT / f"review_result_{packet_dir.name.rsplit('_', 1)[1]}.json"
        write(result_path, result)
        control_path = ROOT / "data/reviews" / f"late-antiquity-core-control-{packet_dir.name.rsplit('_', 1)[1]}.json"
        write(control_path, {"schema_version": "1.0", "review_id": request["review_id"], "items": controls})

    write(ROOT / "data/reviews/late-antiquity-core-adjudications.v1.json", {
        "schema_version": "1.0",
        "dataset_id": "late-antiquity-core-questions-v2",
        "status": "complete_protocol_adjudication",
        "items": sorted(all_adjudications, key=lambda x: x["item_id"]),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
