# Versioned Data Contracts

All v0.2 contracts use `schema_version: "1.0"`. Minor additive fields may be introduced without changing the major version; removing fields or changing their meaning requires a new schema version.

## Source manifest

`sources_public/source_manifest.json` contains a non-empty `sources` list. Every source requires `source_id`, `title`, `source_url`, `license`, `checksum_sha256`, `ingested_at`, `permitted_use`, and a portable relative `processed_path`. Ingestion verifies the SHA-256 checksum and rejects missing files, malformed provenance, absolute paths, and parent traversal.

## Corpus

The corpus contains stable, unique chunks with `chunk_id`, `source_id`, non-empty `text`, positive `start_line`, `end_line`, and `word_count`. The generated corpus contract is `outputs/generated/corpus.v1.json`.

## Questions and relevance judgments

`data/evaluation/questions.v1.json` declares `dataset_id`, `corpus_id`, curation metadata, and a `questions` list. Each question has a stable ID, text, `dev` or `test` split, question type, and graded `relevance` map from chunk ID to grade 1–3. Both splits are mandatory. The test split is held out by process: the CLI defaults to development and test execution must be explicit.

## Retrieval results

`retrieval_results.json` records dataset/corpus IDs, split, k, methods, aggregate metrics, confidence intervals, and per-question records. Each per-question record includes the exact query, relevance judgments, ranked chunk IDs with scores, metrics, and failure class. `retrieval_summary.csv` contains aggregate method rows; `retrieval_details.csv` contains one row per method, question, and retrieved rank.

## Answer fixtures and evaluations

`data/answers/fixtures.v1.json` records answerability, retrieved chunks, response type, answer text, citations, and curated unsupported claims. Validation rejects unknown chunks or malformed labels. `answer_results.json` records deterministic citation-membership, faithfulness-label, unsupported-claim, answerability, and refusal checks. These are regression heuristics rather than objective truth.

## Run metadata

`run_metadata.json` records the harness version, actual configuration, seed, Git revision, UTC timestamp, Python implementation/version, platform, dependency/runtime profile, and corpus checksum. Environment-specific fields are intentionally variable; metric and ranking artifacts remain deterministic for a fixed corpus, dataset, configuration, revision, and seed.
