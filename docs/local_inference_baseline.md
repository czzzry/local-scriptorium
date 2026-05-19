# Local Inference Baseline

## Goal

Test whether a small local model running through Ollama on my Mac can produce useful answers before adding source grounding, retrieval, or RAG.

The purpose of this baseline is not to prove that the local model is excellent. The purpose is to understand what it can and cannot do on its own.

## Setup

- Machine: current Mac
- Local model runner: Ollama
- Model tested: llama3.2:1b
- Inference location: local Mac
- No source chunks supplied
- No retrieval layer
- No RAG
- No cloud model used for the local baseline outputs

Relevant project artifacts:

- `docs/hardware_baseline.md`
- `docs/ollama_installation_log.md`
- `outputs/local_model_hello_world.md`
- `evals/local_model_baseline_prompts.md`
- `outputs/local_model_baseline_outputs.md`
- `outputs/local_vs_chatgpt_comparison.md`

## What Worked

The local model successfully ran on my Mac through Ollama and generated responses from the command line.

The model performed reasonably well on constrained text-analysis tasks, especially:

- extracting the main claim from a sentence
- summarizing a short passage
- refusing to answer when sources were insufficient
- identifying uncertainty from a limited excerpt
- explaining general evidence vs interpretation distinctions

These results suggest that a small local model may be useful inside Scriptorium if the task is tightly scoped and the relevant source material is supplied clearly.

## What Failed

The local model struggled with abstract AI architecture concepts.

The most important failures were:

- confusing local inference with local model training
- explaining RAG vaguely or incorrectly
- misunderstanding edge inference
- introducing unnecessary ML-engineering concepts
- sounding confident even when the answer was wrong or misleading

These failures show that a working local model is not the same as a reliable AI system.

## Comparison With ChatGPT

ChatGPT produced clearer and more accurate answers for the selected comparison prompts, especially for architecture concepts like local inference, RAG, and edge inference.

However, ChatGPT is used here as a stronger reference model, not as an unquestionable source of truth. Final correctness should be judged against explicit expected-answer criteria, source documentation where relevant, and logical consistency.

The comparison suggests that the small local model is not reliable as a general technical explainer, but may still be useful for narrow source-grounded tasks.

## Key Learning

The main lesson is that local inference works technically, but raw local generation is not enough.

A useful local AI research assistant needs:

- clear source material
- source chunks
- retrieval
- structured prompts
- source IDs
- uncertainty handling
- evaluation

This supports the original Scriptorium architecture:

source files → chunks with source IDs → retrieval → local model inference → grounded answer → evaluation

## Implications for Scriptorium

The local model should not be treated as an independent authority.

Instead, it should be treated as a local generation engine that receives carefully selected source chunks and produces constrained answers.

The next phase should therefore focus on source preparation and chunking rather than more model experimentation.

## Decision

Proceed to the source corpus and chunking phase.

The MVP should continue using Ollama and llama3.2:1b as the baseline local model for now. More powerful local models can be tested later, but the next learning bottleneck is the source → chunk → retrieve workflow, not model selection.

## Next Phase

Next tickets:

1. Select first source corpus
2. Create source metadata file
3. Clean first source files
4. Create chunk ID convention
5. Create first chunks