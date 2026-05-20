# Grounding Failure Notes

## Goal

Document the results of the first manual RAG prompt comparison.

This note summarizes what happened when the local model was asked to answer selected Boethius questions with and without supplied source chunks.

The purpose is not to pretend the first grounded test succeeded. The purpose is to identify where the current pipeline is working and where it still fails.

## Related Artifacts

Question set:

`evals/manual_rag_questions.md`

Manual evidence map:

`evals/manual_rag_chunk_map.md`

Prompt comparison output:

`outputs/manual_rag_prompt_test.md`

Chunk file:

`chunks/boethius_consolation_chunks.json`

Runner script:

`scripts/run_manual_rag_test.py`

## Summary of Results

The first manual RAG prompt test produced mixed results.

Providing source chunks improved topical relevance in some cases, especially for the question about Fortune. However, the grounded prompt did not reliably produce well-supported answers.

The most important finding is:

> Relevant chunks plus a source-use instruction do not guarantee a grounded answer.

This means the pipeline must evaluate both retrieval and generation separately.

## Retrieval vs Generation

The SCRIP-20 manual chunk map helped identify likely relevant chunks for each question.

For SCRIP-21, the model was given those selected chunks directly. This means retrieval was manually controlled for the test.

Therefore, when the grounded answer failed, the likely issue was not retrieval. The more likely issues were:

- weak local model behavior
- insufficiently strict grounded prompt format
- difficulty extracting meaning from literary/allegorical text
- failure to follow citation instructions
- failure to handle insufficient-evidence questions

## Question-Level Findings

### Q01: Philosophy and Poetry

Question:

What is the relationship between Philosophy and the Muses of Poetry at the beginning of the work?

Finding:

The grounded answer failed to capture the obvious antagonism between Philosophy and the Muses of Poetry.

The supplied chunks contained enough evidence to answer better. Chunk 001 shows the female figure rebuking the Muses of Poetry and accusing them of feeding Boethius with sweet poison rather than healing him. Chunk 003 helps identify the female figure as Philosophy.

Failure mode:

The model received relevant evidence but failed to extract the central relationship.

Likely issue:

Generation failure, not retrieval failure.

### Q03: Fortune's Nature

Question:

How does Philosophy describe the nature of Fortune?

Finding:

The grounded answer was better than the ungrounded answer because it focused on mutability and changeability rather than giving a generic philosophical survey.

However, it still did not cite chunk IDs and remained somewhat loose.

Failure mode:

Partial success. Grounding improved topic relevance but not citation discipline or precision.

Likely issue:

Prompt format needs to force evidence-backed claims.

### Q09: Insufficient Evidence — Christianity

Question:

Based only on the selected Boethius chunks, can we say whether the work is explicitly Christian?

Finding:

The grounded answer failed badly. It introduced unsupported context and summarized providence/free will instead of answering the actual evidence question.

The correct behavior should have been:

The supplied chunks contain theological language about God, providence, prayer, judgment, and divine knowledge, but they are not sufficient by themselves to prove that the work is explicitly Christian unless explicitly Christian markers are present in the chunks.

Failure mode:

Insufficient-evidence failure and hallucination.

Likely issue:

The model did not follow the instruction to limit itself to the supplied chunks.

## Main Failure Modes

### 1. Missing the central relation in supplied evidence

The model failed Q01 even though the relevant chunks were supplied.

This shows that giving evidence is not enough. The model must also be able to interpret and prioritize the evidence correctly.

### 2. Weak citation discipline

The grounded prompt instructed the model to cite chunk IDs, but the model often failed to do so.

This means future prompts should require a stricter answer structure.

### 3. Outside-context hallucination

The Q09 grounded answer introduced unsupported contextual claims.

This is especially important because the test question explicitly asked the model to reason only from selected chunks.

### 4. Poor insufficient-evidence handling

The model did not reliably say:

> The supplied chunks are not enough to determine this.

This is a major RAG failure mode. A trustworthy research assistant must know when not to answer.

### 5. Literary/allegorical extraction difficulty

The model struggled with symbolic literary material, especially the relationship between Philosophy and Poetry in the opening scene.

This suggests that smaller local models may struggle more with interpretive humanities-style source material than with simple factual lookup.

## What Worked

- The project now has a repeatable script for running grounded and ungrounded prompts.
- The output format makes comparison easy.
- The manual evidence map is useful.
- Q03 showed that chunks can improve topical relevance.
- The failure cases are clear enough to guide the next iteration.

## What Did Not Work

- The grounded prompt was not strict enough.
- The local model did not reliably cite chunk IDs.
- The local model did not reliably refuse or caveat when evidence was insufficient.
- Supplying chunks did not prevent hallucination.
- The current answer format does not force the model to show evidence before concluding.

## Recommended Improvements

### 1. Use a stricter grounded prompt format

Future grounded prompts should require this structure:

```text
Direct answer:

Evidence:
- CHUNK_ID: relevant quote or paraphrase
- CHUNK_ID: relevant quote or paraphrase

What the chunks do not show:

Confidence: