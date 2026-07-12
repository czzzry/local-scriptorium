import unittest
from pathlib import Path

from local_scriptorium.contracts import read_json
from local_scriptorium.evaluation import evaluate_retrieval

ROOT = Path(__file__).resolve().parents[1]


class RegressionTests(unittest.TestCase):
    def test_offline_test_baseline_has_defensible_floor(self):
        corpus = read_json(ROOT / "chunks/boethius_consolation_chunks.json")
        questions = read_json(ROOT / "data/evaluation/questions.v1.json")
        result = evaluate_retrieval(corpus, questions, "test")
        # A loose guard catches major ranking/data breakage without claiming a quality target.
        self.assertGreaterEqual(result["methods"]["bm25"]["summary"]["hit_rate@5"], 0.45)
