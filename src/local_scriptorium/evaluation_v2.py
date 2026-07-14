"""Passage-anchor retrieval evaluation for candidate v0.3 questions."""

from __future__ import annotations

from .derived_relevance import derive_relevance
from .retrieval import Retriever


def evaluate_questions_v2(corpus: dict, questions: list[dict], *, method: str = "bm25", top_k: int = 5) -> dict:
    retriever = Retriever(corpus["chunks"])
    relevance = derive_relevance(questions, corpus["chunks"])
    rows = []
    scored = []
    for question in questions:
        results = retriever.search(question["question"], method, top_k)
        relevant = set(relevance[question["question_id"]])
        if question["answerability"] == "unanswerable":
            rows.append({"question_id": question["question_id"], "answerability": "unanswerable", "retrieved": len(results), "refusal_required": True})
            continue
        hits = [result.chunk_id for result in results if result.chunk_id in relevant]
        scored.append(bool(hits))
        rows.append({"question_id": question["question_id"], "answerability": "answerable", "retrieved": len(results), "relevant_hits": len(hits), "hit": bool(hits)})
    return {"schema_version": "v0.3-retrieval-evaluation-1.0", "method": method, "top_k": top_k, "question_count": len(questions), "answerable_count": len(scored), "recall_like_hit_rate": sum(scored) / len(scored) if scored else None, "rows": rows}
