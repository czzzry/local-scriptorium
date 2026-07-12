"""Information-retrieval metrics and deterministic bootstrap intervals."""

from __future__ import annotations

import math
import random
from statistics import mean


def query_metrics(retrieved: list[str], relevance: dict[str, int], k: int) -> dict[str, float]:
    ranked = retrieved[:k]
    relevant = set(relevance)
    hits = [chunk_id for chunk_id in ranked if chunk_id in relevant]
    recall = len(set(hits)) / len(relevant) if relevant else 0.0
    precision = len(set(hits)) / k if k else 0.0
    hit_rate = float(bool(hits))
    first_rank = next((index for index, item in enumerate(ranked, 1) if item in relevant), None)
    reciprocal_rank = 1 / first_rank if first_rank else 0.0
    dcg = sum(relevance.get(item, 0) / math.log2(index + 1) for index, item in enumerate(ranked, 1))
    ideal = sorted(relevance.values(), reverse=True)[:k]
    idcg = sum(grade / math.log2(index + 1) for index, grade in enumerate(ideal, 1))
    return {
        f"recall@{k}": recall,
        f"precision@{k}": precision,
        f"hit_rate@{k}": hit_rate,
        "mrr": reciprocal_rank,
        f"ndcg@{k}": dcg / idcg if idcg else 0.0,
    }


def aggregate(rows: list[dict[str, float]]) -> dict[str, float]:
    return {key: mean(row[key] for row in rows) for key in rows[0]} if rows else {}


def bootstrap_ci(values: list[float], seed: int = 42, samples: int = 2000) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    rng = random.Random(seed)
    means = sorted(mean(rng.choices(values, k=len(values))) for _ in range(samples))
    return means[int(samples * 0.025)], means[min(samples - 1, int(samples * 0.975))]

