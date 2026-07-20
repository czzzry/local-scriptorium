"""Produce a compact v0.3 development report with source and question slices."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--evaluation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    questions = json.loads(args.questions.read_text(encoding="utf-8"))["questions"]
    evaluation = json.loads(args.evaluation.read_text(encoding="utf-8"))
    sources = Counter(chunk.get("author", chunk["source_id"]) for chunk in corpus["chunks"])
    types = Counter(question["question_type"] for question in questions)
    lines = ["# Local Scriptorium v0.3 development report", "", f"Pack: `{corpus.get('pack_id', 'unknown')}`", f"Passages: {len(corpus.get('passages', []))}", f"Chunks: {len(corpus['chunks'])}", "", "## Chunk distribution by author", "", "| Author | Chunks |", "|---|---:|"]
    lines.extend(f"| {author} | {count} |" for author, count in sorted(sources.items()))
    lines += ["", "## Candidate question distribution", "", "| Type | Count |", "|---|---:|"]
    lines.extend(f"| {kind} | {count} |" for kind, count in sorted(types.items()))
    lines += ["", "## Development retrieval result", "", f"- Method: `{evaluation['method']}`", f"- k: {evaluation['top_k']}", f"- Answerable denominator: {evaluation['answerable_count']}", f"- Hit-rate-like development diagnostic: {evaluation['recall_like_hit_rate']}", "", "This is a candidate diagnostic, not a released held-out benchmark score."]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
