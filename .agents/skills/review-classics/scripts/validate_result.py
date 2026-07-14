#!/usr/bin/env python3
"""Validate a second-pass result against a blinded packet."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from local_scriptorium.reviewing import ReviewContractError, validate_result


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: validate_result.py PACKET_DIRECTORY RESULT_JSON", file=sys.stderr)
        return 2
    try:
        summary = validate_result(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    except ReviewContractError as exc:
        print(f"invalid result: {exc}", file=sys.stderr)
        return 1
    print(f"valid result: {summary['review_id']} ({summary['item_count']} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
