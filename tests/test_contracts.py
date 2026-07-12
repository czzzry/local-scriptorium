import copy
import unittest
from pathlib import Path

from local_scriptorium.contracts import (
    ContractError,
    read_json,
    validate_answer_fixtures,
    validate_corpus,
    validate_manifest,
    validate_questions,
)

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_repository_contracts(self):
        manifest = read_json(ROOT / "sources_public/source_manifest.json")
        corpus = read_json(ROOT / "chunks/boethius_consolation_chunks.json")
        questions = read_json(ROOT / "data/evaluation/questions.v1.json")
        fixtures = read_json(ROOT / "data/answers/fixtures.v1.json")
        validate_manifest(manifest, ROOT)
        validate_corpus(corpus)
        validate_questions(questions, {chunk["chunk_id"] for chunk in corpus["chunks"]})
        validate_answer_fixtures(fixtures, {chunk["chunk_id"] for chunk in corpus["chunks"]})
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

    def test_manifest_rejects_machine_specific_or_parent_paths(self):
        manifest = read_json(ROOT / "sources_public/source_manifest.json")
        for bad_path in ("/absolute/machine/path/private.txt", "../private.txt"):
            broken = copy.deepcopy(manifest)
            broken["sources"][0]["processed_path"] = bad_path
            with self.assertRaises(ContractError):
                validate_manifest(broken, ROOT, verify_checksum=False)

    def test_answer_fixture_unknown_citation_is_rejected(self):
        fixtures = read_json(ROOT / "data/answers/fixtures.v1.json")
        with self.assertRaises(ContractError):
            validate_answer_fixtures(fixtures, {"not-a-real-chunk"})
