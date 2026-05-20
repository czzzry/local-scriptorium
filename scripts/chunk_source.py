import json
import re
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]

SOURCE_ID = "BOETHIUS_CONSOLATION_001"
SOURCE_PATH = ROOT / "sources_public" / "processed" / "boethius_consolation_james_clean.md"
OUTPUT_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"

TARGET_WORDS = 500
MIN_WORDS = 250
MAX_WORDS = 750


def count_words(text: str) -> int:
    """Return a rough word count."""
    return len(re.findall(r"\b\S+\b", text))


def strip_frontmatter(lines: list[str]) -> list[tuple[int, str]]:
    """
    Remove YAML frontmatter from the top of the file, if present.

    Returns a list of:
    (original_line_number, line_text)

    We keep original line numbers so chunks can be traced back to the cleaned source.
    """
    numbered_lines = list(enumerate(lines, start=1))

    if not numbered_lines:
        return []

    first_line = numbered_lines[0][1].strip()

    if first_line != "---":
        return numbered_lines

    for index, (_, line) in enumerate(numbered_lines[1:], start=1):
        if line.strip() == "---":
            return numbered_lines[index + 1 :]

    return numbered_lines


def split_into_paragraphs(numbered_lines: list[tuple[int, str]]) -> list[dict]:
    """
    Split source text into paragraphs.

    A paragraph is one or more non-blank lines separated by blank lines.
    We preserve start/end line numbers for traceability.
    """
    paragraphs = []

    current_lines = []
    current_start_line = None
    current_end_line = None

    for line_number, line in numbered_lines:
        stripped = line.rstrip()

        if stripped == "":
            if current_lines:
                paragraphs.append(
                    {
                        "text": "\n".join(current_lines).strip(),
                        "start_line": current_start_line,
                        "end_line": current_end_line,
                        "word_count": count_words("\n".join(current_lines)),
                    }
                )
                current_lines = []
                current_start_line = None
                current_end_line = None
            continue

        if current_start_line is None:
            current_start_line = line_number

        current_lines.append(stripped)
        current_end_line = line_number

    if current_lines:
        paragraphs.append(
            {
                "text": "\n".join(current_lines).strip(),
                "start_line": current_start_line,
                "end_line": current_end_line,
                "word_count": count_words("\n".join(current_lines)),
            }
        )

    return paragraphs


def should_force_standalone(paragraph_text: str) -> bool:
    """
    Return True when a paragraph should become its own chunk.

    Headings and separators are not very useful alone, so for MVP we do NOT
    force them into standalone chunks. This function exists so the rule can
    evolve later.
    """
    return False


def combine_paragraphs_into_chunks(paragraphs: list[dict]) -> list[dict]:
    """
    Combine paragraphs into chunks.

    Rule:
    - Prefer chunks around TARGET_WORDS.
    - Do not exceed MAX_WORDS unless a single paragraph is already huge.
    - Avoid tiny chunks where possible.
    - Preserve paragraph breaks.
    """
    chunks = []

    current_parts = []
    current_start_line = None
    current_end_line = None
    current_word_count = 0

    def flush_current():
        nonlocal current_parts, current_start_line, current_end_line, current_word_count

        if not current_parts:
            return

        chunks.append(
            {
                "text": "\n\n".join(current_parts).strip(),
                "start_line": current_start_line,
                "end_line": current_end_line,
                "word_count": current_word_count,
            }
        )

        current_parts = []
        current_start_line = None
        current_end_line = None
        current_word_count = 0

    for paragraph in paragraphs:
        paragraph_text = paragraph["text"]
        paragraph_words = paragraph["word_count"]

        if should_force_standalone(paragraph_text):
            flush_current()
            chunks.append(paragraph)
            continue

        would_exceed_max = current_word_count + paragraph_words > MAX_WORDS
        current_is_large_enough = current_word_count >= MIN_WORDS

        if would_exceed_max and current_is_large_enough:
            flush_current()

        if current_start_line is None:
            current_start_line = paragraph["start_line"]

        current_parts.append(paragraph_text)
        current_end_line = paragraph["end_line"]
        current_word_count += paragraph_words

        if current_word_count >= TARGET_WORDS:
            flush_current()

    flush_current()

    return chunks


def add_chunk_ids(chunks: list[dict]) -> list[dict]:
    """Add stable chunk IDs and source IDs."""
    chunked = []

    for index, chunk in enumerate(chunks, start=1):
        chunk_id = f"{SOURCE_ID}_CHUNK_{index:03d}"

        chunked.append(
            {
                "chunk_id": chunk_id,
                "source_id": SOURCE_ID,
                "chunk_index": index,
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "word_count": chunk["word_count"],
                "text": chunk["text"],
            }
        )

    return chunked


def write_chunks(chunks: list[dict]) -> None:
    """Write chunks to JSON."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "source_id": SOURCE_ID,
        "source_file": str(SOURCE_PATH.relative_to(ROOT)),
        "chunking_method": "paragraph_combination",
        "target_words": TARGET_WORDS,
        "min_words": MIN_WORDS,
        "max_words": MAX_WORDS,
        "chunk_count": len(chunks),
        "chunks": chunks,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def print_summary(chunks: list[dict]) -> None:
    """Print a useful summary after chunking."""
    word_counts = [chunk["word_count"] for chunk in chunks]

    print("Chunking complete.")
    print(f"Source: {SOURCE_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Chunk count: {len(chunks)}")

    if word_counts:
        print(f"Min words: {min(word_counts)}")
        print(f"Max words: {max(word_counts)}")
        print(f"Average words: {mean(word_counts):.1f}")

    print()
    print("First 3 chunk IDs:")
    for chunk in chunks[:3]:
        print(
            f"- {chunk['chunk_id']} "
            f"(lines {chunk['start_line']}-{chunk['end_line']}, "
            f"{chunk['word_count']} words)"
        )


def main() -> None:
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE_PATH}")

    raw_text = SOURCE_PATH.read_text(encoding="utf-8")
    lines = raw_text.splitlines()

    content_lines = strip_frontmatter(lines)
    paragraphs = split_into_paragraphs(content_lines)
    chunks_without_ids = combine_paragraphs_into_chunks(paragraphs)
    chunks = add_chunk_ids(chunks_without_ids)

    write_chunks(chunks)
    print_summary(chunks)


if __name__ == "__main__":
    main()