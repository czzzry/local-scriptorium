# Ollama Installation Log

This file records the installation and first local inference smoke test for Local Scriptorium.

## Goal

Install Ollama on the current Mac and prove that a local language model can generate a response on this machine.

## Date

2026-05-17

## Tool

Local model runner: Ollama

## Installation Method

Method used:

- [ ] Official macOS app download
- [x] Terminal install script
- [ ] Other:


## Compatibility Check

The historical smoke test succeeded on a local macOS laptop. Exact machine and OS-build fingerprints have been removed from committed documentation; see `hardware_baseline.md` for the reproducibility policy.

## Commands Run

```bash
ollama --version
curl http://localhost:11434/api/tags
ollama run llama3.2:1b
ollama list
ollama ps
