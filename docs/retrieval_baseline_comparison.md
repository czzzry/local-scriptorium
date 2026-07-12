# Retrieval Baseline Comparison

Local Scriptorium evaluates retrieval separately from answer generation. The same ten-question manual evidence map is used for every retriever so that improvements are comparable.

## Results

| Retrieval method | Average Recall@5 | Average Precision@5 | Interpretation |
| --- | ---: | ---: | --- |
| Keyword count | 0.34 | Not measured | Useful zero-dependency baseline, but brittle when query wording differs from the source. |
| BM25 | 0.47 | 0.30 | Better exact-term weighting and a stronger lexical baseline. |
| Vector | 0.49 | 0.34 | Helps with semantic matches, but remains uneven on the small literary corpus. |
| Hybrid | **0.55** | **0.36** | Best result in this evaluation; combines lexical and semantic evidence. |

The detailed generated reports are committed under `outputs/`:

- [Keyword retrieval](../outputs/keyword_retrieval_eval.md)
- [BM25 retrieval](../outputs/bm25_retrieval_eval.md)
- [Vector retrieval](../outputs/vector_retrieval_eval.md)
- [Hybrid retrieval](../outputs/hybrid_retrieval_eval.md)

## What The Numbers Mean

`Recall@5` measures how much of the manually expected evidence appears in the top five retrieved chunks. `Precision@5` measures how much of that five-chunk context is expected evidence rather than noise.

Hybrid retrieval is the current default because it produced the strongest aggregate result. The 50/50 weighting is intentionally not tuned: optimizing weights against only ten questions would overfit the evaluation set.

## Reproduce The Dependency-Free Baselines

From the repository root, using Python 3.10 or newer:

```bash
python3 scripts/evaluate_keyword_retrieval.py
python3 scripts/evaluate_bm25_retrieval.py
```

Vector and hybrid evaluation additionally require a local Ollama instance and the `embeddinggemma` model, as described in the main README.

## Limits

- one evaluated source corpus
- ten manually authored questions
- one first-pass evidence map
- no statistical confidence interval
- results measure retrieval over this corpus, not general RAG quality
