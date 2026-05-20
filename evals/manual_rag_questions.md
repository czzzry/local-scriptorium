# Manual RAG Questions

## Goal

Create a small manual question set for testing whether Local Scriptorium can answer from retrieved Boethius chunks.

These questions will be used in the next tickets to manually select relevant chunks, run prompts with and without source chunks, and compare grounded vs ungrounded answers.

## Source

Source ID: `BOETHIUS_CONSOLATION_001`

Chunk file:

`chunks/boethius_consolation_chunks.json`

## Question Design Principles

The question set should include:

- simple factual/source-location questions
- conceptual summary questions
- interpretation questions that still require source evidence
- comparison questions
- uncertainty / insufficient-evidence questions

The goal is not to test general knowledge of Boethius. The goal is to test whether answers can be grounded in retrieved chunks.

---

## Questions

### Q01: Philosophy and Poetry

Question:

What is the relationship between Philosophy and the Muses of Poetry at the beginning of the work?

Question type:

Interpretive summary

What this tests:

Whether the system can explain a symbolic scene without overclaiming beyond the source.

---

### Q02: Boethius’ Complaint

Question:

How does Boethius describe his own misery in the opening complaint?

Question type:

Source summary

What this tests:

Whether the system can summarize poetic source text without flattening it into generic sadness.

---

### Q03: Fortune’s Nature

Question:

How does Philosophy describe the nature of Fortune?

Question type:

Concept explanation

What this tests:

Whether the system can explain Fortune as unstable or mutable using source evidence.

---

### Q04: False Happiness

Question:

Why does Philosophy argue that wealth, rank, power, glory, and pleasure cannot provide true happiness?

Question type:

Conceptual synthesis

What this tests:

Whether the system can combine evidence across related chunks without inventing unsupported doctrine.

---

### Q05: True Happiness

Question:

What does Philosophy identify as true happiness or the highest good?

Question type:

Concept explanation

What this tests:

Whether the system can distinguish false goods from the supreme good.

---

### Q06: Providence and Fate

Question:

How does Philosophy distinguish providence from fate?

Question type:

Definition / comparison

What this tests:

Whether the system can handle a technical philosophical distinction from the source.

---

### Q07: Evil and Power

Question:

Why does Philosophy argue that wicked people are weak rather than powerful?

Question type:

Argument reconstruction

What this tests:

Whether the system can reconstruct a paradoxical argument without making it sound like ordinary moralism.

---

### Q08: Good and Bad Fortune

Question:

In what sense does Philosophy claim that every fortune is good fortune?

Question type:

Argument explanation

What this tests:

Whether the system can explain a counterintuitive claim using the source’s reasoning.

---

### Q09: Insufficient Evidence — Christianity

Question:

Based only on the selected Boethius chunks, can we say whether the work is explicitly Christian?

Question type:

Insufficient evidence / uncertainty

What this tests:

Whether the system avoids answering from outside knowledge and distinguishes what the chunks show from broader historical context.

---

### Q10: Insufficient Evidence — Author Biography

Question:

Based only on the selected Boethius chunks, what can we safely say about the historical circumstances of Boethius’ imprisonment and death?

Question type:

Insufficient evidence / uncertainty

What this tests:

Whether the system avoids relying on front matter, epilogue, or outside biography unless those chunks are actually supplied.

---

# Notes for Next Ticket

In SCRIP-20, manually select relevant chunks for each question.

For each question, record:

- question ID
- likely relevant chunk IDs
- why those chunks are relevant
- whether the evidence is sufficient
- whether the answer should include an uncertainty caveat