"""Small deterministic retrieval baselines with shared ranking logic."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

STOPWORDS = frozenset(
    "a an and are as at be by can did do does for from had has have he her his how in is it "
    "its of on or she the their this to was were what when where which who why with would work "
    "boethius philosophy".split()
)


def tokenize(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z]+", text.lower()) if len(word) > 2 and word not in STOPWORDS]


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    score: float
    rank: int


class Retriever:
    """Index a corpus once and expose keyword, BM25, TF-IDF-vector and hybrid ranking."""

    def __init__(self, chunks: Iterable[dict]) -> None:
        self.chunks = list(chunks)
        if not self.chunks:
            raise ValueError("cannot index an empty corpus")
        self.tokens = [tokenize(chunk["text"]) for chunk in self.chunks]
        self.counts = [Counter(words) for words in self.tokens]
        self.avg_length = sum(map(len, self.tokens)) / len(self.tokens)
        frequencies = Counter(term for words in self.tokens for term in set(words))
        self.idf = {
            term: math.log(1 + (len(self.chunks) - count + 0.5) / (count + 0.5))
            for term, count in frequencies.items()
        }

    def _keyword(self, query: list[str], index: int) -> float:
        return float(sum(self.counts[index][term] for term in set(query)))

    def _bm25(self, query: list[str], index: int, k1: float = 1.5, b: float = 0.75) -> float:
        length = len(self.tokens[index])
        score = 0.0
        for term in query:
            frequency = self.counts[index][term]
            if frequency:
                score += self.idf.get(term, 0.0) * frequency * (k1 + 1) / (
                    frequency + k1 * (1 - b + b * length / self.avg_length)
                )
        return score

    def _vector(self, query: list[str], index: int) -> float:
        query_counts = Counter(query)
        terms = set(query_counts) | set(self.counts[index])
        query_values = [query_counts[t] * self.idf.get(t, 0.0) for t in terms]
        doc_values = [self.counts[index][t] * self.idf.get(t, 0.0) for t in terms]
        numerator = sum(a * b for a, b in zip(query_values, doc_values))
        denominator = math.sqrt(sum(a * a for a in query_values) * sum(b * b for b in doc_values))
        return numerator / denominator if denominator else 0.0

    def search(self, query: str, method: str = "bm25", top_k: int = 5) -> list[SearchResult]:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        terms = tokenize(query)
        if method not in {"keyword", "bm25", "vector", "hybrid"}:
            raise ValueError(f"unknown retrieval method: {method}")
        scores: list[tuple[str, float]] = []
        bm25 = [self._bm25(terms, i) for i in range(len(self.chunks))]
        vector = [self._vector(terms, i) for i in range(len(self.chunks))]
        for index, chunk in enumerate(self.chunks):
            if method == "keyword":
                score = self._keyword(terms, index)
            elif method == "bm25":
                score = bm25[index]
            elif method == "vector":
                score = vector[index]
            else:
                # Reciprocal-rank fusion avoids combining incomparable score scales.
                b_rank = sorted(range(len(bm25)), key=lambda i: (-bm25[i], self.chunks[i]["chunk_id"])).index(index) + 1
                v_rank = sorted(range(len(vector)), key=lambda i: (-vector[i], self.chunks[i]["chunk_id"])).index(index) + 1
                score = 1 / (60 + b_rank) + 1 / (60 + v_rank)
            scores.append((chunk["chunk_id"], score))
        ranked = sorted(scores, key=lambda item: (-item[1], item[0]))[:top_k]
        return [SearchResult(chunk_id=cid, score=score, rank=rank) for rank, (cid, score) in enumerate(ranked, 1)]

