import copy
import unittest
from pathlib import Path

from local_scriptorium.contracts import ContractError, read_json, validate_corpus, validate_manifest, validate_questions

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_repository_contracts(self):
        manifest = read_json(ROOT / "sources_public/source_manifest.json")
        corpus = read_json(ROOT / "chunks/boethius_consolation_chunks.json")
        questions = read_json(ROOT / "data/evaluation/questions.v1.json")
        validate_manifest(manifest, ROOT)
        validate_corpus(corpus)
        validate_questions(questions, {chunk["chunk_id"] for chunk in corpus["chunks"]})
        self.assertEqual(len(questions["questions"]), 50)

    def test_missing_provenance_is_rejected(self):
        manifest = read_json(ROOT / "sources_public/source_manifest.json")
        broken = copy.deepcopy(manifest)
        del broken["sources"][0]["license"]
        with self.assertRaises(ContractError):
            validate_manifest(broken, ROOT, verify_checksum=False)

    def test_unknown_relevance_chunk_is_rejected(self):
        questions = read_json(ROOT / "data/evaluation/questions.v1.json")
        with self.assertRaises(ContractError):
            validate_questions(questions, {"not-a-real-chunk"})
