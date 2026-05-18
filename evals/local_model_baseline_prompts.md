# Local Model Baseline Prompt Set

## Goal

This file defines the first controlled prompt set for testing the local model before adding source grounding, retrieval, or RAG.

The purpose is to evaluate what the local model can and cannot do on its own.

## Test Conditions

- Local model runner: Ollama
- Model: llama3.2:1b
- No source chunks supplied
- No retrieval layer
- No RAG
- No cloud model used for these answers

## What This Prompt Set Tests

These prompts test whether the local model can:

- explain local inference
- explain RAG
- follow source-grounding rules
- extract a main claim
- separate evidence from interpretation
- identify uncertainty
- refuse unsupported claims
- summarize a short passage
- compare local and edge inference
- identify failure modes

---

## Prompt 01: Explain Local Inference

### Purpose

Test whether the model understands local inference as a deployment pattern.

### Prompt

Explain local inference in this project: running a language model on my own Mac instead of using a cloud API. Compare it with cloud inference in concrete terms.

### Expected Good Answer

A good answer should explain that local inference means the model runs on the user's own machine. It should contrast this with cloud inference, where the prompt is sent to an external provider's server. It should mention privacy/control tradeoffs and possible limits around speed, hardware, and model quality.

---

## Prompt 02: Explain RAG

### Purpose

Test whether the model can explain retrieval-augmented generation clearly.

### Prompt

Explain retrieval-augmented generation in plain English. Use the example of asking questions about a book stored locally on my machine.

### Expected Good Answer

A good answer should explain that the system first retrieves relevant passages from the book, then gives those passages to the model so it can answer from them. It should not imply that the model magically knows the book without being given the text.

---

## Prompt 03: Source-Grounded Answer Rules

### Purpose

Test whether the model can define rules for answering only from supplied sources.

### Prompt

Give me rules for answering questions using only supplied source excerpts. The answer should avoid making claims that are not supported by the excerpts.

### Expected Good Answer

A good answer should mention using only the supplied text, citing source IDs, separating evidence from interpretation, flagging uncertainty, and refusing to answer when sources are insufficient.

---

## Prompt 04: Extract Main Claim

### Purpose

Test whether the model can identify the main claim in a single sentence.

### Prompt

Given this sentence, identify the main claim: "Dawson treats religion not as one institution within culture, but as a formative center that gives a civilization its symbolic order."

### Expected Good Answer

A good answer should say that the main claim is that Dawson sees religion as central or formative for culture/civilization, not merely as one institution among others.

---

## Prompt 05: Separate Evidence from Interpretation

### Purpose

Test whether the model can distinguish evidence from interpretation.

### Prompt

Explain the difference between evidence and interpretation when answering a question about a historical author.

### Expected Good Answer

A good answer should say that evidence is what the source directly says or shows, while interpretation is the reasoned explanation of what that evidence means. It should warn against presenting interpretation as if it were direct textual evidence.

---

## Prompt 06: Identify Uncertainty

### Purpose

Test whether the model can identify what can and cannot be safely concluded from a limited source excerpt.

### Prompt

A source excerpt says: "Dawson criticizes purely economic explanations of civilization." What can we safely conclude from this, and what can we not conclude?

### Expected Good Answer

A good answer should say that Dawson criticizes explanations that reduce civilization to economics alone. It should not conclude that he thinks economics is irrelevant, that he rejects capitalism, or that he has a fully developed alternative theory unless the source says so.

---

## Prompt 07: Refuse Unsupported Answer

### Purpose

Test whether the model knows how to avoid unsupported claims.

### Prompt

If the supplied sources do not mention Dawson's view of capitalism, how should an AI assistant answer the question "What did Dawson think of capitalism?"

### Expected Good Answer

A good answer should refuse to invent an answer. It should say that the supplied sources do not establish Dawson's view of capitalism and that more source material is needed.

---

## Prompt 08: Summarize a Passage

### Purpose

Test whether the model can summarize a short abstract passage.

### Prompt

Summarize this passage in three bullets: "A civilization is not held together only by laws, markets, or armies. It also depends on inherited symbols, rituals, loyalties, and assumptions about the sacred."

### Expected Good Answer

A good answer should mention that civilization depends on more than institutions or force, that symbolic/cultural inheritance matters, and that sacred assumptions can help bind a civilization together.

---

## Prompt 09: Compare Local and Edge Inference

### Purpose

Test whether the model can distinguish local inference from edge inference.

### Prompt

Explain the difference between local inference on a laptop and edge inference in a company deployment.

### Expected Good Answer

A good answer should explain that local inference on a laptop is single-device inference, while edge inference usually means running models near users/data across endpoint devices, local servers, branches, factories, hospitals, or other non-centralized environments. It should say the concepts overlap but are not identical.

---

## Prompt 10: Failure Modes

### Purpose

Test whether the model can identify realistic failure modes for an AI research assistant.

### Prompt

List five ways a local AI research assistant could give a bad answer when asked about a source text.

### Expected Good Answer

A good answer should mention hallucination, bad retrieval, misunderstanding the question, using unsupported claims, missing nuance, confusing sources, or being overconfident when evidence is weak.