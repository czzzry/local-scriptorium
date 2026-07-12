import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from local_scriptorium.cli import main

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_offline_ingest_evaluate_report(self):
        with tempfile.TemporaryDirectory() as directory:
            common = ["--root", str(ROOT), "--output", directory]
            self.assertEqual(main([*common, "ingest"]), 0)
            self.assertEqual(main([*common, "evaluate", "--split", "test", "--deterministic"]), 0)
            self.assertEqual(main([*common, "report"]), 0)
            generated = Path(directory)
            self.assertTrue((generated / "report.md").is_file())
            self.assertTrue((generated / "report.html").is_file())
            self.assertTrue((generated / "retrieval_summary.csv").is_file())
            metadata = json.loads((generated / "run_metadata.json").read_text())
            self.assertEqual(metadata["timestamp"], "normalized-for-reproducibility")

    def test_retrieve_emits_json(self):
        process = subprocess.run(
            [sys.executable, "-m", "local_scriptorium", "--root", str(ROOT), "retrieve", "nature of fortune"],
            text=True, capture_output=True, check=True, env={**os.environ, "PYTHONPATH": str(ROOT / "src")}
        )
        self.assertEqual(json.loads(process.stdout)["method"], "bm25")

    def test_default_split_is_development(self):
        from local_scriptorium.cli import parser
        self.assertEqual(parser().parse_args(["evaluate"]).split, "dev")

