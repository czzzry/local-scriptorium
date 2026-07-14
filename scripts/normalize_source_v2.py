"""Normalize one approved Gutenberg text into the committed v0.3 form."""

from __future__ import annotations

import argparse
from pathlib import Path

from local_scriptorium.ingestion import remove_gutenberg_wrapper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--translator", required=True)
    args = parser.parse_args()
    raw = Path(args.input).read_text(encoding="utf-8", errors="replace")
    body = remove_gutenberg_wrapper(raw)
    header = ("---\n"
              f"source_id: {args.source_id}\n"
              f"title: {args.title}\n"
              f"author: {args.author}\n"
              f"translator: {args.translator}\n"
              "source_type: primary_text_translation\n"
              "status: cleaned_for_v0.3\n"
              "---\n\n")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(header + body.strip() + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
