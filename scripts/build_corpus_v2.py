"""Build canonical passages and chunks for a small v0.3 tracer selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from local_scriptorium.ingestion import SourceDescriptor, build_chunks, build_passages, sha256_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--source", action="append", nargs=5, metavar=("ID", "PATH", "AUTHOR", "WORK", "TRANSLATOR"), required=True)
    args = parser.parse_args()
    all_passages: list[dict[str, object]] = []
    all_chunks: list[dict[str, object]] = []
    source_records = []
    for source_id, path, author, work, translator in args.source:
        source_path = Path(path)
        text = source_path.read_text(encoding="utf-8")
        descriptor = SourceDescriptor(source_id, author, work, translator, 1895 if source_id.startswith("IAMBLICHUS") else 1897)
        passages = build_passages(text, descriptor)
        chunks = build_chunks(passages)
        all_passages.extend(passages)
        all_chunks.extend(chunks)
        source_records.append({"source_id": source_id, "path": str(source_path), "text_sha256": sha256_text(text), "passage_count": len(passages), "chunk_count": len(chunks)})
    payload = {"schema_version": "v0.3-corpus-1.0", "sources": source_records, "passages": all_passages, "chunks": all_chunks}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {output} ({len(all_passages)} passages, {len(all_chunks)} chunks)")


if __name__ == "__main__":
    main()
