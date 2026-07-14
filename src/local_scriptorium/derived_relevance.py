"""Derive chunk-level judgments from canonical passage anchors."""

from __future__ import annotations


def derive_relevance(questions: list[dict], chunks: list[dict]) -> dict[str, dict[str, int]]:
    """Map each question's acceptable evidence groups to the selected chunks.

    This is intentionally derived at evaluation time; canonical passage IDs remain
    the benchmark authority when a chunker changes.
    """
    passage_to_chunks: dict[str, set[str]] = {}
    for chunk in chunks:
        for passage_id in chunk.get("passage_ids", []):
            passage_to_chunks.setdefault(passage_id, set()).add(chunk["chunk_id"])
    output: dict[str, dict[str, int]] = {}
    for question in questions:
        grades: dict[str, int] = {}
        for evidence_set in question.get("acceptable_evidence_sets", []):
            for group in evidence_set.get("required_groups", []):
                for passage_id in group:
                    for chunk_id in passage_to_chunks.get(passage_id, set()):
                        grades[chunk_id] = max(grades.get(chunk_id, 0), 3)
        output[question["question_id"]] = grades
    return output
