## First Corpus Decision

Selected source:

Boethius, *The Consolation of Philosophy*

Author:

Anicius Manlius Severinus Boethius

Translator:

H. R. James

Source type:

Primary source text in public-domain English translation

Public/private status:

Public source from Project Gutenberg, suitable for `sources_public/`

File location:

`sources_public/raw/boethius_consolation_james.txt`

Proposed source ID:

BOETHIUS_CONSOLATION_001

Reason for selection:

The text is philosophically and theologically rich, short enough for a first RAG/chunking experiment, and structured around arguments about fortune, happiness, providence, evil, and free will. It is a better first Scriptorium test than a giant multi-volume work because it is dense but manageable.

Why this source is suitable for MVP:

It is available as clean Plain Text UTF-8 from Project Gutenberg, which avoids OCR/scanned-PDF cleanup. It should be suitable for testing source cleaning, chunking, retrieval, source IDs, and grounded answers.

Risks / Caveats:

The file includes Project Gutenberg header/footer material that should be removed or ignored before chunking. The translation is older, so language may be archaic, but that is acceptable for the project.

## Candidate Sources Downloaded

I downloaded several clean public-text candidates into `sources_public/raw/`:

- Plato, Apology
- Plato, Apology/Crito/Phaedo
- Augustine, Confessions
- Augustine, City of God Vol. I
- Boethius, Consolation of Philosophy

These are treated as candidate sources, not the full MVP corpus.

## Active MVP Source

Selected active source:

Boethius, *The Consolation of Philosophy*

Reason:

This is the best first Scriptorium test because it is philosophically dense, structured, and manageable. The other downloaded texts will remain as candidate sources for later tests.

## Scope Control

For MVP, I will process only one active source first. The other downloaded files will stay in `sources_public/raw/` but will not be chunked or evaluated until the source → chunk → retrieve → answer loop works on the first source.