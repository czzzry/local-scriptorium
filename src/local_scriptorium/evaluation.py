"""Offline retrieval and grounded-answer evaluation orchestration."""

from __future__ import annotations

import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import __version__
from .contracts import SCHEMA_VERSION, sha256_file
from .metrics import aggregate, bootstrap_ci, query_metrics
from .retrieval import Retriever


def revision(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def run_metadata(root: Path, corpus_path: Path, seed: int, deterministic: bool) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "harness_version": __version__,
        "configuration": {"top_k": 5, "methods": ["keyword", "bm25", "vector", "hybrid"]},
        "seed": seed,
        "revision": revision(root),
        "timestamp": "normalized-for-reproducibility" if deterministic else datetime.now(UTC).isoformat(),
        "runtime": {"python": platform.python_version(), "platform": "normalized" if deterministic else platform.platform()},
        "corpus_checksum_sha256": sha256_file(corpus_path),
    }


def classify_failure(metrics: dict[str, float], k: int) -> str:
    if metrics[f"recall@{k}"] == 0:
        return "complete_miss"
    if metrics[f"recall@{k}"] < 1:
        return "partial_evidence"
    if metrics["mrr"] < 0.5:
        return "low_rank"
    if metrics[f"precision@{k}"] < 0.2:
        return "distractor_heavy"
    return "none"


def evaluate_retrieval(corpus: dict, questions: dict, split: str, k: int = 5, seed: int = 42) -> dict:
    retriever = Retriever(corpus["chunks"])
    selected = [q for q in questions["questions"] if q["split"] == split]
    methods: dict[str, Any] = {}
    for method in ("keyword", "bm25", "vector", "hybrid"):
        rows = []
        for question in selected:
            ranked = retriever.search(question["question"], method, k)
            metrics = query_metrics([item.chunk_id for item in ranked], question["relevance"], k)
            rows.append(
                {
                    "question_id": question["question_id"],
                    "retrieved": [item.chunk_id for item in ranked],
                    "metrics": metrics,
                    "failure": classify_failure(metrics, k),
                }
            )
        summary = aggregate([row["metrics"] for row in rows])
        uncertainty = {
            name: {"low": bootstrap_ci([row["metrics"][name] for row in rows], seed)[0], "high": bootstrap_ci([row["metrics"][name] for row in rows], seed)[1]}
            for name in summary
        }
        methods[method] = {"summary": summary, "confidence_intervals_95": uncertainty, "questions": rows}
    return {"schema_version": SCHEMA_VERSION, "split": split, "top_k": k, "methods": methods}


def evaluate_answers(fixtures: dict) -> dict:
    results = []
    for item in fixtures["answers"]:
        citations = set(item["citations"])
        available = set(item["retrieved_chunk_ids"])
        unsupported = item["unsupported_claims"]
        should_refuse = not item["answerable"]
        refused = item["response_type"] == "refusal"
        results.append(
            {
                "answer_id": item["answer_id"],
                "citation_correctness": float(bool(citations) and citations <= available) if item["answerable"] else float(not citations),
                "faithful": float(not unsupported),
                "unsupported_claim_count": len(unsupported),
                "answerability_correct": float(should_refuse == refused),
                "correct_refusal": float(refused) if should_refuse else None,
            }
        )
    numeric = ["citation_correctness", "faithful", "unsupported_claim_count", "answerability_correct"]
    summary = {key: sum(row[key] for row in results) / len(results) for key in numeric}
    refusals = [row["correct_refusal"] for row in results if row["correct_refusal"] is not None]
    summary["correct_refusal"] = sum(refusals) / len(refusals) if refusals else 0.0
    return {
        "schema_version": SCHEMA_VERSION,
        "evaluator": "deterministic_fixture_checks_v1; labels are curated heuristics, not objective truth",
        "summary": summary,
        "answers": results,
    }


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

