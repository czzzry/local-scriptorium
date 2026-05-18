# Local Model Baseline Outputs

## Goal

Run the 10 baseline prompts against the local model before adding source grounding, retrieval, or RAG.

This baseline is meant to show what the local model can and cannot do on its own.

## Date

2026-05-18

## Test Conditions

- Local model runner: Ollama
- Model: llama3.2:1b
- Inference location: local Mac
- No source chunks supplied
- No retrieval layer
- No RAG
- No cloud model used for these answers

## Command Pattern

```bash
ollama run llama3.2:1b "PROMPT TEXT"
```
## Prompt 01: Explain Local Inference

### Purpose

Test whether the model understands local inference as a deployment pattern.

### Prompt

Explain local inference in this project: running a language model on my own Mac instead of using a cloud API. Compare it with cloud inference in concrete terms.

### Expected Good Answer

A good answer should explain that local inference means the model runs on the user's own machine. It should contrast this with cloud inference, where the prompt is sent to an external provider's server. It should mention privacy/control tradeoffs and possible limits around speed, hardware, and model quality.

### Local Model Output

Here's how local inference works:

1. **Model definition**: You define your language model using popular libraries like PyTorch or TensorFlow, along with 
a dataset (e.g., a text corpus).
2. **Training**: You train the model using your dataset, either manually or using an existing pre-trained version.
3. **Model storage**: Once trained, you save the model's weights and configuration to disk.
4. **Model loading**: When you want to use the model for inference, you load it from disk using your local machine's 
CPU.

Now, let's compare local inference with cloud-based API inference:

**Cloud-based API inference**

* **Benefits**:
	+ Faster training times due to pre-trained models and distributed computing.
	+ Scalability: multiple instances can run on a single infrastructure, making it suitable for large-scale language 
models.
	+ Convenience: pre-trained models are often available on platforms like Hugging Face's Transformers or TensorFlow Hub.
* **Drawbacks**:
	+ Requires an internet connection to download and upload data.
	+ Limited control over model training and deployment due to external factors (e.g., latency, maintenance).
	+ May require additional infrastructure management and monitoring.

**Local inference**

* **Benefits**:
	+ Complete control over the training process, including dataset selection, model architecture, and hyperparameter 
tuning.
	+ No reliance on internet connectivity or third-party APIs.
	+ Faster development times due to local training and deployment.
* **Drawbacks**:
	+ Requires significant computational resources (e.g., GPU power) and storage capacity.
	+ Longer training times compared to cloud-based inference.
	+ May require manual data preprocessing, model selection, and tuning.

To illustrate the difference, consider a simple language model trained on a dataset of 10 million text samples. With 
local inference:

1. You define your language model using PyTorch.
2. Train the model for 100 epochs on your local Mac ( GPU power: 8 GB).
3. Save the trained model to disk.

With cloud-based API inference, you would use Hugging Face's Transformers model and deploy it on a cloud platform like 
AWS Lambda or Google Cloud Functions.

1. Pre-trained models are uploaded to the cloud API.
2. You trigger an API endpoint that runs your local language model using PyTorch.
3. The response is sent back to the client, which can then use it for further processing (e.g., sentiment analysis).

In summary, local inference offers complete control and faster development times, but requires significant 
computational resources and longer training times. Cloud-based API inference provides scalability and convenience, but 
may require manual intervention and more complex infrastructure management.

### Notes

Weak / confused answer.

The model correctly recognized that local inference involves running something on the local machine rather than relying fully on a cloud API, but it confused inference with model training. It described defining a model in PyTorch/TensorFlow, training on a dataset, saving weights, and tuning hyperparameters. That is not the MVP goal.

For this project, local inference means using an already-trained local model through Ollama to generate answers on my Mac. The key distinction is where answer generation happens, not whether I personally train the model.

Failure modes:
- conflates inference with training
- overcomplicates the answer
- introduces irrelevant ML-engineering details
- sounds confident despite misunderstanding the task

