import unittest
from pathlib import Path

from local_scriptorium.contracts import ContractError, validate_questions_v2
from local_scriptorium.packs import load_corpus_pack


ROOT = Path(__file__).resolve().parents[1]
PASSAGES = {"PASSAGE_A", "PASSAGE_B", "PASSAGE_C"}


def question(
    question_id: str,
    split: str,
    answerability: str,
    evidence_sets: list[dict],
) -> dict:
    passage_ids = sorted(
        {
            passage_id
            for evidence_set in evidence_sets
            for group in evidence_set.get("required_groups", [])
            for passage_id in group
        }
    )
    return {
        "question_id": question_id,
        "family_id": f"FAMILY_{question_id}",
        "question": f"What does item {question_id} ask?",
        "split": split,
        "question_type": (
            "unanswerable" if answerability == "unanswerable" else "concept_tracing"
        ),
        "risk_tags": [],
        "answerability": answerability,
        "canonical_passage_ids": passage_ids,
        "acceptable_evidence_sets": evidence_sets,
        "curation_state": "accepted",
    }


class V2ContractTests(unittest.TestCase):
    def test_answerable_and_unanswerable_questions_validate(self) -> None:
        data = {
            "schema_version": "2.0",
            "dataset_id": "fixture",
            "questions": [
                question(
                    "Q1",
                    "dev",
                    "answerable",
                    [{"required_groups": [["PASSAGE_A"], ["PASSAGE_B"]]}],
                ),
                question("Q2", "test", "unanswerable", []),
            ],
        }
        validate_questions_v2(data, PASSAGES)

    def test_unanswerable_question_cannot_have_evidence(self) -> None:
        data = {
            "schema_version": "2.0",
            "questions": [
                question(
                    "Q1",
                    "dev",
                    "unanswerable",
                    [{"required_groups": [["PASSAGE_A"]]}],
                ),
                question("Q2", "test", "unanswerable", []),
            ],
        }
        with self.assertRaises(ContractError):
            validate_questions_v2(data, PASSAGES)

    def test_unknown_passage_is_rejected(self) -> None:
        data = {
            "schema_version": "2.0",
            "questions": [
                question(
                    "Q1",
                    "dev",
                    "answerable",
                    [{"required_groups": [["NOT_A_PASSAGE"]]}],
                ),
                question("Q2", "test", "unanswerable", []),
            ],
        }
        with self.assertRaises(ContractError):
            validate_questions_v2(data, PASSAGES)

    def test_pack_resolves_by_declared_id(self) -> None:
        pack = load_corpus_pack(ROOT, "late-antiquity-core-v1")
        self.assertEqual(pack.pack_id, "late-antiquity-core-v1")
        self.assertIn("IAMBLICHUS_MYSTERIES_001", pack.manifest["active_source_ids"])

    def test_invalid_required_group_is_rejected(self) -> None:
        data = {
            "schema_version": "2.0",
            "questions": [
                question(
                    "Q1",
                    "dev",
                    "answerable",
                    [{"required_groups": [[]]}],
                ),
                question("Q2", "test", "unanswerable", []),
            ],
        }
        with self.assertRaises(ContractError):
            validate_questions_v2(data, PASSAGES)
