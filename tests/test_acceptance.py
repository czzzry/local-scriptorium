import json
import tempfile
import unittest
from pathlib import Path

from local_scriptorium.acceptance import accept_reviewed_questions


class AcceptanceTests(unittest.TestCase):
    def test_material_disagreement_stays_candidate_without_adjudication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = root / "candidate.json"
            reconciliation = root / "reconciliation.json"
            output = root / "accepted.json"
            question = {"question_id": "Q1", "family_id": "F1", "question": "What?", "split": "dev", "question_type": "single_passage_textual", "risk_tags": [], "answerability": "answerable", "canonical_passage_ids": ["P1"], "acceptable_evidence_sets": [{"required_groups": [["P1"]]}], "curation_state": "candidate"}
            question_test = dict(question, question_id="Q2", family_id="F2", split="test")
            candidate.write_text(json.dumps({"schema_version": "2.0", "dataset_id": "D", "questions": [question, question_test]}))
            reconciliation.write_text(json.dumps({"items": [{"item_id": "Q1", "status": "material_disagreement"}, {"item_id": "Q2", "status": "agreement"}]}))
            result = accept_reviewed_questions(candidate, [reconciliation], None, output)
            self.assertEqual(result["status"], "review_incomplete")
            self.assertEqual(json.loads(output.read_text())["questions"][0]["curation_state"], "candidate")


if __name__ == "__main__":
    unittest.main()
