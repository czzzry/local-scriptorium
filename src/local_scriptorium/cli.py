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
from .ingestion import SourceDescriptor, build_chunks, build_passages, sha256_text
from .derived_relevance import derive_relevance
from .generation import FakeModelAdapter, grounded_answer
from .evaluation_v2 import evaluate_questions_v2
from .acceptance import accept_reviewed_questions
from .packs import load_corpus_pack
from .reporting import write_reports
from .retrieval import Retriever
from .reviewing import (
    ReviewContractError,
    export_review_packet,
    reconcile_review,
    validate_packet as validate_review_packet,
    validate_result as validate_review_result,
    audit_review_coverage,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "outputs" / "generated"


def paths(args: argparse.Namespace) -> tuple[Path, Path, Path, Path]:
    root = Path(args.root).resolve()
    output = Path(args.output).resolve() if args.output else root / "outputs" / "generated"
    if args.pack:
        pack = load_corpus_pack(root, args.pack)
        pack_output = output / "packs" / pack.pack_id
        return root, pack_output, pack.corpus_path, pack.questions_path
    return root, output, root / "chunks" / "boethius_consolation_chunks.json", root / "data" / "evaluation" / "questions.v1.json"


def command_validate_pack(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    pack = load_corpus_pack(root, args.pack)
    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "pack_id": pack.pack_id,
                "active_source_ids": pack.manifest["active_source_ids"],
                "blocked_source_ids": pack.manifest["blocked_source_ids"],
                "manifest": str(pack.manifest_path.relative_to(root)),
            },
            indent=2,
        )
    )
    return 0


def read_jsonl(path: Path) -> list[dict]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"JSONL record must be an object: {path}")
            records.append(value)
    return records


def command_review_export(args: argparse.Namespace) -> int:
    request = read_json(Path(args.request))
    items = read_jsonl(Path(args.items))
    evidence = read_jsonl(Path(args.evidence))
    summary = export_review_packet(Path(args.output), request, items, evidence)
    print(json.dumps(summary, indent=2))
    return 0


def command_review_validate_packet(args: argparse.Namespace) -> int:
    summary = validate_review_packet(Path(args.packet).resolve())
    print(json.dumps(summary, indent=2))
    return 0


def command_review_validate_result(args: argparse.Namespace) -> int:
    summary = validate_review_result(
        Path(args.packet).resolve(),
        Path(args.result).resolve(),
    )
    print(json.dumps(summary, indent=2))
    return 0


def command_review_reconcile(args: argparse.Namespace) -> int:
    output = reconcile_review(
        Path(args.control).resolve(),
        Path(args.packet).resolve(),
        Path(args.result).resolve(),
        Path(args.output).resolve(),
    )
    print(json.dumps(output, indent=2))
    return 0


def command_review_audit(args: argparse.Namespace) -> int:
    questions = read_json(Path(args.questions))["questions"]
    accepted = [item["question_id"] for item in questions if item.get("curation_state") == "accepted"]
    paths = [Path(value) for value in args.reconciliation]
    output = audit_review_coverage(accepted, paths)
    print(json.dumps(output, indent=2))
    return 0 if output["ready"] else 2


def command_review_accept(args: argparse.Namespace) -> int:
    result = accept_reviewed_questions(
        Path(args.questions), [Path(value) for value in args.reconciliation],
        Path(args.adjudication) if args.adjudication else None, Path(args.output),
    )
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "accepted" else 2


def command_ingest(args: argparse.Namespace) -> int:
    root, output, source_corpus, _ = paths(args)
    if args.pack:
        pack = load_corpus_pack(root, args.pack)
        records = []
        chunks = []
        passages = []
        for source_id in pack.manifest["active_source_ids"]:
            source = next(item for item in pack.source_register["sources"] if item["source_id"] == source_id)
            path = root / source["processed_path"]
            if not path.exists():
                raise FileNotFoundError(f"approved processed source missing for {source_id}: {path}")
            text = path.read_text(encoding="utf-8")
            descriptor = SourceDescriptor(source_id, source["author"], source["work"], source["translator"], source["edition_year"])
            built_passages = build_passages(text, descriptor)
            built_chunks = build_chunks(built_passages, chunker_id=pack.manifest["chunker_id"])
            passages.extend(built_passages)
            chunks.extend(built_chunks)
            records.append({"source_id": source_id, "processed_path": source["processed_path"], "text_sha256": sha256_text(text), "passage_count": len(built_passages), "chunk_count": len(built_chunks)})
        corpus = {"schema_version": "v0.3-corpus-1.0", "pack_id": pack.pack_id, "sources": records, "passages": passages, "chunks": chunks}
        output.mkdir(parents=True, exist_ok=True)
        write_json(output / "corpus.v1.json", corpus)
        write_json(output / "manifest.v1.json", pack.manifest)
        print(output / "corpus.v1.json")
        return 0
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


def command_ask(args: argparse.Namespace) -> int:
    root, output, source_corpus, _ = paths(args)
    corpus_path = output / "corpus.v1.json" if (output / "corpus.v1.json").exists() else source_corpus
    corpus = read_json(corpus_path)
    validate_corpus(corpus)
    results = Retriever(corpus["chunks"]).search(args.question, args.method, args.top_k)
    print(f"Question: {args.question}\n")
    if not results:
        print("No grounded evidence found; refusing to invent an answer.")
        return 0
    if args.generate == "fake":
        generated = grounded_answer(args.question, results, corpus, FakeModelAdapter())
        print(f"\nAnswer: {generated['answer']}")
        print("Citations: " + ", ".join(generated["citations"]))
    print("Grounded evidence (generation intentionally optional):")
    by_id = {chunk["chunk_id"]: chunk for chunk in corpus["chunks"]}
    for index, result in enumerate(results, 1):
        chunk = by_id[result.chunk_id]
        print(f"\n[{index}] {chunk.get('author', chunk['source_id'])} — {result.chunk_id}")
        print(chunk["text"][:900].strip())
    return 0


