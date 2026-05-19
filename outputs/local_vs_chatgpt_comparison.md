# Local vs ChatGPT Comparison

## Goal

Compare selected local model outputs against ChatGPT/cloud outputs using the same baseline prompts.

The purpose is to understand where the local model is good enough, where it fails, and what types of tasks may require stronger cloud models or better grounding.

## Date

2026-05-19

## Models Compared

### Local Model

- Runner: Ollama
- Model: llama3.2:1b
- Inference location: local Mac
- Source file: `outputs/local_model_baseline_outputs.md`

### Cloud Model

- Model: ChatGPT
- Inference location: cloud
- Source: manual run using the same prompt text

## Comparison Method

For each selected prompt, compare:

- accuracy
- clarity
- specificity
- overconfidence
- whether it followed the task
- whether the answer would be safe to use without further review

Scoring:

- 5/5 = strong, usable
- 4/5 = good with minor weaknesses
- 3/5 = mixed
- 2/5 = mostly poor
- 1/5 = serious misunderstanding
- 0/5 = unusable or unrelated

---

## P01: Explain Local Inference

### Prompt

Explain local inference in this project: running a language model on my own Mac instead of using a cloud API. Compare it with cloud inference in concrete terms.

### Local Model Summary

TODO

### Local Score

TODO/5

### ChatGPT Output Summary

Local inference means running a language model directly on my own computer (for example, a MacBook) instead of sending requests to a cloud AI service over the internet.

With local inference:
- The model files are downloaded and stored on my machine.
- My Mac’s CPU, GPU, and memory do the computation.
- Documents can stay entirely local and private.
- The system can still work without internet access.
- Response speed depends on my hardware.

Example:
If I ask, “Summarize chapter 3 of this PDF,” the request is processed entirely on my Mac.

Cloud inference is different:
- The model runs on servers owned by a provider like OpenAI or Anthropic.
- My prompt and sometimes my documents are sent over the internet.
- The provider’s hardware performs the computation.
- Models are usually larger and more powerful.
- I pay through API usage or subscriptions.

Concrete comparison:

Local inference:
- Privacy: High
- Internet required: No
- Speed: Depends on laptop hardware
- Cost model: Upfront hardware/electricity
- Model size: Usually smaller
- Control/customization: High

Cloud inference:
- Privacy: Data leaves my machine
- Internet required: Yes
- Speed: Depends on network and provider
- Cost model: API fees/subscription
- Model size: Often much larger
- Control/customization: Lower

Summary:
Local inference prioritizes privacy, ownership, and offline capability. Cloud inference prioritizes convenience, scale, and access to larger models.

### ChatGPT Score

TODO/5

### Comparison Notes

TODO

---

## P02: Explain RAG

### Prompt

Explain retrieval-augmented generation in plain English. Use the example of asking questions about a book stored locally on my machine.

### Local Model Summary

TODO

### Local Score

TODO/5

### ChatGPT Output Summary

Retrieval-augmented generation (RAG) is a method where an AI system first looks up relevant information from documents, then uses that information to answer a question.

Plain English example:

Suppose I have a digital copy of a book stored on my laptop.

If I ask:
“What does the author say about religious symbolism?”

The system does not rely only on what the language model already “knows.”
Instead, it:
1. Searches the local book for relevant passages.
2. Retrieves the most relevant sections.
3. Gives those passages to the language model as context.
4. Generates an answer based on the retrieved text.

Without RAG:
- The model might guess.
- It could hallucinate or mix up facts.

With RAG:
- The answer is grounded in the actual source material.
- The system can cite or summarize specific passages.

Simple analogy:
RAG is like giving the AI an open-book exam instead of forcing it to answer entirely from memory.

Summary:
RAG combines document search (“retrieval”) with AI text generation (“generation”) so answers are based on real source material instead of guesses.

### ChatGPT Score

TODO/5

### Comparison Notes

TODO

---

## P04: Extract Main Claim

### Prompt

Given this sentence, identify the main claim: "Dawson treats religion not as one institution within culture, but as a formative center that gives a civilization its symbolic order."

### Local Model Summary

TODO

### Local Score

TODO/5

### ChatGPT Output Summary

Sentence:
“Dawson treats religion not as one institution within culture, but as a formative center that gives a civilization its symbolic order.”

Main claim:
Dawson believes religion is the central organizing force of civilization and culture.

Explanation:
The sentence contrasts two views:
- Religion as just one institution among many.
- Religion as the core force shaping a civilization’s symbols, meaning, and structure.

The author argues Dawson supports the second view.

Summary:
The key idea is that religion fundamentally shapes civilization rather than merely existing inside it.

### ChatGPT Score

TODO/5

### Comparison Notes

TODO

---

## P07: Refuse Unsupported Answer

### Prompt

If the supplied sources do not mention Dawson's view of capitalism, how should an AI assistant answer the question "What did Dawson think of capitalism?"

### Local Model Summary

TODO

### Local Score

TODO/5

### ChatGPT Output Summary

If the supplied sources do not mention Dawson’s view of capitalism, the AI assistant should avoid inventing an answer.

A good response would:
- Clearly state that the available sources do not discuss Dawson’s views on capitalism.
- Avoid speculation or unsupported conclusions.
- Optionally suggest consulting additional sources.

Example response:
“The provided materials do not describe Dawson’s views on capitalism, so I cannot answer that confidently from the supplied sources alone.”

Why this matters:
Large language models can sometimes generate plausible-sounding but unsupported claims. A reliable assistant should distinguish between:
- Information actually present in the sources.
- Information that is unknown or unsupported.

Summary:
The assistant should acknowledge the limitation of the sources rather than hallucinating an answer.

### ChatGPT Score

TODO/5

### Comparison Notes

TODO

---

## P09: Compare Local and Edge Inference

### Prompt

Explain the difference between local inference on a laptop and edge inference in a company deployment.

### Local Model Summary

TODO

### Local Score

TODO/5

### ChatGPT Output Summary

Local inference on a laptop means a single user runs an AI model directly on their personal machine.

Example:
A student runs a small language model on a MacBook to chat with PDFs offline.

Edge inference in a company deployment is broader:
- AI models run on devices or servers close to where data is generated.
- The deployment may involve many devices across an organization.
- The goal is often low latency, privacy, reliability, or reduced cloud costs.

Examples of edge inference:
- Factory cameras detecting defects locally.
- Retail store devices analyzing customer traffic.
- Hospital systems processing sensitive data on-site.
- Company laptops running internal AI assistants without sending data to the cloud.

Key difference:
- Local inference usually describes personal/local model execution.
- Edge inference describes a distributed deployment architecture used by organizations.

Comparison:

Local inference on laptop:
- Single-user setup
- Personal device
- Small-scale
- Often experimental or personal productivity focused

Edge inference:
- Organizational deployment
- Multiple devices or edge servers
- Scalable infrastructure
- Often designed for business operations and security requirements

Summary:
Local inference is an individual use case, while edge inference is an enterprise deployment strategy that keeps AI processing close to the source of the data.

### ChatGPT Score

TODO/5

### Comparison Notes

TODO

---

# Initial Findings

## Where the local model was good enough

TODO

## Where the local model was not good enough

TODO

## What this suggests for Scriptorium

TODO

## Main conclusion

TODO