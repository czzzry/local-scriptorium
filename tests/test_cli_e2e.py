import json
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
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
            self.assertTrue((generated / "retrieval_details.csv").is_file())
            metadata = json.loads((generated / "run_metadata.json").read_text())
            self.assertTrue(metadata["timestamp"].endswith("+00:00"))
            self.assertEqual(metadata["configuration"]["split"], "test")
            self.assertEqual(metadata["configuration"]["top_k"], 5)
            self.assertEqual(metadata["runtime"]["dependencies"]["runtime"], "python-standard-library")
            rendered = (generated / "report.html").read_text(encoding="utf-8")
            self.assertIn("<h1>Local Scriptorium Evaluation Report</h1>", rendered)
            self.assertIn("<table>", rendered)
            self.assertIn("<pre><code>python -m pip install", rendered)

    def test_retrieve_emits_json(self):
        process = subprocess.run(
            [sys.executable, "-m", "local_scriptorium", "--root", str(ROOT), "retrieve", "nature of fortune"],
            text=True, capture_output=True, check=True, env={**os.environ, "PYTHONPATH": str(ROOT / "src")}
        )
        self.assertEqual(json.loads(process.stdout)["method"], "bm25")

    def test_default_split_is_development(self):
        from local_scriptorium.cli import parser
        self.assertEqual(parser().parse_args(["evaluate"]).split, "dev")

    def test_validate_v03_pack_emits_machine_readable_summary(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(
                main(
                    [
                        "--root",
                        str(ROOT),
                        "--pack",
                        "late-antiquity-core-v1",
                        "validate-pack",
                    ]
                ),
                0,
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["pack_id"], "late-antiquity-core-v1")
        self.assertIn("IAMBLICHUS_MYSTERIES_001", payload["active_source_ids"])

    def test_ingest_tracer_pack_builds_real_passages_and_chunks(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-m", "local_scriptorium", "--root", str(ROOT), "--output", directory,
                 "--pack", "late-antiquity-tracer-v1", "ingest"],
                text=True, capture_output=True, env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            corpus = json.loads((Path(directory) / "packs" / "late-antiquity-tracer-v1" / "corpus.v1.json").read_text())
            self.assertEqual(corpus["schema_version"], "v0.3-corpus-1.0")
            self.assertGreater(len(corpus["passages"]), 1000)
            self.assertEqual({item["source_id"] for item in corpus["sources"]}, {"BOETHIUS_CONSOLATION_001", "IAMBLICHUS_MYSTERIES_001"})

    def test_full_core_pack_ingests_after_plotinus_scope_is_verified(self):
        result = subprocess.run(
            [sys.executable, "-m", "local_scriptorium", "--root", str(ROOT), "--pack", "late-antiquity-core-v1", "ingest"],
            text=True, capture_output=True, env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_review_export_and_validate_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request = root / "request.json"
            items = root / "items.jsonl"
            evidence = root / "evidence.jsonl"
            packet = root / "packet"
            request.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "review_id": "CLI_REVIEW",
                        "review_kind": "question_evidence",
                        "protocol_version": "1.0",
                        "pack_id": "fixture",
                        "independence_level": "I1",
                        "external_context_allowed": False,
                        "randomization_seed": 1,
                    }
                ),
                encoding="utf-8",
            )
            items.write_text('{"item_id":"ITEM_A","question":"What is supported?"}\n', encoding="utf-8")
            evidence.write_text('{"evidence_id":"EVIDENCE_A","evidence_refs":["ITEM_A"]}\n', encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(
                    main(
                        [
                            "--root",
                            str(ROOT),
                            "review",
                            "export",
                            "--request",
                            str(request),
                            "--items",
                            str(items),
                            "--evidence",
                            str(evidence),
                            "--output",
                            str(packet),
                        ]
                    ),
                    0,
                )
            self.assertEqual(json.loads(output.getvalue())["review_id"], "CLI_REVIEW")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(
                    main(["--root", str(ROOT), "review", "validate-packet", str(packet)]),
                    0,
                )
