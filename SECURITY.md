# Security Policy

Local Scriptorium processes local text. Treat private corpora, prompts, generated answers, and embedding caches as sensitive. Keep them under ignored paths (`sources_private/` or `outputs/generated/`) and never add secrets to manifests or command history.

Report a vulnerability privately to the repository owner rather than opening a public issue containing exploit details or sensitive data. This research harness has no network service in its default configuration. Optional Ollama use inherits the security posture of the local Ollama installation and is outside the offline CI boundary.
