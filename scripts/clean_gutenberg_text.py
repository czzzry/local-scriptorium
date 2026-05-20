from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = ROOT / "sources_public" / "raw" / "boethius_consolation_james.txt"
OUTPUT_PATH = ROOT / "sources_public" / "processed" / "boethius_consolation_james_clean.md"

SOURCE_ID = "BOETHIUS_CONSOLATION_001"
TITLE = "The Consolation of Philosophy"
AUTHOR = "Boethius"
TRANSLATOR = "H. R. James"


def remove_gutenberg_header_footer(text: str) -> str:
    """
    Remove common Project Gutenberg header/footer material.

    Gutenberg files are not perfectly consistent. Some use lines like:
    *** START OF THE PROJECT GUTENBERG EBOOK ...
    *** END OF THE PROJECT GUTENBERG EBOOK ...

    Older files may use:
    End of Project Gutenberg's ...

    This function tries to keep only the actual book text.
    """
    lines = text.splitlines()

    start_index = 0
    end_index = len(lines)

    start_markers = [
        "*** START OF",
        "***START OF",
        "START OF THE PROJECT GUTENBERG",
    ]

    end_markers = [
        "*** END OF",
        "***END OF",
        "END OF THE PROJECT GUTENBERG",
        "END OF PROJECT GUTENBERG",
        "End of Project Gutenberg",
    ]

    for i, line in enumerate(lines):
        normalized = line.upper()
        if any(marker.upper() in normalized for marker in start_markers):
            start_index = i + 1
            break

    for i, line in enumerate(lines):
        normalized = line.upper()
        if any(marker.upper() in normalized for marker in end_markers):
            end_index = i
            break

    return "\n".join(lines[start_index:end_index]).strip()


def normalize_line_breaks(text: str) -> str:
    """
    Normalize whitespace without trying to be too clever.

    For MVP, we preserve paragraph breaks and avoid aggressive reflow.
    Later, we can make this smarter if chunking quality is poor.
    """
    lines = [line.rstrip() for line in text.splitlines()]

    cleaned_lines = []
    previous_blank = False

    for line in lines:
        is_blank = line.strip() == ""

        if is_blank and previous_blank:
            continue

        cleaned_lines.append(line)
        previous_blank = is_blank

    return "\n".join(cleaned_lines).strip()


def add_markdown_header(text: str) -> str:
    """
    Add source metadata at the top of the cleaned file.

    This helps humans and future scripts know what source this text came from.
    """
    header = f"""---
source_id: {SOURCE_ID}
title: {TITLE}
author: {AUTHOR}
translator: {TRANSLATOR}
source_type: primary_text_translation
status: cleaned_for_mvp
---

# {TITLE}

Author: {AUTHOR}  
Translator: {TRANSLATOR}  
Source ID: {SOURCE_ID}

---

"""
    return header + text + "\n"


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw source not found: {RAW_PATH}")

    raw_text = RAW_PATH.read_text(encoding="utf-8", errors="replace")

    book_text = remove_gutenberg_header_footer(raw_text)
    cleaned_text = normalize_line_breaks(book_text)
    final_text = add_markdown_header(cleaned_text)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(final_text, encoding="utf-8")

    print("Cleaned source written to:")
    print(OUTPUT_PATH)
    print()
    print("Character count:")
    print(len(final_text))


if __name__ == "__main__":
    main()