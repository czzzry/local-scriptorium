import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from local_scriptorium.reviewing import (
    ReviewContractError,
    export_review_packet,
    reconcile_review,
    stale_dependencies,
    validate_packet,
    validate_result,
)


def write_packet(root: Path, *, forbidden: bool = False) -> Path:
    packet = root / "packet"
    packet.mkdir()
    request = {
        "schema_version": "1.0",
        "review_id": "REVIEW_001",
        "review_kind": "question_evidence",
        "protocol_version": "1.0",
        "pack_id": "fixture-pack",
        "independence_level": "I1",
        "external_context_allowed": False,
        "randomization_seed": 42,
        "allowed_input_files": ["items.jsonl", "evidence.jsonl"],
        "opaque_item_ids": ["ITEM_A"],
    }
    item = {
        "item_id": "ITEM_A",
        "question": "What does the passage establish?",
        "task_type": "single_passage_textual",
    }
    if forbidden:
        item["expected_answer"] = "hidden"
    evidence = {
        "evidence_id": "EVIDENCE_A",
        "evidence_refs": ["ITEM_A"],
        "text": "The supplied passage.",
    }
    (packet / "request.json").write_text(json.dumps(request), encoding="utf-8")
    (packet / "items.jsonl").write_text(json.dumps(item) + "\n", encoding="utf-8")
    (packet / "evidence.jsonl").write_text(json.dumps(evidence) + "\n", encoding="utf-8")
    files = {}
    for filename in ("request.json", "items.jsonl", "evidence.jsonl"):
        digest = hashlib.sha256((packet / filename).read_bytes()).hexdigest()
        files[filename] = digest
    (packet / "manifest.json").write_text(
        json.dumps({"schema_version": "1.0", "files": files}),
        encoding="utf-8",
    )
    return packet


class ReviewingTests(unittest.TestCase):
    def test_export_randomizes_and_validates_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exported"
            summary = export_review_packet(
                output,
                {
                    "schema_version": "1.0",
                    "review_id": "REVIEW_EXPORT",
                    "review_kind": "question_evidence",
                    "protocol_version": "1.0",
                    "pack_id": "fixture-pack",
                    "independence_level": "I1",
                    "external_context_allowed": False,
                    "randomization_seed": 42,
                },
                [
                    {"item_id": "ITEM_A", "question": "A"},
                    {"item_id": "ITEM_B", "question": "B"},
                ],
                [{"evidence_id": "EVIDENCE_A", "evidence_refs": ["ITEM_A"]}],
            )
            self.assertEqual(summary["review_id"], "REVIEW_EXPORT")
            self.assertEqual(len(summary["item_ids"]), 2)
            self.assertTrue((output / "manifest.json").is_file())

    def test_valid_packet_and_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            packet = write_packet(Path(directory))
            summary = validate_packet(packet)
            result = Path(directory) / "result.json"
            result.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "review_id": "REVIEW_001",
                        "protocol_version": "1.0",
                        "input_manifest_sha256": summary["manifest_sha256"],
                        "skill_checksum": "skill-checksum",
                        "reviewer_type": "test",
                        "model_identity": "fixture",
                        "independence_level": "I1",
                        "external_context_used": False,
                        "completed_at": "2026-07-13T00:00:00+00:00",
                        "items": [
                            {
                                "item_id": "ITEM_A",
                                "action": "accept",
                                "reason_codes": [],
                                "confidence": "high",
                                "evidence_refs": ["EVIDENCE_A"],
                                "rationale": "The supplied passage directly supports the item.",
                                "external_review_required": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            validated = validate_result(packet, result)
            self.assertEqual(validated["item_count"], 1)

    def test_forbidden_packet_field_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            packet = write_packet(Path(directory), forbidden=True)
            with self.assertRaises(ReviewContractError):
                validate_packet(packet)

    def test_manifest_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            packet = write_packet(Path(directory))
            (packet / "items.jsonl").write_text(
                '{"item_id":"ITEM_A","question":"tampered"}\n',
                encoding="utf-8",
            )
            with self.assertRaises(ReviewContractError):
                validate_packet(packet)

    def test_result_item_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            packet = write_packet(Path(directory))
            summary = validate_packet(packet)
            result = Path(directory) / "result.json"
            result.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "review_id": "REVIEW_001",
                        "protocol_version": "1.0",
                        "input_manifest_sha256": summary["manifest_sha256"],
                        "skill_checksum": "skill-checksum",
                        "reviewer_type": "test",
                        "model_identity": "fixture",
                        "independence_level": "I1",
                        "external_context_used": False,
                        "completed_at": "2026-07-13T00:00:00+00:00",
                        "items": [],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ReviewContractError):
                validate_result(packet, result)

    def test_reconciliation_is_separate_from_second_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = write_packet(root)
            summary = validate_packet(packet)
            result = root / "result.json"
            result.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "review_id": "REVIEW_001",
                        "protocol_version": "1.0",
                        "input_manifest_sha256": summary["manifest_sha256"],
                        "skill_checksum": "skill-checksum",
                        "reviewer_type": "test",
                        "model_identity": "fixture",
                        "independence_level": "I1",
                        "external_context_used": False,
                        "completed_at": "2026-07-13T00:00:00+00:00",
                        "items": [
                            {
                                "item_id": "ITEM_A",
                                "action": "revise",
                                "reason_codes": ["missing_evidence"],
                                "confidence": "medium",
                                "evidence_refs": ["EVIDENCE_A"],
                                "rationale": "The first pass selected insufficient evidence.",
                                "external_review_required": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            control = root / "control.json"
            control.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "review_id": "REVIEW_001",
                        "items": [{"item_id": "ITEM_A", "first_pass_action": "accept"}],
                    }
                ),
                encoding="utf-8",
            )
            reconciliation = root / "reconciliation.json"
            output = reconcile_review(control, packet, result, reconciliation)
            self.assertEqual(output["items"][0]["status"], "material_disagreement")
            self.assertTrue(reconciliation.is_file())

    def test_dependency_change_is_stale(self) -> None:
        self.assertEqual(
            stale_dependencies(
                {"source": "one", "question": "two"},
                {"source": "one", "question": "changed"},
            ),
            ["question"],
        )