Usefulness: 1/5

Result:
Mostly failed.

Reason:
The answer recognized that local computation is involved, but it confused local inference with local model training. It overemphasized PyTorch/TensorFlow, datasets, training, weights, hyperparameter tuning, and GPU requirements. For this project, local inference means using an already-trained model through Ollama to generate answers on my Mac.

Main failure mode:
Conflates inference with training.

---

## Prompt 02: Explain RAG

### Purpose

Test whether the model can explain retrieval-augmented generation clearly.

### Prompt

Explain retrieval-augmented generation in plain English. Use the example of asking questions about a book stored locally on my machine.

### Expected Good Answer

A good answer should explain that the system first retrieves relevant passages from the book, then gives those passages to the model so it can answer from them. It should not imply that the model magically knows the book without being given the text.

### Local Model Output

Retrieval-Augmented Generation (RAG) is a type of AI model that helps you find what you're looking for by combining 
the power of search with the understanding of human behavior.

Let's use an example to illustrate this:

Imagine you're at home, and you want to find a book on your local bookshelf. You know it's there because it was placed 
there when you moved in. But, instead of searching through every single book on the shelf (which would be tedious), 
RAG takes a more nuanced approach.

RAG starts by looking for clues about where the book might be located. These clues can be things like:

* "Is this book on the top shelf?"
* "Is it next to something else?"
* "Does it have any pictures or reviews on it?"

If RAG finds multiple possible locations, it will then look up specific answers (like "yes" or "no") and provide them 
as a list of options. This process continues until it finds the book you're looking for.

Here's an example:

RAG asks itself: "Is this book on the top shelf?" It finds that yes, it is. So RAG adds "top shelf" to its list of 
possible locations.

Next, RAG asks: "Is there anything else next to this book?" After a quick scan, RAG finds that "yes," there are some 
books on a nearby table. So RAG adds "table next to top shelf" to its list.

RAG continues this process, adding more clues and narrowing down the possible locations until it finally finds the 
book you're looking for: a worn copy of your favorite novel.

That's retrieval-augmented generation in action! It uses search as a starting point and then applies human-like 
reasoning to refine the results.

### Notes

Partial but weak answer.

The model understood that RAG involves retrieving relevant information before answering, and the bookshelf analogy loosely captures the idea of searching for relevant material. However, it did not clearly explain the actual RAG pipeline.

It incorrectly framed RAG as a type of AI model rather than as a system architecture/pattern. It also focused too much on a vague search-and-reasoning analogy and did not explain that retrieved passages are inserted into the model prompt before answer generation.

For this project, the important RAG flow is:

question → retrieve relevant source chunks → pass chunks to local model → generate grounded answer → cite source IDs

Failure modes:
- vague analogy
- treats RAG as a model rather than an architecture
- misses the retrieval-to-prompt-to-generation flow
- does not mention source chunks or grounded answers clearly

Result: partial fail
Usefulness: 2/5
Main issue: vague analogy, incomplete technical explanation
---

## Prompt 03: Source-Grounded Answer Rules

### Purpose

Test whether the model can define rules for answering only from supplied sources.

### Prompt

Give me rules for answering questions using only supplied source excerpts. The answer should avoid making claims that are not supported by the excerpts.

### Expected Good Answer

A good answer should mention using only the supplied text, citing source IDs, separating evidence from interpretation, flagging uncertainty, and refusing to answer when sources are insufficient.

### Local Model Output

Here are some general rules for answering questions using only provided source excerpts, while avoiding claims that 
are not supported by the text:

