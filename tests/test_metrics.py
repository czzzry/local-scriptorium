import unittest

from local_scriptorium.metrics import aggregate, bootstrap_ci, query_metrics


class MetricsTests(unittest.TestCase):
    def test_ranked_metrics(self):
        result = query_metrics(["noise", "a", "b"], {"a": 3, "b": 1}, 3)
        self.assertEqual(result["recall@3"], 1.0)
        self.assertAlmostEqual(result["precision@3"], 2 / 3)
        self.assertEqual(result["mrr"], 0.5)
        self.assertGreater(result["ndcg@3"], 0)

    def test_empty_relevance(self):
        self.assertEqual(query_metrics([], {}, 5)["hit_rate@5"], 0.0)

    def test_bootstrap_is_seeded(self):
        self.assertEqual(bootstrap_ci([0, 1, 1], seed=7), bootstrap_ci([0, 1, 1], seed=7))

    def test_aggregate(self):
        self.assertEqual(aggregate([{"x": 0.0}, {"x": 1.0}]), {"x": 0.5})

