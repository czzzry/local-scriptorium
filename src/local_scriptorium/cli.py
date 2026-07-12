"""Command-line interface for composable local evaluation workflows."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .contracts import (
    ContractError,
    read_json,
    validate_corpus,
    validate_answer_fixtures,
    validate_manifest,
    validate_questions,
)
from .evaluation import evaluate_answers, evaluate_retrieval, run_metadata, write_json
from .reporting import write_reports
from .retrieval import Retriever

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "outputs" / "generated"


def paths(args: argparse.Namespace) -> tuple[Path, Path, Path, Path]:
    root = Path(args.root).resolve()
    output = Path(args.output).resolve() if args.output else root / "outputs" / "generated"
    return root, output, root / "chunks" / "boethius_consolation_chunks.json", root / "data" / "evaluation" / "questions.v1.json"


def command_ingest(args: argparse.Namespace) -> int:
    root, output, source_corpus, _ = paths(args)
    manifest = read_json(root / "sources_public" / "source_manifest.json")
    validate_manifest(manifest, root)
    corpus = read_json(source_corpus)
    corpus["schema_version"] = "1.0"
    validate_corpus(corpus)
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "corpus.v1.json", corpus)
    shutil.copyfile(root / "sources_public" / "source_manifest.json", output / "manifest.v1.json")
    print(output / "corpus.v1.json")
    return 0


def command_retrieve(args: argparse.Namespace) -> int:
    root, output, source_corpus, _ = paths(args)
    corpus_path = output / "corpus.v1.json" if (output / "corpus.v1.json").exists() else source_corpus
    corpus = read_json(corpus_path)
    corpus.setdefault("schema_version", "1.0")
    validate_corpus(corpus)
    results = Retriever(corpus["chunks"]).search(args.query, args.method, args.top_k)
    payload = {"schema_version": "1.0", "query": args.query, "method": args.method, "top_k": args.top_k, "results": [vars(result) for result in results]}
    print(json.dumps(payload, indent=2))
    return 0


def command_evaluate(args: argparse.Namespace) -> int:
    root, output, source_corpus, questions_path = paths(args)
    corpus_path = output / "corpus.v1.json" if (output / "corpus.v1.json").exists() else source_corpus
    corpus = read_json(corpus_path)
    corpus.setdefault("schema_version", "1.0")
    questions = read_json(questions_path)
    validate_corpus(corpus)
    validate_questions(questions, {chunk["chunk_id"] for chunk in corpus["chunks"]})
    fixtures = read_json(root / "data" / "answers" / "fixtures.v1.json")
    validate_answer_fixtures(fixtures, {chunk["chunk_id"] for chunk in corpus["chunks"]})
    results = evaluate_retrieval(corpus, questions, args.split, args.top_k, args.seed)
    answer_results = evaluate_answers(fixtures)
    metadata = run_metadata(
        root,
        corpus_path,
        seed=args.seed,
        split=args.split,
        top_k=args.top_k,
        deterministic=args.deterministic,
    )
    write_json(output / "retrieval_results.json", results)
    write_json(output / "answer_results.json", answer_results)
    write_json(output / "run_metadata.json", metadata)
    print(output / "retrieval_results.json")
    return 0


def command_report(args: argparse.Namespace) -> int:
    _, output, _, _ = paths(args)
    results = read_json(output / "retrieval_results.json")
    answers = read_json(output / "answer_results.json")
    metadata = read_json(output / "run_metadata.json")
    write_reports(output, results, answers, metadata)
    print(output / "report.md")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="scriptorium", description="Offline local-RAG evaluation harness")
    result.add_argument("--root", default=str(ROOT), help="repository root")
    result.add_argument("--output", help="generated artifact directory")
    commands = result.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest", help="validate provenance and materialize a corpus contract")
    ingest.set_defaults(function=command_ingest)
    retrieve = commands.add_parser("retrieve", help="retrieve ranked evidence for one query")
    retrieve.add_argument("query")
    retrieve.add_argument("--method", choices=["keyword", "bm25", "vector", "hybrid"], default="bm25")
    retrieve.add_argument("--top-k", type=int, default=5)
    retrieve.set_defaults(function=command_retrieve)
    evaluate = commands.add_parser("evaluate", help="run offline retrieval and answer evaluation")
    evaluate.add_argument("--split", choices=["dev", "test"], default="dev", help="test must be selected explicitly")
    evaluate.add_argument("--top-k", type=int, default=5)
    evaluate.add_argument("--seed", type=int, default=42)
    evaluate.add_argument("--deterministic", action="store_true")
    evaluate.set_defaults(function=command_evaluate)
    report = commands.add_parser("report", help="derive Markdown, HTML, and CSV from raw results")
    report.set_defaults(function=command_report)
    return result


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        return args.function(args)
    except (ContractError, FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
