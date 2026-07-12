import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OutputIsolationTests(unittest.TestCase):
    def test_legacy_scripts_do_not_target_curated_outputs(self):
        for path in (ROOT / "scripts").glob("*.py"):
            text = path.read_text(encoding="utf-8")
            if "OUTPUT_PATH" in text or "OUTPUT_LOG_PATH" in text:
                if path.name not in {"chunk_source.py", "clean_gutenberg_text.py"}:
                    self.assertIn('"generated"', text, path.name)

