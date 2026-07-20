# v0.2 Release Readiness Audit

Status: Historical. Superseded by the completed v0.3 release evidence in `README.md`, `CHANGELOG.md`, and `docs/analysis/v0.3_case_study.md`.

This checklist maps the v0.2 brief to repository evidence. It is intended for final human review before tagging.

| Requirement | Evidence | Status |
|---|---|---|
| Installable package and composable CLI | `pyproject.toml`; `src/local_scriptorium/cli.py`; CLI end-to-end tests | Complete |
| Offline deterministic baseline | Standard-library runtime; two-run artifact comparison; CI has no model/API step | Complete |
| Optional local model/vector separation | Historical Ollama scripts isolated under generated output; README labels TF-IDF vs dense embeddings | Complete |
| Versioned data contracts and provenance | `docs/data_contracts.md`; validators; manifest checksum and path tests | Complete |
| Run configuration and environment record | `run_metadata.json` includes configuration, seed, revision, UTC timestamp, runtime, dependencies, checksum | Complete |
| Generated/human output separation | `.gitignore`; `docs/analysis/`; output-isolation test covering every script output path | Complete |
| At least 50 defensible questions | 50 source-linked questions: 30 dev, 20 held-out test | Complete, pending independent scholarly adjudication |
| Ranked retrieval metrics and uncertainty | Recall, precision, hit rate, MRR, nDCG, seeded bootstrap intervals | Complete |
| Retrieval failure taxonomy | Per-question labels and report definitions/counts | Complete |
| Held-out tuning protection | Development default, explicit test selection, documented split policy | Complete as procedural protection |
| Grounded-answer evaluation | Citation, curated faithfulness/unsupported claims, answerability, refusal fixtures | Complete as deterministic heuristic regression checks |
| Derived reporting | Raw JSON, aggregate/detail CSV, Markdown, styled self-contained HTML | Complete |
| Unit, CLI, edge, smoke, and regression tests | `tests/`; versioned regression thresholds | Complete |
| Offline CI and dependency updates | `.github/workflows/ci.yml`; `.github/dependabot.yml` | Complete |
| Portfolio documentation and architecture diagram | README, Mermaid diagram, demo, methodology, contributing, security, license, corpus notice, changelog | Complete |
| Privacy, portability, and licensing review | Privacy scanner, portable-path validator, machine fingerprint redaction, data notice | Complete |

## Release recommendation

The repository is technically ready for a `v0.2.0` release candidate. Before tagging, a human should review the held-out question/relevance judgments and confirm the Project Gutenberg notice is suitable for the intended distribution jurisdiction. Those reviews affect evidentiary confidence and legal context, not the reproducibility of the current harness.
