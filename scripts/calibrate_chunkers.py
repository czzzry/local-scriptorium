"""Offline chunker calibration report for an acquired corpus pack."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from local_scriptorium.ingestion import SourceDescriptor, build_chunks, build_passages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", action="append", nargs=5, required=True,
                        metavar=("ID", "PATH", "AUTHOR", "WORK", "TRANSLATOR"))
    args = parser.parse_args()
    configs = [("paragraph-window-300-v1", 300, 500), ("paragraph-window-500-v1", 500, 750), ("paragraph-window-700-v1", 700, 1000)]
    rows = []
    for chunker_id, target, maximum in configs:
        chunks = []
        for source_id, path, author, work, translator in args.source:
            text = Path(path).read_text(encoding="utf-8")
            passages = build_passages(text, SourceDescriptor(source_id, author, work, translator, 1900))
            chunks.extend(build_chunks(passages, chunker_id=chunker_id, target_words=target, max_words=maximum))
        counts = [int(chunk["word_count"]) for chunk in chunks]
        rows.append({"chunker_id": chunker_id, "target_words": target, "max_words": maximum,
                     "chunk_count": len(chunks), "mean_words": round(sum(counts) / len(counts), 2),
                     "max_observed_words": max(counts), "outlier_count": sum(value > maximum for value in counts),
                     "source_ids": sorted({chunk["source_id"] for chunk in chunks})})
    payload = {"schema_version": "v0.3-chunker-calibration-1.0", "selection_rule": "record stats; do not select on held-out questions", "configurations": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
