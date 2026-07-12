# Hardware Context for Historical Local Inference

The v0.1 Ollama experiments ran on a consumer laptop rather than dedicated inference hardware. Exact model identifiers, OS build numbers, storage figures, and other machine fingerprints are intentionally not committed.

## Why hardware context matters

Local inference performance depends on CPU/GPU capability, memory, storage, thermals, model size, quantization, and runner version. A reproducible performance study should capture those values in private run metadata or an ignored generated artifact, then publish only the minimum aggregate hardware class needed to interpret results.

The v0.2 deterministic retrieval benchmark does not use Ollama and makes no performance claim based on the historical machine. Runtime metadata for each new evaluation run is generated locally under `outputs/generated/` and is ignored by Git.
