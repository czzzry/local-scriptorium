# Automated Local Model Baseline Run

## Goal

Run the baseline prompt set against the local model using an automated script.

## Run Metadata

- Date/time: 2026-05-19 17:37:30
- Model: llama3.2:1b
- Local model runner: Ollama
- Inference location: local Mac
- Prompt source: `evals/local_model_baseline_prompts.json`
- Script: `scripts/run_ollama_baseline.py`
- No source chunks supplied
- No retrieval layer
- No RAG
- No cloud model used for these answers

---

## P01: Explain Local Inference

### Prompt

```text
Explain local inference in this project: running a language model on my own Mac instead of using a cloud API. Compare it with cloud inference in concrete terms.
```

### Local Model Output

```text
Local inference refers to the process of training and deploying a language model directly on your own machine (in this case, a Mac) rather than relying on a cloud-based API. Here's how it works:

**Cloud Inference:**

When you use a cloud API for inference, the following occurs:

1. Your request is sent to the cloud server.
2. The cloud server processes the input and generates an output.
3. The output is returned to your application or user interface.

In contrast, local inference involves training and deploying a language model on your own machine (in this case, a Mac). Here's what happens:

1. Your machine, e.g., Mac, has a CPU, GPU, or specialized hardware capable of executing the necessary computations.
2. A pre-trained language model is downloaded from a cloud API or other source.
3. The downloaded model is loaded into memory on your machine.
4. When you ask for inference (e.g., generating text), the local inference process starts:
 * The input data (e.g., text, question) is fed into the trained model.
 * The model's parameters are used to generate output.
5. The resulting output is sent back through your application or user interface.

Now, let's consider a concrete example:

Suppose you have a pre-trained BERT (Bidirectional Encoder Representations from Transformers) language model on a cloud API that can be accessed via the Hugging Face API. You want to use it for local inference on your Mac. Here's what would happen:

* Your Mac loads the BERT model, which requires some computational resources.
* When you ask Hugging Face to generate text (e.g., "What is the meaning of life?"), the system sends the input data and requests a response from the cloud API.
* The cloud API processes the request, generates an output, and returns it back to your Mac.
* Your Mac receives the output and displays it in your application or user interface.

In contrast, if you used a local inference process on your own Mac:

* You would need to download the pre-trained BERT model from Hugging Face's website.
* The downloaded model would be saved locally on your Mac.
* When you ask Hugging Face for inference (e.g., "What is the meaning of life?"), your Mac would load the local model, use it to generate output, and send the result back through your application or user interface.

In this example, the local inference process saves computational resources by not relying on cloud infrastructure. However, you need to have access to a stable internet connection and ensure that your machine meets the necessary requirements for running the local BERT model.
```

### Runtime

27.02 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P02: Explain RAG

### Prompt

```text
Explain retrieval-augmented generation in plain English. Use the example of asking questions about a book stored locally on my machine.
```

### Local Model Output

```text
Retrieval-Augmented Generation (RAG) is a way to generate new text that's more helpful and interesting than simply rephrasing or summarizing existing content.

Imagine you have a book on your local machine, let's say it's called "The Art of Writing". One day, you ask the computer what a particular author's writing style is like. The computer might tell you some general characteristics (e.g., they're known for using descriptive language), but it wouldn't necessarily show you how to apply those techniques in your own writing.

In RAG, the computer tries to answer more specific questions about the book, such as "What are the most common sentence structures used by this author?" or "Can you provide an example of a passage that uses metaphors effectively?"

The computer's goal is to not only provide accurate answers but also help you generate new text based on what it's learned. This can lead to more interesting and relevant content, as well as better understanding of the original material.

For example, if the computer says "This author often uses analogies in their writing", it might then suggest a sentence like: "In her essay 'The Power of Simplicity', Johnson uses an analogy between simplicity and abundance to make a powerful point about consumerism."

RAG is similar to other forms of question-answering, but instead of just providing answers, the computer tries to generate new text that's related to what you're asking. This can help create more engaging and useful content for the user.
```

### Runtime

15.48 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P03: Source-Grounded Answer Rules

### Prompt

```text
Give me rules for answering questions using only supplied source excerpts. The answer should avoid making claims that are not supported by the excerpts.
```

### Local Model Output

