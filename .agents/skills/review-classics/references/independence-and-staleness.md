# Independence, Reconciliation, and Staleness

## Blinding

The packet must not disclose expected answers, creator labels, retrieval method, rank, score, split, thresholds, benchmark results, previous reviews, or control mappings. Candidate passage order is randomized with a recorded seed and internal IDs are opaque.

Filesystem sharing means this is procedural blinding, not cryptographic isolation. A reviewer must be started with a fresh context and explicitly instructed not to search the repository or control directory.

Internal-evidence reviews do not browse the web. External context is allowed only when the request declares it and the result records its use.

## Reconciliation

The reviewer emits a second opinion only. A separate reconciliation stage compares it with the first pass and records agreement, compatible caveat, material disagreement, or unreviewable. A human adjudicator resolves material disagreement. Unresolved specialist cases are excluded from scored release data.

## Staleness

Reviews are immutable. A changed source text, canonical passage, chunk, chunker configuration, question, evidence pool, answer, retrieved context, corpus membership, or major protocol version makes the affected review stale. A minor protocol change is retained as legacy_protocol until release policy requests refresh.

Release checks must report the exact dependency mismatch and must never silently omit stale reviews.
