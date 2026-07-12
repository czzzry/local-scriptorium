"""Derive human-readable reports from raw result artifacts."""

from __future__ import annotations

import csv
import html
import io
from pathlib import Path


def retrieval_csv(results: dict) -> str:
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["method", "recall@5", "precision@5", "hit_rate@5", "mrr", "ndcg@5"])
    for method, value in results["methods"].items():
        summary = value["summary"]
        writer.writerow([method, *(f"{summary[key]:.6f}" for key in ("recall@5", "precision@5", "hit_rate@5", "mrr", "ndcg@5"))])
    return stream.getvalue()


def markdown_report(results: dict, answers: dict, metadata: dict) -> str:
    lines = [
        "# Local Scriptorium Evaluation Report",
        "",
        "## Results at a glance",
        "",
        "| Method | Recall@5 | Precision@5 | Hit rate@5 | MRR | nDCG@5 | Recall 95% CI |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for method, value in results["methods"].items():
        metric = value["summary"]
        ci = value["confidence_intervals_95"]["recall@5"]
        lines.append(
            f"| {method} | {metric['recall@5']:.3f} | {metric['precision@5']:.3f} | "
            f"{metric['hit_rate@5']:.3f} | {metric['mrr']:.3f} | {metric['ndcg@5']:.3f} | "
            f"[{ci['low']:.3f}, {ci['high']:.3f}] |"
        )
    answer = answers["summary"]
    failures: dict[str, int] = {}
    for method in results["methods"].values():
        for row in method["questions"]:
            failures[row["failure"]] = failures.get(row["failure"], 0) + 1
    lines.extend(
        [
            "",
            "## Methodology",
            "",
            f"This report evaluates the held-out `{results['split']}` split at k={results['top_k']}. "
            "Relevance judgments are manually curated and graded 1–3. Confidence intervals are "
            "2,000-sample seeded non-parametric bootstrap intervals over questions.",
            "",
            "The `vector` method is an offline TF-IDF cosine baseline. It preserves a vector-style "
            "comparison without requiring Ollama; it is not a dense semantic embedding model. Hybrid "
            "uses reciprocal-rank fusion of BM25 and that vector baseline.",
            "",
            "## Corpus and run",
            "",
            f"- Contract version: `{metadata['schema_version']}`",
            f"- Harness version: `{metadata['harness_version']}`",
            f"- Corpus checksum: `{metadata['corpus_checksum_sha256']}`",
            f"- Revision: `{metadata['revision']}`",
            f"- Seed: `{metadata['seed']}`",
            "",
            "## Grounded-answer checks",
            "",
            f"- Citation correctness: {answer['citation_correctness']:.3f}",
            f"- Fixture faithfulness: {answer['faithful']:.3f}",
            f"- Mean unsupported claims: {answer['unsupported_claim_count']:.3f}",
            f"- Answerability classification: {answer['answerability_correct']:.3f}",
            f"- Correct refusal on unanswerable fixtures: {answer['correct_refusal']:.3f}",
            "",
            "These deterministic checks operate on curated fixture labels. They are useful regression "
            "signals, not objective ground truth and not a substitute for expert review.",
            "",
            "## Retrieval failure taxonomy",
            "",
        ]
    )
    lines.extend(f"- `{name}`: {count}" for name, count in sorted(failures.items()))
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- One public-domain work and one historical English translation limit generalizability.",
            "- Questions and relevance judgments have not received independent scholarly adjudication.",
            "- The test split is protected by convention and CLI defaults, not an access-control system.",
            "- Offline TF-IDF vectors do not measure dense embedding quality.",
            "- Bootstrap intervals quantify question-sampling uncertainty only.",
            "",
            "## Exact reproduction",
            "",
            "```bash",
            "python -m pip install -e .",
            "scriptorium ingest",
            "scriptorium evaluate --split test --deterministic",
            "scriptorium report",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def html_report(markdown: str) -> str:
    # Deliberately tiny, self-contained rendering: preserve exact report text safely.
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width'><title>Local Scriptorium report</title>"
        "<style>body{font:16px/1.55 system-ui;max-width:980px;margin:3rem auto;padding:0 1rem;}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:1.25rem;border-radius:8px}</style></head>"
        f"<body><pre>{html.escape(markdown)}</pre></body></html>\n"
    )


def write_reports(output: Path, results: dict, answers: dict, metadata: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    markdown = markdown_report(results, answers, metadata)
    (output / "report.md").write_text(markdown, encoding="utf-8")
    (output / "report.html").write_text(html_report(markdown), encoding="utf-8")
    (output / "retrieval_summary.csv").write_text(retrieval_csv(results), encoding="utf-8")
