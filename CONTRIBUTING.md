# Contributing

Use Python 3.11+ and install `.[dev]`. Keep the default path offline and dependency-light. Changes to ranking, chunking, questions, or relevance judgments must include tests and a regenerated held-out report. Tune on `dev`; run `test` only for a release candidate or regression check, and record why.

Human interpretation belongs in `docs/analysis/`. Never commit `outputs/generated/`, credentials, private texts, raw model files, or machine-specific paths. New corpus material needs a stable ID, source URL, license, SHA-256 checksum, ingestion date, permitted-use statement, and a privacy review.

Before committing:

```bash
ruff check .
python -m unittest discover -s tests -v
python scripts/privacy_check.py
scriptorium ingest
scriptorium evaluate --split test --deterministic
scriptorium report
```