1. **Stick to verifiable facts**: Only report information that can be confirmed through the sources you've read or 
accessed.
2. **Avoid assumptions and interpretations**: Refrain from making inferences or drawing conclusions based on the 
excerpt alone. Instead, focus on extracting specific details and data mentioned in the source.
3. **Limit claims to what's explicitly stated**: If an excerpt says "this study found that...", avoid making claims 
like "it's concluded that..." or "the results show that...". Instead, state the exact phrase used by the author, such 
as "it was found to be true".
4. **Use the sources' language and tone**: When quoting the excerpt, try to match the author's voice, tone, and 
writing style. This will help you sound more accurate and trustworthy.
5. **Be transparent about your process**: Explain how you've interpreted or analyzed the source to support your 
answer. For example, "I based my response on the key findings stated in paragraph 3 of the report".
6. **Avoid speculative language**: Refrain from using phrases like "in general", "it's worth noting that...", or 
"notably", which can imply unsubstantiated opinions.
7. **Use quotes accurately**: If you're quoting someone directly, use their exact words and punctuation as written in 
the source.

By following these guidelines, you'll be able to provide answers that are grounded in the provided excerpts and 
demonstrate a clear understanding of the material.

### Notes

Usefulness: 4/5

Result:
Mostly successful.

Reason:
The model gave useful rules for answering from supplied source excerpts. It correctly emphasized source-supported claims, avoiding unsupported assumptions, using accurate quotes, and being transparent about how the answer was derived.

Weaknesses:
The answer was slightly too restrictive about avoiding interpretation. For Scriptorium, interpretation is allowed, but it should be clearly labeled and grounded in evidence. The model also did not mention source IDs, an uncertainty section, or refusing to answer when sources are insufficient.

Main failure modes:
- missing source-ID requirement
- weak distinction between evidence and interpretation
- does not explicitly require insufficient-evidence caveats
---

## Prompt 04: Extract Main Claim

### Purpose

Test whether the model can identify the main claim in a single sentence.

### Prompt

Given this sentence, identify the main claim: "Dawson treats religion not as one institution within culture, but as a formative center that gives a civilization its symbolic order."

### Expected Good Answer

A good answer should say that the main claim is that Dawson sees religion as central or formative for culture/civilization, not merely as one institution among others.

### Local Model Output

The main claim of the given sentence is that Dawson views religion as a central aspect or "formative center" that 
shapes a society's (or civilization's) cultural and symbolic framework.

### Notes

Usefulness: 5/5

Result:
Successful.

Reason:
The model correctly identified the main claim: Dawson sees religion as a formative center of culture/civilization, not merely as one institution among others. The answer is concise, accurate, and does not add unsupported claims.

Main failure modes:
None significant for this prompt.
---

## Prompt 05: Separate Evidence from Interpretation

### Purpose

Test whether the model can distinguish evidence from interpretation.

### Prompt

Explain the difference between evidence and interpretation when answering a question about a historical author.

### Expected Good Answer

A good answer should say that evidence is what the source directly says or shows, while interpretation is the reasoned explanation of what that evidence means. It should warn against presenting interpretation as if it were direct textual evidence.

### Local Model Output

When answering a question about a historical author, it's essential to distinguish between two concepts: evidence and 
interpretation.

Evidence refers to facts, data, or objects that can be verified through research, observation, and documentation. It 
involves:

1. Collecting and analyzing primary sources (e.g., texts, images, artifacts) from the time period.
2. Using these sources to support claims about the author's life, work, and ideas.
3. Drawing conclusions based on careful examination of the evidence.

Interpretation, on the other hand, involves making sense of the evidence by drawing conclusions, inferences, or 
interpretations about the author's meaning, intentions, and significance. It often involves:

1. Analyzing the language, tone, and style used in the primary sources.
2. Considering historical context, social norms, and cultural values that influenced the author's work.
3. Using the evidence to build a narrative or argument about the author's thought process, motivations, and impact.

To answer a question about a historical author effectively:

1. Focus on verifiable facts from primary sources (e.g., texts, letters, diaries).
2. Be cautious of interpretations that are not supported by evidence.
3. Avoid making assumptions or speculative conclusions based solely on the evidence.

