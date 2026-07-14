"""Optional grounded-answer orchestration with a deterministic fake adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ModelAdapter(Protocol):
    def answer(self, question: str, context: list[dict]) -> str: ...


@dataclass(frozen=True)
class FakeModelAdapter:
    """Offline adapter used by tests; it never invents beyond supplied context."""

    def answer(self, question: str, context: list[dict]) -> str:
        if not context:
            return "The corpus does not provide enough grounded evidence to answer this question."
        authors = ", ".join(dict.fromkeys(str(item.get("author", item["source_id"])) for item in context))
        return f"The retrieved local passages concern {authors}. A source-grounded answer requires reading the cited passages directly; the corpus does not justify additional claims beyond them."


def grounded_answer(question: str, results: list, corpus: dict, adapter: ModelAdapter) -> dict:
    by_id = {chunk["chunk_id"]: chunk for chunk in corpus["chunks"]}
    context = [by_id[result.chunk_id] for result in results if result.chunk_id in by_id]
    answer = adapter.answer(question, context)
    return {
        "schema_version": "v0.3-grounded-answer-1.0",
        "question": question,
        "answerability": "answerable" if context else "unanswerable",
        "answer": answer,
        "textual_evidence": [{"chunk_id": item["chunk_id"], "source_id": item["source_id"], "author": item.get("author"), "work": item.get("work"), "locator": {"start_line": item.get("start_line"), "end_line": item.get("end_line")}} for item in context],
        "interpretation": "No independent interpretation is asserted by the deterministic adapter.",
        "uncertainty": "This is an evidence display/fake-adapter result, not a scholarly judgment.",
        "citations": [item["chunk_id"] for item in context],
    }
