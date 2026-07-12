import unittest

from local_scriptorium.evaluation import evaluate_answers


class AnswerEvaluationTests(unittest.TestCase):
    def test_flags_bad_citation_unsupported_claim_and_missed_refusal(self):
        fixtures = {
            "schema_version": "1.0",
            "answers": [
                {
                    "answer_id": "bad-answer",
                    "question_id": "q1",
                    "answerable": True,
                    "retrieved_chunk_ids": ["chunk-a"],
                    "response_type": "answer",
                    "answer": "An unsupported answer.",
                    "citations": ["chunk-b"],
                    "unsupported_claims": ["unsupported"],
                },
                {
                    "answer_id": "missed-refusal",
                    "question_id": "q2",
                    "answerable": False,
                    "retrieved_chunk_ids": [],
                    "response_type": "answer",
                    "answer": "I answered anyway.",
                    "citations": [],
                    "unsupported_claims": [],
                },
            ],
        }
        results = evaluate_answers(fixtures)
        self.assertEqual(results["answers"][0]["citation_correctness"], 0.0)
        self.assertEqual(results["answers"][0]["faithful"], 0.0)
        self.assertEqual(results["answers"][0]["unsupported_claim_count"], 1)
        self.assertEqual(results["answers"][1]["answerability_correct"], 0.0)
        self.assertEqual(results["answers"][1]["correct_refusal"], 0.0)