By understanding the difference between evidence and interpretation, you can critically evaluate historical sources, 
construct a nuanced understanding of an author's work, and provide accurate and thoughtful responses to questions 
about their life and ideas.

### Notes

Usefulness: 4.5/5

Result:
Successful.

Reason:
The model clearly distinguishes evidence from interpretation. It correctly explains that evidence comes from verifiable sources, while interpretation involves reasoning about meaning, context, intention, and significance. This is directly relevant to Scriptorium because the system needs to avoid presenting interpretation as if it were direct evidence.

Weaknesses:
The answer is somewhat generic, but that is expected because the prompt itself was general. It did not mention source IDs or retrieved chunks, but the prompt did not ask for a RAG-specific answer. A better future prompt would explicitly ask the model to explain evidence vs interpretation in the context of source chunks and source IDs.

Main failure modes:
- somewhat generic
- could better distinguish supported interpretation from speculation

---

## Prompt 06: Identify Uncertainty

### Purpose

Test whether the model can identify what can and cannot be safely concluded from a limited source excerpt.

### Prompt

A source excerpt says: "Dawson criticizes purely economic explanations of civilization." What can we safely conclude from this, and what can we not conclude?

### Expected Good Answer

A good answer should say that Dawson criticizes explanations that reduce civilization to economics alone. It should not conclude that he thinks economics is irrelevant, that he rejects capitalism, or that he has a fully developed alternative theory unless the source says so.

### Local Model Output

From the given source excerpt:

* We can conclude that Dawson is criticizing a particular approach or perspective to understanding civilization.
* The specific critique is of purely economic explanations, which suggests that Dawson may be arguing that economics 
alone cannot fully explain the complexities of human societies.

We can safely conclude the following:

* Dawson likely believes that economic factors are not sufficient to account for cultural and social changes in 
civilizations.
* He may argue that other factors, such as politics, sociology, or psychology, play a more significant role in shaping 
civilization.

However, we cannot safely conclude the following:

* That Dawson is opposed to all economic explanations of civilization.
* That he believes economics has no explanatory power at all.
* The extent to which he actually criticizes purely economic explanations or what specific economic factors he targets 
is unknown without further information.

### Notes

Usefulness: 4.5/5

Result:
Successful.

Reason:
The model correctly identifies that the excerpt supports a limited conclusion: Dawson criticizes purely economic explanations of civilization, likely because he thinks economics alone is insufficient. It also correctly refuses to overextend the claim into stronger conclusions, such as saying Dawson rejects economics entirely or opposes all economic explanations.

Strengths:
- separates safe conclusions from unsafe conclusions
- avoids overclaiming
- recognizes that more source material would be needed
- gives a good example of uncertainty handling

Weaknesses:
The answer slightly speculates when it says Dawson may think politics, sociology, or psychology play a more significant role. That might be plausible, but the supplied excerpt does not establish those specific alternatives. A more careful answer would say only that Dawson likely thinks non-economic factors also matter, without naming specific factors unless the source does.

Main failure modes:
- minor unsupported speculation
- otherwise strong uncertainty handling

---

## Prompt 07: Refuse Unsupported Answer

### Purpose

Test whether the model knows how to avoid unsupported claims.

### Prompt

If the supplied sources do not mention Dawson's view of capitalism, how should an AI assistant answer the question "What did Dawson think of capitalism?"

### Expected Good Answer

A good answer should refuse to invent an answer. It should say that the supplied sources do not establish Dawson's view of capitalism and that more source material is needed.

### Local Model Output

If the provided sources do not mention Dawson's views on capitalism specifically, it would be more accurate and safe 
to provide a generic response that avoids speculation or assuming Dawson's opinion on the topic.

Here are a few options:

