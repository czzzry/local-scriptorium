import unittest
from types import SimpleNamespace

from local_scriptorium.generation import FakeModelAdapter, grounded_answer


class GenerationTests(unittest.TestCase):
    def test_fake_adapter_refuses_without_context(self):
        result = grounded_answer("Question", [], {"chunks": []}, FakeModelAdapter())
        self.assertEqual(result["answerability"], "unanswerable")
        self.assertEqual(result["citations"], [])

    def test_grounded_answer_carries_canonical_source_metadata(self):
        corpus = {"chunks": [{"chunk_id": "C1", "source_id": "S1", "author": "Author", "work": "Work", "start_line": 1, "end_line": 2}]}
        result = grounded_answer("Question", [SimpleNamespace(chunk_id="C1")], corpus, FakeModelAdapter())
        self.assertEqual(result["answerability"], "answerable")
        self.assertEqual(result["textual_evidence"][0]["author"], "Author")
        self.assertEqual(result["citations"], ["C1"])


if __name__ == "__main__":
    unittest.main()
