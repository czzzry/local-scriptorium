import json
import tempfile
import unittest
from pathlib import Path

from local_scriptorium.reviewing import audit_review_coverage


class ReviewCoverageTests(unittest.TestCase):
    def test_coverage_reports_missing_and_stale_items(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reconciliation.json"
            path.write_text(json.dumps({"items": [{"item_id": "Q1", "status": "agreement"}]}))
            result = audit_review_coverage(["Q1", "Q2"], [path], stale_item_ids={"Q1"})
            self.assertFalse(result["ready"])
            self.assertEqual({item["code"] for item in result["blockers"]}, {"MISSING_REVIEW_COVERAGE", "STALE_REVIEWS"})


if __name__ == "__main__":
    unittest.main()