* You could say: "The source does not provide information about what Dawson thought of capitalism. To determine his 
views, we would need additional context or evidence from other sources."
* Another option is: "Unfortunately, there is no mention of Dawson's views on capitalism in the provided text. We 
cannot conclude anything about his thoughts on this topic based solely on these sources."
* You could also say: "Without more information or context about Dawson's work or statements, it is not possible to 
determine what he thought of capitalism."

These responses acknowledge that the sources do not provide sufficient information to infer Dawson's views on 
capitalism and instead highlight the need for additional evidence or context.


### Notes

Usefulness: 5/5

Result:
Successful.

Reason:
The model correctly refuses to invent Dawson's view of capitalism when the supplied sources do not mention it. It gives several safe answer formulations that acknowledge the lack of evidence and request additional source material. This is exactly the behavior needed for source-grounded answering.

Strengths:
- refuses unsupported speculation
- clearly says the provided sources are insufficient
- gives safe response templates
- does not overclaim
- keeps the answer tied to available evidence

Weaknesses:
None significant for this prompt.

Main failure modes:
None significant.

---

## Prompt 08: Summarize a Passage

### Purpose

Test whether the model can summarize a short abstract passage.

### Prompt

Summarize this passage in three bullets: "A civilization is not held together only by laws, markets, or armies. It also depends on inherited symbols, rituals, loyalties, and assumptions about the sacred."

### Expected Good Answer

A good answer should mention that civilization depends on more than institutions or force, that symbolic/cultural inheritance matters, and that sacred assumptions can help bind a civilization together.

### Local Model Output

Here are three bullets summarizing the passage:

• A civilization's structure is more complex than just its material institutions (laws, markets, armies).
• Symbolic, ritualistic, and cultural elements play a crucial role in holding a civilization together.
• Inherited symbols, rituals, loyalties, and assumptions about the sacred shape the social fabric of a civilization.

### Notes

Usefulness: 5/5

Result:
Successful.

Reason:
The model accurately summarizes the passage in three bullets and preserves the main ideas: civilization is not held together only by material or institutional forces, symbolic and ritual elements matter, and inherited sacred assumptions help shape social cohesion.

Strengths:
- follows the requested three-bullet format
- captures the main claim clearly
- does not add unsupported claims
- keeps the summary concise
- preserves the distinction between material institutions and symbolic/sacred order

Weaknesses:
None significant for this prompt.

Main failure modes:
None significant.


---

## Prompt 09: Compare Local and Edge Inference

### Purpose

Test whether the model can distinguish local inference from edge inference.

### Prompt

Explain the difference between local inference on a laptop and edge inference in a company deployment.

### Expected Good Answer

A good answer should explain that local inference on a laptop is single-device inference, while edge inference usually means running models near users/data across endpoint devices, local servers, branches, factories, hospitals, or other non-centralized environments. It should say the concepts overlap but are not identical.

### Local Model Output

Local inference on a laptop refers to the process of making decisions or computations at the individual user's device, 
typically when interacting with an application or service that is designed for mobile devices (e.g., tablets, 
smartphones). In this context:

* The laptop is considered the "local" device because it makes the decision or computation directly.
* No external cloud-based services are involved in making the inference.
* The laptop's own memory and processing power are used to perform the inference.

On the other hand, edge inference occurs when an application or service needs to make decisions or computations at a 
centralized server, but instead of performing the operation locally on the device, it sends the request to the edge 
(the nearest cell tower) to forward the data. The data is then processed by the cloud-based servers before being 
returned to the client.

* Edge inference involves:
	+ Sending requests to an external cloud-based service
	+ Data processing occurs at a centralized server
	+ The results are sent back to the device

Key differences:

* **Device involvement**: Local inference involves individual devices, while edge inference involves central servers.
* **Cloud involvement**: Local inference does not involve cloud services, whereas edge inference requires some level 
of cloud connectivity.
* **Decision-making process**: Local inference makes decisions directly on the device's local data, whereas edge 
inference sends requests to a server for processing and then returns the results.

### Notes