```text
Here are some general rules for answering questions using only provided source excerpts, aiming to avoid making claims that are not supported by the text:

1. **Be selective**: Only use excerpts that directly address the question or provide relevant information.
2. **Focus on key terms**: Highlight specific phrases or words from the excerpt that accurately convey your answer's main point.
3. **Avoid assumptions**: Refrain from making assumptions about the topic, context, or reader background that aren't explicitly stated in the excerpt.
4. **Stick to verifiable facts**: Only include information that can be verified through credible sources and is supported by evidence within the text.
5. **Use quotes judiciously**: When using a quote, paraphrase or summarize it to ensure accuracy and avoid misattributing ideas or words.
6. **Don't imply unknowns**: Avoid stating what's not explicitly stated in the excerpt, as this can be misleading.
7. **Be transparent about sources**: Acknowledge the source of your information (e.g., "According to [Source X]") when using a quotation or paraphrasing an idea.

Here are some specific rules for different types of questions:

* For factual questions:
	+ Only use information explicitly stated in the excerpt.
	+ Verify facts through credible sources.
* For opinion-based questions:
	+ Avoid making claims that aren't supported by the text (e.g., "Some people think...")
	+ Focus on presenting a balanced view or alternative perspectives.
* For analysis-style questions:
	+ Use excerpts to support your analysis and interpretation of the information.
	+ Avoid making value judgments or providing conclusions without sufficient evidence.

Remember, the goal is to provide accurate, verifiable information that aligns with the original source's intent.
```

### Runtime

20.78 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P04: Extract Main Claim

### Prompt

```text
Given this sentence, identify the main claim: "Dawson treats religion not as one institution within culture, but as a formative center that gives a civilization its symbolic order."
```

### Local Model Output

```text
The main claim of this sentence is that Dawson views religion as a central and fundamental aspect of a civilization's cultural identity, rather than just one aspect of various social institutions. In other words, he argues that religion plays a crucial role in shaping the overall structure and meaning of a society.
```

### Runtime

4.88 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P05: Separate Evidence from Interpretation

### Prompt

```text
Explain the difference between evidence and interpretation when answering a question about a historical author.
```

### Local Model Output

```text
When discussing a historical author, it's essential to distinguish between evidence and interpretation to provide an accurate and nuanced understanding of their work.

Evidence refers to specific facts, data, or materials that support or contradict a particular statement or theory about the author or their work. This can include:

1. Primary sources: Original texts, documents, letters, diaries, or other primary materials that were written by the author themselves.
2. Secondary sources: Academic studies, reviews, essays, or analyses written by scholars or historians that interpret and analyze the author's work based on these primary sources.
3. Contextual information: Information about the historical period, cultural context, social norms, and intellectual currents in which the author wrote.

Interpretation, on the other hand, involves making sense of evidence to draw conclusions about the author's intentions, meaning, or significance. This can include:

1. Analyzing language and style: Understanding how the author used literary devices, such as symbolism, imagery, or tone, to convey their message.
2. Examining themes and motifs: Identifying recurring ideas, emotions, or concerns that appear throughout the work.
3. Considering historical context: Understanding how the author's work reflects, challenges, or responds to the social, cultural, or intellectual issues of their time.

To provide a clear example:

* A historian might say, "The novel 'War and Peace' by Leo Tolstoy was written during the Napoleonic Wars." (Evidence) This statement is supported by historical records and context.
* However, if someone were to analyze Tolstoy's writing style in the novel, examine how it reflects his philosophical views on history and human nature, or consider how it responds to the societal issues of the time, they might draw a different conclusion about Tolstoy's intentions. (Interpretation)

In this case, the historian provides evidence from the text itself, while the analyst uses interpretation to make connections between that evidence and Tolstoy's broader philosophical ideas.

It's essential to note that these two concepts are not mutually exclusive, and historians often use a combination of both evidence and interpretation to construct a nuanced understanding of an author's work.
```

### Runtime

18.50 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P06: Identify Uncertainty

### Prompt

```text
A source excerpt says: "Dawson criticizes purely economic explanations of civilization." What can we safely conclude from this, and what can we not conclude?
```

### Local Model Output

```text
From the excerpt, we can deduce the following:

* Dawson is expressing a critical view of economic explanations for human society or civilization.
* This suggests that he may be skeptical of economic theories that attempt to explain societal development in purely materialistic terms.

What we cannot safely conclude from this excerpt:

* It's impossible to determine Dawson's specific views on other aspects of sociology, anthropology, or cultural studies. The excerpt only provides information about his critique of economic explanations.
* Dawson may not have explicitly stated what he means by "civilization." While he criticizes purely economic explanations, it's possible that he has other criticisms in mind as well.
* We can't assume Dawson is dismissing all economic theories or models without evidence. His critique might be targeted at specific aspects of economics that he disagrees with, rather than rejecting the entire field of study.
```

### Runtime

7.87 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P07: Refuse Unsupported Answer

### Prompt

```text
If the supplied sources do not mention Dawson's view of capitalism, how should an AI assistant answer the question "What did Dawson think of capitalism?"
```

### Local Model Output