def command_derive_relevance(args: argparse.Namespace) -> int:
    questions = read_json(Path(args.questions))["questions"]
    corpus = read_json(Path(args.corpus))
    payload = {"schema_version": "v0.3-derived-relevance-1.0", "question_dataset_id": read_json(Path(args.questions)).get("dataset_id"), "relevance": derive_relevance(questions, corpus["chunks"])}
    write_json(Path(args.output), payload)
    print(args.output)
    return 0


def command_evaluate_v2(args: argparse.Namespace) -> int:
    corpus = read_json(Path(args.corpus))
    questions = read_json(Path(args.questions))["questions"]
    result = evaluate_questions_v2(corpus, questions, method=args.method, top_k=args.top_k)
    write_json(Path(args.output), result)
    print(args.output)
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
    result.add_argument("--pack", help="explicit v0.3 corpus pack ID")
    commands = result.add_subparsers(dest="command", required=True)
    validate_pack = commands.add_parser("validate-pack", help="validate an explicit corpus pack")
    validate_pack.add_argument("pack_id", nargs="?", help="pack ID when --pack is not provided")
    validate_pack.set_defaults(function=command_validate_pack)
    review = commands.add_parser("review", help="create and validate blinded review artifacts")
    review_commands = review.add_subparsers(dest="review_command", required=True)
    review_export = review_commands.add_parser("export", help="export a blinded review packet")
    review_export.add_argument("--request", required=True)
    review_export.add_argument("--items", required=True)
    review_export.add_argument("--evidence", required=True)
    review_export.add_argument("--output", required=True)
    review_export.set_defaults(function=command_review_export)
    review_packet = review_commands.add_parser("validate-packet")
    review_packet.add_argument("packet")
    review_packet.set_defaults(function=command_review_validate_packet)
    review_result = review_commands.add_parser("validate-result")
    review_result.add_argument("packet")
    review_result.add_argument("result")
    review_result.set_defaults(function=command_review_validate_result)
    review_reconcile = review_commands.add_parser("reconcile")
    review_reconcile.add_argument("--control", required=True)
    review_reconcile.add_argument("--packet", required=True)
    review_reconcile.add_argument("--result", required=True)
    review_reconcile.add_argument("--output", required=True)
    review_reconcile.set_defaults(function=command_review_reconcile)
    review_audit = review_commands.add_parser("audit", help="audit review coverage without mutating controls")
    review_audit.add_argument("--questions", required=True)
    review_audit.add_argument("--reconciliation", action="append", default=[])
    review_audit.set_defaults(function=command_review_audit)
    review_accept = review_commands.add_parser("accept", help="promote only reconciled/adjudicated question candidates")
    review_accept.add_argument("--questions", required=True)
    review_accept.add_argument("--reconciliation", action="append", default=[])
    review_accept.add_argument("--adjudication")
    review_accept.add_argument("--output", required=True)
    review_accept.set_defaults(function=command_review_accept)
    ingest = commands.add_parser("ingest", help="validate provenance and materialize a corpus contract")
    ingest.set_defaults(function=command_ingest)
    retrieve = commands.add_parser("retrieve", help="retrieve ranked evidence for one query")
    retrieve.add_argument("query")
    retrieve.add_argument("--method", choices=["keyword", "bm25", "vector", "hybrid"], default="bm25")
    retrieve.add_argument("--top-k", type=int, default=5)
    retrieve.set_defaults(function=command_retrieve)
    ask = commands.add_parser("ask", help="show grounded evidence for an interactive question")
    ask.add_argument("question")
    ask.add_argument("--method", choices=["keyword", "bm25", "vector", "hybrid"], default="bm25")
    ask.add_argument("--top-k", type=int, default=5)
    ask.add_argument("--generate", choices=["none", "fake"], default="none")
    ask.set_defaults(function=command_ask)
    derived = commands.add_parser("derive-relevance", help="derive chunk judgments from canonical passage anchors")
    derived.add_argument("--questions", required=True)
    derived.add_argument("--corpus", required=True)
    derived.add_argument("--output", required=True)
    derived.set_defaults(function=command_derive_relevance)
    evaluate_v2 = commands.add_parser("evaluate-v2", help="evaluate passage-anchored v0.3 question candidates")
    evaluate_v2.add_argument("--questions", required=True)
    evaluate_v2.add_argument("--corpus", required=True)
    evaluate_v2.add_argument("--output", required=True)
    evaluate_v2.add_argument("--method", choices=["keyword", "bm25", "vector", "hybrid"], default="bm25")
    evaluate_v2.add_argument("--top-k", type=int, default=5)
    evaluate_v2.set_defaults(function=command_evaluate_v2)
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
        if args.command == "validate-pack":
            args.pack = args.pack or args.pack_id
            if not args.pack:
                raise ValueError("validate-pack requires --pack or a pack ID")
        return args.function(args)
    except (ContractError, ReviewContractError, FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
