import unittest

from local_scriptorium.evaluation_v2 import evaluate_questions_v2


class EvaluationV2Tests(unittest.TestCase):
    def test_unanswerable_items_are_not_in_retrieval_denominator(self):
        corpus = {"chunks": [{"chunk_id": "C1", "source_id": "S", "text": "fortune and providence", "passage_ids": ["P1"], "start_line": 1, "end_line": 2, "word_count": 3}]}
        questions = [
            {"question_id": "Q1", "question": "fortune", "answerability": "answerable", "acceptable_evidence_sets": [{"required_groups": [["P1"]]}]},
            {"question_id": "Q2", "question": "original Greek wording", "answerability": "unanswerable", "acceptable_evidence_sets": []},
        ]
        result = evaluate_questions_v2(corpus, questions)
        self.assertEqual(result["answerable_count"], 1)
        self.assertEqual(len(result["rows"]), 2)


if __name__ == "__main__":
    unittest.main()
