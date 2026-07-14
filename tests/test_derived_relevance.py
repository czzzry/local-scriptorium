import unittest

from local_scriptorium.derived_relevance import derive_relevance


class DerivedRelevanceTests(unittest.TestCase):
    def test_passage_truth_maps_to_chunks_without_mutating_questions(self):
        questions = [{
            "question_id": "Q1",
            "acceptable_evidence_sets": [{"required_groups": [["P1"], ["P2"]]}],
        }]
        chunks = [{"chunk_id": "C1", "passage_ids": ["P1"]}, {"chunk_id": "C2", "passage_ids": ["P2"]}]
        self.assertEqual(derive_relevance(questions, chunks), {"Q1": {"C1": 3, "C2": 3}})
        self.assertNotIn("relevance", questions[0])


if __name__ == "__main__":
    unittest.main()
