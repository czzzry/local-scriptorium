import unittest
from pathlib import Path

from local_scriptorium.contracts import read_json
from local_scriptorium.evaluation import evaluate_retrieval

ROOT = Path(__file__).resolve().parents[1]


class RegressionTests(unittest.TestCase):
    def test_offline_test_baseline_has_defensible_floor(self):
        corpus = read_json(ROOT / "chunks/boethius_consolation_chunks.json")
        questions = read_json(ROOT / "data/evaluation/questions.v1.json")
        thresholds = read_json(ROOT / "data/evaluation/regression_thresholds.v1.json")
        result = evaluate_retrieval(corpus, questions, "test")
        for method, minimum in thresholds["minimum"].items():
            with self.subTest(method=method):
                self.assertGreaterEqual(result["methods"][method]["summary"][thresholds["metric"]], minimum)
