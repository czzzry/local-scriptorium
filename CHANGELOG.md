# Changelog

## 0.3.0 — Late Antiquity Evaluation Corpus

- Expanded the public-domain corpus to nine source units across six Late Antique authors.
- Added stable canonical passages before retrieval chunking, with edition metadata and checksums.
- Added a reviewed v0.3 benchmark with answerable, synthesis, attribution, comparison, concept-tracing, and explicit unanswerable questions.
- Added blinded review packets, reconciliation, adjudication, stale-review detection, and a fail-closed release audit.
- Added an offline grounded-answer workflow and explicit limits around scholarly and original-language claims.
- Kept the default install dependency-free and the complete deterministic workflow offline.

## 0.2.0 — Reproducible Evaluation Harness

- Added an installable, standard-library offline package and `scriptorium` CLI.
- Added strict versioned corpus, provenance, question, result, answer, and run contracts.
- Added a manually curated 50-question development/held-out dataset.
- Standardized keyword, BM25, offline TF-IDF vector, and reciprocal-rank hybrid evaluation.
- Added ranked metrics, bootstrap confidence intervals, failure taxonomy, answer fixtures, and derived reports.
- Added detailed ranked-result CSV, complete run metadata, versioned regression thresholds, and styled HTML reporting.
- Isolated generated output and added tests, CI, privacy checks, and release documentation.

## 0.1.0 — Manual MVP

- Established the Boethius corpus, stable chunks, ten manual questions, historical lexical/dense retrieval experiments, and local Ollama generation notes.
