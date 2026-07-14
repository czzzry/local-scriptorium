#!/usr/bin/env python3
"""Validate a blinded Local Scriptorium review packet."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from local_scriptorium.reviewing import ReviewContractError, validate_packet


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_packet.py PACKET_DIRECTORY", file=sys.stderr)
        return 2
    try:
        summary = validate_packet(Path(sys.argv[1]).resolve())
    except ReviewContractError as exc:
        print(f"invalid packet: {exc}", file=sys.stderr)
        return 1
    print(f"valid packet: {summary['review_id']} ({len(summary['item_ids'])} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
