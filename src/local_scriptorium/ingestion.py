"""Deterministic v0.3 source normalization, passage, and chunk builders."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def remove_gutenberg_wrapper(text: str) -> str:
    """Return the book body, excluding Project Gutenberg distribution text."""
    lines = text.splitlines()
    start = next(
        (i + 1 for i, line in enumerate(lines) if "*** START OF" in line.upper()),
        0,
    )
    end = next(
        (i for i, line in enumerate(lines[start:], start=start)
         if "*** END OF" in line.upper() or "END OF PROJECT GUTENBERG" in line.upper()),
        len(lines),
    )
    return "\n".join(line.rstrip() for line in lines[start:end]).strip()


def _without_frontmatter(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    if not lines or lines[0].strip() != "---":
        return lines, {}
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return lines, {}
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return lines[end + 1 :], metadata


def paragraphs(text: str) -> list[dict[str, object]]:
    """Split normalized text into stable, line-addressable paragraphs."""
    raw_lines, metadata = _without_frontmatter(text.splitlines())
    result: list[dict[str, object]] = []
    current: list[str] = []
    start: int | None = None

    def flush(end: int) -> None:
        nonlocal current, start
        if current and start is not None:
            body = "\n".join(current).strip()
            if body:
                result.append({"text": body, "start_line": start, "end_line": end,
                               "word_count": len(re.findall(r"\S+", body)),
                               "metadata": metadata})
        current, start = [], None

    for number, line in enumerate(raw_lines, start=1):
        if not line.strip():
            flush(number - 1)
        else:
            if start is None:
                start = number
            current.append(line.rstrip())
    flush(len(raw_lines))
    return result


@dataclass(frozen=True)
class SourceDescriptor:
    source_id: str
    author: str
    work: str
    translator: str
    edition_year: int
    content_kind: str = "primary_text"


def build_passages(text: str, source: SourceDescriptor) -> list[dict[str, object]]:
    """Build canonical passages; IDs are based on source and source line span."""
    built = []
    for index, paragraph in enumerate(paragraphs(text), start=1):
        body = str(paragraph["text"])
        start = int(paragraph["start_line"])
        end = int(paragraph["end_line"])
        passage_id = f"{source.source_id}:p{index:04d}:l{start}-{end}"
        built.append({
            "passage_id": passage_id,
            "source_id": source.source_id,
            "author": source.author,
            "work": source.work,
            "translator": source.translator,
            "edition_year": source.edition_year,
            "content_kind": source.content_kind,
            "locator": {"start_line": start, "end_line": end},
            "text": body,
            "text_sha256": sha256_text(body),
            "predecessor_id": built[-1]["passage_id"] if built else None,
        })
    for current, following in zip(built, built[1:]):
        current["successor_id"] = following["passage_id"]
    if built:
        built[-1]["successor_id"] = None
    return built


def build_chunks(passages: Iterable[dict[str, object]], *, chunker_id: str = "paragraph-window-v1",
                 target_words: int = 500, max_words: int = 750) -> list[dict[str, object]]:
    """Combine adjacent passages without crossing a source boundary."""
    chunks: list[dict[str, object]] = []
    current: list[dict[str, object]] = []
    words = 0

    def flush() -> None:
        nonlocal current, words
        if not current:
            return
        text = "\n\n".join(str(item["text"]) for item in current)
        first, last = current[0], current[-1]
        source_id = str(first["source_id"])
        chunk_id = f"{source_id}:c{len([c for c in chunks if c['source_id'] == source_id]) + 1:04d}"
        chunks.append({
            "chunk_id": chunk_id,
            "chunker_id": chunker_id,
            "source_id": source_id,
            "author": first["author"], "work": first["work"],
            "translator": first["translator"], "edition_year": first["edition_year"],
            "content_kind": first["content_kind"],
            "first_passage_id": first["passage_id"],
            "last_passage_id": last["passage_id"],
            "start_line": first["locator"]["start_line"],
            "end_line": last["locator"]["end_line"],
            "passage_ids": [item.get("canonical_passage_id", item["passage_id"]) for item in current],
            "text": text,
            "text_sha256": sha256_text(text),
            "word_count": len(re.findall(r"\S+", text)),
        })
        current, words = [], 0

    for passage in passages:
        count = len(re.findall(r"\S+", str(passage["text"])))
        if current and passage["source_id"] != current[0]["source_id"]:
            flush()
        if count > max_words:
            # Deterministic fallback for an oversized structural passage. The
            # passage remains the scholarly anchor; only its retrieval text is
            # split into numbered fragments.
            if current:
                flush()
            words_in_passage = str(passage["text"]).split()
            for offset in range(0, len(words_in_passage), max_words):
                fragment = dict(passage)
                fragment["text"] = " ".join(words_in_passage[offset:offset + max_words])
                fragment["passage_id"] = f"{passage['passage_id']}:f{offset // max_words + 1:03d}"
                fragment["canonical_passage_id"] = passage["passage_id"]
                current.append(fragment)
                words = len(words_in_passage[offset:offset + max_words])
                flush()
            continue
        if current and words + count > max_words:
            flush()
        current.append(passage)
        words += count
        if words >= target_words:
            flush()
    flush()
    return chunks
