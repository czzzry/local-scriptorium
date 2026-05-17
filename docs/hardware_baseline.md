# Hardware Baseline

This file records the machine used for the Local Scriptorium MVP.

The purpose is to make local inference results interpretable. If a local model is slow, unstable, or limited, those results should be understood in relation to the hardware used.

## Date Captured

2026-05-17

## Machine

Mac model: MacBook Pro
Model identifier: MacBookPro16,2
Processor / chip: Quad-Core Intel Core i7
Memory / RAM: 16 GB
macOS version: macOS 26.3.1
Available storage: 100 GB

## Why This Matters

Local inference runs the model on this machine rather than on a cloud server. That means performance depends on local hardware constraints such as:

- CPU / GPU capability
- available memory
- available storage
- operating system compatibility
- thermal limits
- model size

This baseline will help interpret later results from Ollama or other local model runners.

## Initial Local Inference Expectation

This machine will be used for the MVP local inference smoke test.

The MVP does not require excellent model quality or production-level performance. The immediate goal is to prove that a local model can run, generate responses, and support the source → chunk → retrieve → answer → evaluate learning loop.
