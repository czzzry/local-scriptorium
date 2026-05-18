# Local Model Hello World

## Goal

Run a small local LLM and produce the first local answer.

## Date

2026-05-18

## Model

Model: llama3.2:1b

## Commands Used

Model pull command:

ollama pull llama3.2:1b

Model run command:

ollama run llama3.2:1b "In this project, local inference means running a language model on my own Mac instead of sending the prompt to a cloud API. Explain that in 5 bullet points."

## Prompt

In this project, local inference means running a language model on my own Mac instead of sending the prompt to a cloud API. Explain that in 5 bullet points.

## Output

Here are five bullet points explaining local inference for your project:

• **Improved Security**: By running the language model on your own Mac instead of sending it to a cloud API, you can 
ensure that sensitive data is not being transmitted over the internet, reducing the risk of data breaches or 
hacking.

• **Reduced Latency**: Local inference typically means executing tasks locally without relying on external 
services, which can result in faster processing times and better responsiveness for your application. This 
is particularly important if your application needs to respond quickly to user input or perform complex 
calculations.

• **Increased Control**: By running the language model on your own Mac, you have complete control over its 
settings, allowing you to tailor it to your specific use case and preferences. You can also choose not to 
share sensitive data or logs with anyone else, maintaining confidentiality and data ownership.

• **Faster Development and Testing**: Local inference enables you to test and iterate on your language 
model development without relying on cloud services. This speedier feedback loop allows for faster 
testing, debugging, and refinement of your model, ensuring that it meets your project's requirements.

• **Data Ownership and Flexibility**: By running the language model locally, you can choose how and where 
it is stored, making it easier to manage data ownership and compliance with relevant regulations. You can 
also decide whether to use local data for training or testing purposes, giving you more flexibility in 
your development workflow.



## Notes

This is the first local model output generated for Local Scriptorium.

The goal of this ticket is not to evaluate model quality. The goal is to prove that a small local LLM can be pulled, run, and used to generate an answer on this Mac.

## Acceptance Criteria

- [x] Model pulled
- [x] Prompt returns output
- [x] Model name and command saved
- [x] Output artifact created