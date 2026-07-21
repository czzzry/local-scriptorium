.PHONY: demo install test lint release-audit

demo:
	PYTHONPATH=src python3 -m local_scriptorium --pack late-antiquity-core-v1 ingest
	PYTHONPATH=src python3 -m local_scriptorium --pack late-antiquity-core-v1 ask \
		"How do providence and fortune differ?" --generate fake

install:
	python3 -m pip install -e '.[dev]'

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v
	python3 scripts/privacy_check.py

lint:
	python3 -m ruff check .

release-audit:
	PYTHONPATH=src python3 scripts/release_audit_v3.py \
		--register sources_public/source_register.v2.json \
		--pack data/packs/late_antiquity_core.v1.json \
		--questions data/evaluation/late-antiquity-core-questions-v2.accepted.json \
		--review-policy data/reviews/review_policy.v1.json
