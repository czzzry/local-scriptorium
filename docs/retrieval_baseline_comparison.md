# Retrieval Baseline Comparison

This document preserves the original comparison entry point. The v0.1 ten-question experiment reported Recall@5 of 0.34 for keyword count, 0.47 for BM25, 0.49 for Ollama `embeddinggemma`, and 0.55 for a 50/50 hybrid. Those historical figures came from different scripts and a much smaller dataset; they are not directly comparable with v0.2.

The current reproducible comparison is generated from raw artifacts:

```bash
scriptorium ingest
scriptorium evaluate --split test --deterministic
scriptorium report
```

The resulting `outputs/generated/report.md` contains all five ranked metrics, seeded bootstrap intervals, failure counts, answer checks, run metadata, and limitations. The methodology and architectural changes are documented in [analysis/v0.2_methodology.md](analysis/v0.2_methodology.md).

This file is human-authored and scripts never overwrite it.
