"""Derive human-readable reports from raw result artifacts."""

from __future__ import annotations

import csv
import html
import io
import re
from pathlib import Path


def retrieval_csv(results: dict) -> str:
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["method", "recall@5", "precision@5", "hit_rate@5", "mrr", "ndcg@5"])
    for method, value in results["methods"].items():
        summary = value["summary"]
        writer.writerow([method, *(f"{summary[key]:.6f}" for key in ("recall@5", "precision@5", "hit_rate@5", "mrr", "ndcg@5"))])
    return stream.getvalue()


def retrieval_details_csv(results: dict) -> str:
    """Return one row per retrieved chunk with judgments and query metrics."""
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([
        "method", "question_id", "rank", "chunk_id", "score", "relevance_grade",
        "failure", "recall", "precision", "hit_rate", "mrr", "ndcg",
    ])
    k = results["top_k"]
    for method, value in results["methods"].items():
        for row in value["questions"]:
            metrics = row["metrics"]
            for result in row["retrieved"]:
                writer.writerow([
                    method, row["question_id"], result["rank"], result["chunk_id"],
                    f"{result['score']:.12f}", row["relevance"].get(result["chunk_id"], 0),
                    row["failure"], f"{metrics[f'recall@{k}']:.6f}",
                    f"{metrics[f'precision@{k}']:.6f}", f"{metrics[f'hit_rate@{k}']:.6f}",
                    f"{metrics['mrr']:.6f}", f"{metrics[f'ndcg@{k}']:.6f}",
                ])
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
            f"- Dataset: `{results['dataset_id']}` (`{results['split']}` split)",
            f"- Corpus: `{results['corpus_id']}`",
            f"- Harness version: `{metadata['harness_version']}`",
            f"- Corpus checksum: `{metadata['corpus_checksum_sha256']}`",
            f"- Revision: `{metadata['revision']}`",
            f"- Seed: `{metadata['seed']}`",
            f"- Timestamp: `{metadata['timestamp']}`",
            f"- Python: `{metadata['runtime']['python']}`",
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
    definitions = {
        "complete_miss": "no judged evidence retrieved in the top k",
        "partial_evidence": "some but not all judged evidence retrieved",
        "low_rank": "all evidence retrieved but the first hit ranks below position two",
        "distractor_heavy": "all evidence retrieved with less than 0.2 precision",
        "none": "none of the defined failure conditions occurred",
    }
    lines.extend(
        f"- `{name}`: {count} — {definitions[name]}" for name, count in sorted(failures.items())
    )
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
    """Render the report's constrained Markdown subset without external dependencies."""

    def inline(value: str) -> str:
        escaped = html.escape(value)
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)

    lines = markdown.splitlines()
    body: list[str] = []
    index = 0
    in_code = False
    code: list[str] = []
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            if in_code:
                body.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
                code = []
            in_code = not in_code
            index += 1
            continue
        if in_code:
            code.append(line)
            index += 1
            continue
        if line.startswith("# "):
            body.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            body.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("| ") and index + 1 < len(lines) and lines[index + 1].startswith("|---"):
            headers = [cell.strip() for cell in line.strip("|").split("|")]
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].startswith("|"):
                rows.append([cell.strip() for cell in lines[index].strip("|").split("|")])
                index += 1
            body.append("<div class='table-wrap'><table><thead><tr>" + "".join(f"<th>{inline(cell)}</th>" for cell in headers) + "</tr></thead><tbody>")
            body.extend("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>" for row in rows)
            body.append("</tbody></table></div>")
            continue
        elif line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].startswith("- "):
                items.append(lines[index][2:])
                index += 1
            body.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>")
            continue
        elif line.strip():
            paragraph = [line.strip()]
            while index + 1 < len(lines) and lines[index + 1].strip() and not lines[index + 1].startswith(("#", "- ", "|", "```")):
                index += 1
                paragraph.append(lines[index].strip())
            body.append(f"<p>{inline(' '.join(paragraph))}</p>")
        index += 1

    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Local Scriptorium evaluation report</title><style>"
        ":root{color-scheme:light dark;--bg:#f8f5ee;--card:#fff;--ink:#17201c;--muted:#526158;"
        "--line:#d9ddd8;--accent:#235c45}*{box-sizing:border-box}body{margin:0;background:var(--bg);"
        "color:var(--ink);font:16px/1.6 system-ui,-apple-system,sans-serif}main{max-width:1080px;"
        "margin:0 auto;padding:3rem 1.25rem 5rem}h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.05;"
        "margin:0 0 2rem;color:var(--accent)}h2{margin-top:2.75rem;border-bottom:1px solid var(--line);"
        "padding-bottom:.45rem}p,li{max-width:78ch}.table-wrap{overflow:auto;background:var(--card);"
        "border:1px solid var(--line);border-radius:12px}table{width:100%;border-collapse:collapse}"
        "th,td{text-align:left;padding:.75rem;border-bottom:1px solid var(--line);white-space:nowrap}"
        "th{background:#eaf0eb}code{background:#e6ebe7;padding:.12rem .32rem;border-radius:4px}"
        "pre{overflow:auto;background:#17201c;color:#f4f1e9;padding:1rem;border-radius:10px}"
        "pre code{background:transparent;padding:0}@media(prefers-color-scheme:dark){:root{--bg:#101512;"
        "--card:#18201b;--ink:#edf3ee;--muted:#aab7ae;--line:#36443a;--accent:#8ad0aa}"
        "th{background:#223128}code{background:#29372e}}</style></head><body><main>"
        + "".join(body)
        + "</main></body></html>\n"
    )


def write_reports(output: Path, results: dict, answers: dict, metadata: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    markdown = markdown_report(results, answers, metadata)
    (output / "report.md").write_text(markdown, encoding="utf-8")
    (output / "report.html").write_text(html_report(markdown), encoding="utf-8")
    (output / "retrieval_summary.csv").write_text(retrieval_csv(results), encoding="utf-8")
    (output / "retrieval_details.csv").write_text(retrieval_details_csv(results), encoding="utf-8")
