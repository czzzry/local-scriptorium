import unittest

from local_scriptorium.retrieval import Retriever


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.retriever = Retriever([
            {"chunk_id": "b", "text": "fortune changes and turns her wheel"},
            {"chunk_id": "a", "text": "happiness is the complete good"},
            {"chunk_id": "c", "text": "unrelated poetry"},
        ])

    def test_all_methods_rank_matching_chunk_first(self):
        for method in ("keyword", "bm25", "vector", "hybrid"):
            with self.subTest(method=method):
                self.assertEqual(self.retriever.search("complete happiness good", method, 1)[0].chunk_id, "a")

    def test_ties_are_stable(self):
        self.assertEqual([row.chunk_id for row in self.retriever.search("missing", "bm25", 3)], ["a", "b", "c"])

    def test_invalid_method_and_k(self):
        with self.assertRaises(ValueError):
            self.retriever.search("x", "dense")
        with self.assertRaises(ValueError):
            self.retriever.search("x", top_k=0)