```text
If the provided sources (or in this case, you) do not mention Dawson's views on capitalism, it would be reasonable for an AI assistant to respond by:

1. Acknowledging the absence of a specific quote or statement.
2. Explaining that without direct quotes or references to his views, it is not possible to accurately summarize his perspective on capitalism.

A possible response could be:

"I'm sorry, I don't have any information about Dawson's views on capitalism from your sources. If you could provide more context or clarify which sources you're referring to, I'd be happy to try and help further."
```

### Runtime

5.44 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P08: Summarize a Passage

### Prompt

```text
Summarize this passage in three bullets: "A civilization is not held together only by laws, markets, or armies. It also depends on inherited symbols, rituals, loyalties, and assumptions about the sacred."
```

### Local Model Output

```text
Here are three bullets summarizing the passage:

• A civilization's foundation goes beyond its formal institutions.
• Symbols, rituals, loyalty, and assumptions about a shared understanding of the world are crucial in holding a society together.
• Inherited cultural elements play a significant role in shaping a civilization's identity.
```

### Runtime

3.21 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P09: Compare Local and Edge Inference

### Prompt

```text
Explain the difference between local inference on a laptop and edge inference in a company deployment.
```

### Local Model Output

```text
Local inference on a laptop refers to the process of executing machine learning models directly within an organization's internal infrastructure, such as a private data center or cloud environment. In this setup, the model is running on a centralized server that is accessible from multiple laptops, allowing users to access and run models without relying on external cloud services.

On the other hand, Edge inference in a company deployment refers to a specific use case where machine learning models are deployed at the edge of the network, i.e., closer to the end-users. This typically occurs when a company deploys its own private edge computing infrastructure, which includes edge devices such as gateways, switches, and appliances, that run AI and ML workloads directly.

Here's how the key differences between local inference on laptops and Edge inference in a company deployment are:

1. **Location**: Local inference on laptops is typically performed on centralized servers, while Edge inference occurs at the edge of the network.
2. **Model Serving**: In local inference, models are often served from a centralized server or cloud service. In contrast, Edge inference involves serving models directly from edge devices, such as gateways or appliances.
3. **Model Access**: Local inference allows users to access models from multiple laptops connected to the same centralized server. Edge inference, on the other hand, enables models to be accessed only from end-users who are physically closer to the deployed edge devices.
4. **Latency and Speed**: Edge inference is generally faster than local inference due to the reduced latency and network hops between users and edge devices.
5. **Security and Control**: Deploying models at the edge provides more control over security, data processing, and maintenance, as well as greater flexibility in deploying specific workloads or use cases.
6. **Scalability**: Edge deployments can be more scalable than local deployments, allowing for easier addition of new users or workloads without affecting existing infrastructure.

In summary, while both approaches enable machine learning inference, Edge inference is specifically tailored to the needs of a company's edge computing deployment, providing faster access, better security and control, and greater scalability.
```

### Runtime

19.16 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

## P10: Failure Modes

### Prompt

```text
List five ways a local AI research assistant could give a bad answer when asked about a source text.
```

### Local Model Output

```text
Here are five ways a local AI research assistant could give a bad answer when asked about a source text:

1. **Misinterpretation of information**: The AI might misinterpret the context or nuances of the original source text, leading to an inaccurate summary or explanation.

Example: A user asks "What does the book 'The History of Art' by John Smith say about Michelangelo's Last Supper?" The AI responds with a simplistic summary that doesn't account for the complex historical and artistic context surrounding the painting.

2. **Incorrect citation**: The AI might incorrectly cite sources or authors, leading to confusion or misinformation.

Example: A user asks "What are some of the main ideas presented in Plato's 'The Republic'?" The AI responds with a list of topics that aren't actually covered in the book.

3. **Overemphasis on popular vs. scholarly perspectives**: The AI might prioritize popular or sensationalist views over more nuanced or scholarly interpretations, leading to an inaccurate understanding of the source text.

Example: A user asks "What does the author 'David Hume' say about morality?" The AI responds with a simplistic statement that doesn't account for Hume's complex and nuanced philosophical ideas on morality.

4. **Inaccurate information about authors or publications**: The AI might provide incorrect information about authors, publications, or historical events, leading to confusion or misinformation.

Example: A user asks "What was the title of 'The Great Gatsby' by F. Scott Fitzgerald?" The AI responds with a fictional book title, leading to confusion and frustration for the user.

5. **Failure to address counterarguments**: The AI might fail to consider counterarguments or opposing views in response to a source text question, leading to an incomplete or inaccurate understanding of the topic.

Example: A user asks "What are some arguments made by Thomas Hobbes regarding the role of government?" The AI responds with a simplistic summary that doesn't acknowledge or address Hobbes' criticisms of his own ideas.
```

### Runtime

16.28 seconds

### Notes

TODO

### Usefulness Score

TODO/5

---

