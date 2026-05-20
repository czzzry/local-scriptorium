# Chunk ID Convention

## Goal

Define a stable ID convention for source chunks in Local Scriptorium.

Chunks are the searchable evidence units used by the retrieval system. Each chunk needs a stable ID so generated answers can cite the source material that supports them.

## Source ID

A source ID identifies the original source text.

Format:

`AUTHOR_WORK_NUMBER`

Example:

`BOETHIUS_CONSOLATION_001`

This means:

- author: Boethius
- work: The Consolation of Philosophy
- source number: 001

The source ID is defined in:

`sources_public/source_manifest.json`

## Chunk ID

A chunk ID identifies a specific passage created from a source.

Format:

`SOURCE_ID_CHUNK_###`

Example:

`BOETHIUS_CONSOLATION_001_CHUNK_001`

Another example:

`BOETHIUS_CONSOLATION_001_CHUNK_042`

## Rules

1. Every chunk must have one unique chunk ID.
2. Every chunk ID must include the source ID.
3. Chunk numbering starts at `001`.
4. Chunk numbers should use three digits so sorting works cleanly.
5. Chunk IDs should be stable once created.
6. If the chunking method changes significantly, regenerate chunks deliberately and document the change.
7. Chunk IDs should appear in model prompts and generated answers.

## Why Stability Matters

If an answer cites:

`BOETHIUS_CONSOLATION_001_CHUNK_017`

then that ID should continue to point to the same passage unless the corpus is intentionally regenerated.

Stable IDs make it possible to:

- trace answers back to source passages
- evaluate whether retrieval found the right evidence
- debug bad answers
- compare model outputs across runs
- avoid vague or unverifiable citations

## First Active Source

The first active MVP source is:

`BOETHIUS_CONSOLATION_001`

The first chunk IDs will therefore look like:

`BOETHIUS_CONSOLATION_001_CHUNK_001`

`BOETHIUS_CONSOLATION_001_CHUNK_002`

`BOETHIUS_CONSOLATION_001_CHUNK_003`

## Future Extension

Later, chunk metadata may also include:

- source title
- author
- translator
- section or book number
- approximate word count
- start/end character offsets
- source type
- public/private status

For MVP, the required fields are:

- chunk_id
- source_id
- text