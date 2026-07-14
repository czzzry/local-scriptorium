import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseAuditTests(unittest.TestCase):
    def test_audit_fails_closed_for_pending_plotinus_and_candidates(self):
        result = subprocess.run([
            sys.executable, "scripts/release_audit_v3.py",
            "--register", "sources_public/source_register.v2.json",
            "--pack", "data/packs/late_antiquity_core.v1.json",
            "--questions", "data/evaluation/late-antiquity-available-questions-v2.candidates.json",
            "--review-policy", "data/reviews/review_policy.v1.json",
        ], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ready"])
        self.assertEqual({item["code"] for item in payload["blockers"]}, {"BENCHMARK_NOT_ACCEPTED"})


if __name__ == "__main__":
    unittest.main()
