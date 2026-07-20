"""Generate auditable question candidates from canonical passage anchors.

This deliberately produces ``candidate`` items, not gold labels. Acceptance still
requires blinded review and adjudication described by the v0.3 protocol.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    corpus = json.loads(args.canonical.read_text(encoding="utf-8"))
    passages = corpus["passages"]
    by_source: dict[str, list[dict]] = {}
    for passage in passages:
        by_source.setdefault(passage["source_id"], []).append(passage)
    sources = sorted(by_source)
    questions: list[dict] = []

    def item(number: int, family: str, text: str, split: str, question_type: str,
             ids: list[str], answerability: str = "answerable", risk: list[str] | None = None) -> None:
        evidence = [] if answerability == "unanswerable" else [{"required_groups": [[pid] for pid in ids]}]
        questions.append({"question_id": f"CAND-{number:03d}", "family_id": family,
                          "question": text, "split": split, "question_type": question_type,
                          "risk_tags": risk or [], "answerability": answerability,
                          "canonical_passage_ids": ids, "acceptable_evidence_sets": evidence,
                          "curation_state": "candidate"})

    n = 1
    # 30 single-passage textual candidates.
    for index in range(30):
        passage = passages[index]
        lead = " ".join(str(passage["text"]).split())[:90]
        item(n, f"single-{index:03d}", f"What claim or distinction is made in the passage beginning ‘{lead}…’?", "dev" if index < 21 else "test", "single_passage_textual", [passage["passage_id"]])
        n += 1
    # 20 within-work synthesis candidates.
    for index in range(20):
        group = by_source[sources[index % len(sources)]][index:index + 2]
        ids = [p["passage_id"] for p in group]
        item(n, f"synthesis-{index:03d}", "How do these two passages from the same work develop or qualify one another?", "dev" if index < 14 else "test", "within_work_synthesis", ids, risk=["interpretation_sensitive"])
        n += 1
    # 10 source-scope candidates.
    for index in range(10):
        source = sources[index % len(sources)]
        passage = by_source[source][0]
        item(n, f"scope-{index:03d}", "Which author and work does this passage belong to, and what edition metadata is recorded?", "dev" if index < 7 else "test", "attribution_source_scope", [passage["passage_id"]], risk=["source_attribution"])
        n += 1
    # 20 pairwise cross-author candidates.
    for index in range(20):
        left = by_source[sources[index % len(sources)]][0]
        right = by_source[sources[(index + 1) % len(sources)]][0]
        item(n, f"pair-{index:03d}", "What similarity or difference can be stated cautiously from these two authors’ passages?", "dev" if index < 14 else "test", "cross_author_comparison", [left["passage_id"], right["passage_id"]], risk=["interpretation_sensitive", "translation_sensitive"])
        n += 1
    # 10 concept-tracing candidates.
    for index in range(10):
        chosen = [by_source[sources[(index + offset) % len(sources)]][0]["passage_id"] for offset in range(3)]
        item(n, f"trace-{index:03d}", "How does the selected concept appear across these three source units?", "dev" if index < 7 else "test", "concept_tracing", chosen, risk=["interpretation_sensitive"])
        n += 1
    # 10 plausible near-miss unanswerables.
    for index in range(10):
        item(n, f"unanswerable-{index:03d}", "Does this acquired corpus establish the exact original-language wording and definitive authorship of this claim?", "dev" if index < 7 else "test", "unanswerable", [], "unanswerable", ["external_adjudication"])
        n += 1

    payload = {"schema_version": "2.0", "dataset_id": "late-antiquity-available-questions-v2-candidates", "status": "candidate_generation_pending_review", "questions": questions}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {args.output} ({len(questions)} candidates)")


if __name__ == "__main__":
    main()
