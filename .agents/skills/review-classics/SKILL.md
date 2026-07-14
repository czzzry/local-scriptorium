---
name: review-classics
description: Review blinded Local Scriptorium packets containing classical or Late Antique text, question evidence, source scope, chunk boundaries, citations, or grounded answer claims. Use for second-pass source-consistency review, disagreement detection, and release-readiness checks. Do not use to certify editions, licensing, original-language philology, historical truth, or scholarly consensus.
---

# Review Classics

Use this skill as a blinded second-pass reviewer of a Local Scriptorium packet. The protocol improves consistency and exposes disagreement; it does not create an independent human scholar.

## Required workflow

1. Validate the packet directory and all checksums before reading its items.
2. Confirm the declared independence level.
3. Read only packet-approved files and the named rubric.
4. Use the supplied corpus bundle to inspect full relevant sections and neighboring passages. Do not search the repository for control data.
5. Judge the supplied textual evidence, answerability, attribution, or claim support according to the review kind.
6. Record concise evidence-bound rationale and exact opaque evidence references.
7. Escalate translation, original-language, chronology, authorship, contested doctrine, and interpretive-consensus questions.
8. Write a structured result without hidden chain-of-thought.
9. Validate the result before returning it.
10. Never edit questions, passages, chunks, manifests, first-pass labels, gold data, or reconciliation.

## Independence

- I0 is invalid when expected answers, original labels, prior rationale, retrieval scores, split identity, or previous reviews are exposed.
- I1 is a fresh blinded procedural pass using the same model family.
- I2 is a fresh blinded pass using a different model or provider.
- I3 is an independent qualified human specialist.

Report the level; never call I1 or I2 scholarly validation.

## Review kinds

- chunk_quality: boundary, context, content kind, and attribution.
- question_evidence: question clarity, answerability, required passages, distractors, and cross-source coverage.
- source_scope_check: compliance with an already-approved edition and content policy.
- answer_claim: claim-level support, citation alignment, overreach, contradiction, relevance, and refusal.

## Verdicts

Use only accept, accept_with_caveat, revise, reject, insufficient_internal_evidence, needs_external_specialist, or invalid_packet. Reconciliation is performed outside this skill.

## References

- Read references/review-schema.md for packet and result fields.
- Read references/rubrics.md for review-kind criteria and reason codes.
- Read references/independence-and-staleness.md for blinding, reconciliation, and invalidation rules.

## Validation commands

The project validators can be run without an agent runtime:

    python3 .agents/skills/review-classics/scripts/validate_packet.py PACKET_DIRECTORY
    python3 .agents/skills/review-classics/scripts/validate_result.py PACKET_DIRECTORY RESULT_JSON

