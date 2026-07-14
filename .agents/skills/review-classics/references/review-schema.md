# Review Packet and Result Schema

## Packet directory

A packet contains request.json, items.jsonl, evidence.jsonl, and manifest.json. It may contain only additional files named by request.json and listed in manifest.json.

request.json requires:

- schema_version: 1.0
- review_id
- review_kind
- protocol_version
- pack_id
- independence_level
- external_context_allowed
- randomization_seed
- allowed_input_files
- opaque_item_ids

items.jsonl contains one JSON object per opaque item. Every item requires item_id. Depending on review kind it may include question, task_type, candidate_evidence, atomic_claims, citations, or chunk context.

The packet must not contain expected answers, first-pass verdicts or grades, first-pass rationale, retrieval method, rank or score, split identity, thresholds, benchmark results, previous reviews, chain-of-thought, or hidden control mappings.

manifest.json has schema_version 1.0 and a files object mapping relative packet filenames to their SHA-256 checksums. The manifest does not hash itself.

## Result

second_pass.json requires:

- schema_version: 1.0
- review_id
- protocol_version
- input_manifest_sha256
- skill_checksum
- reviewer_type
- model_identity
- independence_level
- external_context_used
- completed_at
- items

Each item result requires:

- item_id
- action
- reason_codes
- confidence
- evidence_refs
- rationale
- external_review_required

Result actions are accept, accept_with_caveat, revise, reject, insufficient_internal_evidence, needs_external_specialist, and invalid_packet.

The result is an immutable proposed second opinion. It must not contain a reconciliation decision or modify canonical benchmark artifacts.
