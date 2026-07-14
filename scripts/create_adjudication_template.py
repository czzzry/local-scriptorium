"""Create a human-adjudication template without inventing decisions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    questions = json.loads(args.questions.read_text(encoding="utf-8"))["questions"]
    payload = {"schema_version": "1.0", "dataset_id": "late-antiquity-core-questions-v2", "status": "pending_human_adjudication", "items": [{"item_id": q["question_id"], "decision": None, "rationale": None, "adjudicator": None} for q in questions]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