Usefulness: 2/5

Result:
Mostly failed.

Reason:
The model partly explains local inference correctly: it says computation happens on the local device and does not require an external cloud service. However, it gives a poor and misleading explanation of edge inference.

The major error is that it describes edge inference as sending data to "the edge (the nearest cell tower)" and then onward to centralized cloud servers. That is not the core meaning of edge inference. Edge inference usually means running the model near the user/data, such as on endpoint devices, local servers, branch-office servers, factory machines, hospital infrastructure, or other non-central cloud environments.

Strengths:
- correctly says local inference uses the local device's compute
- correctly contrasts local inference with external cloud processing in broad terms

Weaknesses:
- misunderstands edge inference
- treats edge as basically a routing layer to cloud servers
- over-focuses on cell towers/mobile networks
- misses local/on-prem/company-site edge deployment patterns
- creates a false contrast between local device and centralized server

Main failure modes:
- incorrect technical definition
- misleading architecture explanation
- overconfident wrong answer

---

## Prompt 10: Failure Modes

### Purpose

Test whether the model can identify realistic failure modes for an AI research assistant.

### Prompt

List five ways a local AI research assistant could give a bad answer when asked about a source text.

### Expected Good Answer

A good answer should mention hallucination, bad retrieval, misunderstanding the question, using unsupported claims, missing nuance, confusing sources, or being overconfident when evidence is weak.

### Local Model Output

Here are five ways a local AI research assistant could provide an inaccurate or misleading answer when asked about a 
source text:

1. **Misinterpretation of quotes**: The researcher might misquote the source, taking it out of context or using it to 
support an unrelated idea.

Example: "According to [Source], 'AI is a solution to poverty.' This quote is taken from an interview with a tech 
industry expert."

2. **Inaccurate or incomplete information**: The research assistant might provide partial or misleading information 
about the source, such as not mentioning key details or omitting important context.

Example: "The article mentions that [Source] advocates for increased government funding for AI research but omits its 
discussion on potential ethical concerns."

3. **Incorrect attribution**: The researcher might incorrectly attribute a statement to the wrong person or 
organization.

Example: "According to [Source], 'AI is a key driver of economic growth.' This quote is actually from a speech by a 
business leader, not an academic study."

4. **Misleading language**: The research assistant might use ambiguous or misleading language to describe the source 
text, making it appear more complex than it actually is.

Example: "The article discusses [Source]'s analysis of AI's impact on society and argues that 'AI is a threat to human 
relationships.' This quote is taken from an academic paper published in a journal, but its actual content is quite 
different."

5. **Oversimplification or misrepresentation**: The researcher might oversimplify or distort the source text to fit 
their own perspective or make it appear more convincing.

Example: "According to [Source], 'AI is not just about automation; it's about creating new jobs and opportunities for 
all.' This quote is taken from a report by an industry think tank, but its actual content is much more nuanced."

These errors can lead to inaccurate or misleading responses when asked about source texts, which can have serious 
consequences in fields like academia, research, and policy-making.

### Notes

Usefulness: 4/5

Result:
Successful.

Reason:
The model identifies several realistic failure modes for an AI research assistant working with source texts: misquoting, omitting context, incorrect attribution, misleading wording, and oversimplification. These are directly relevant to Scriptorium because the assistant must avoid distorting source material while sounding confident.

Strengths:
- identifies realistic source-handling failures
- emphasizes context, attribution, and nuance
- recognizes that misleading answers can come from partial or distorted use of evidence
- relevant to future evaluation criteria

Weaknesses:
The examples are somewhat clumsy and oddly focused on AI-policy examples rather than books or historical/theological texts. It also misses some important RAG-specific failure modes, such as bad retrieval, confusing one source with another, hallucinating citations, or answering from general model knowledge instead of retrieved chunks.

Main failure modes:
- generic examples
- not Scriptorium-specific
- misses retrieval-specific failures
