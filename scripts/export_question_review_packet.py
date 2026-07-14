"""Create a blinded question-evidence review packet from candidate artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from local_scriptorium.reviewing import export_review_packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--review-id", default="late-antiquity-candidate-calibration-001")
    args = parser.parse_args()
    questions = json.loads(args.questions.read_text(encoding="utf-8"))["questions"][args.offset:args.offset + args.limit]
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    passage_to_chunks: dict[str, list[dict]] = {}
    for chunk in corpus["chunks"]:
        for passage_id in chunk.get("passage_ids", []):
            passage_to_chunks.setdefault(passage_id, []).append(chunk)
    items = []
    evidence = []
    for question in questions:
        item_id = question["question_id"]
        items.append({"item_id": item_id, "question": question["question"], "question_type": question["question_type"]})
        refs = []
        for passage_id in question["canonical_passage_ids"]:
            refs.extend(chunk["chunk_id"] for chunk in passage_to_chunks.get(passage_id, []))
        for chunk_id in dict.fromkeys(refs):
            chunk = next(c for c in corpus["chunks"] if c["chunk_id"] == chunk_id)
            evidence.append({"evidence_id": f"{item_id}:{chunk_id}", "item_id": item_id, "source_id": chunk["source_id"], "text": chunk["text"], "locator": {"start_line": chunk["start_line"], "end_line": chunk["end_line"]}, "evidence_refs": [chunk_id]})
    request = {"schema_version": "1.0", "review_id": args.review_id, "review_kind": "question_evidence", "protocol_version": "1.0", "pack_id": corpus.get("pack_id", "unknown"), "independence_level": "I1", "external_context_allowed": False, "randomization_seed": 20260713 + args.offset}
    summary = export_review_packet(args.output, request, items, evidence)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
