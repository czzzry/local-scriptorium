# Security Policy

Local Scriptorium processes local text. Treat private corpora, prompts, generated answers, and embedding caches as sensitive. Keep them under ignored paths (`sources_private/` or `outputs/generated/`) and never add secrets to manifests or command history.

## Supported Version

This is a portfolio prototype. Security fixes are applied to the latest commit on `main`; older commits and releases are not supported.

## Reporting A Vulnerability

Please use GitHub's private **Report a vulnerability** flow in the repository's Security tab. Do not open a public issue containing credentials, personal data, exploit details, or private user content.

Include:

- the affected file, endpoint, or workflow;
- steps to reproduce;
- the impact you observed;
- whether any secret or personal data may have been exposed; and
- a safe way to confirm the fix.

This research harness has no network service in its default configuration. Optional Ollama use inherits the security posture of the local Ollama installation and is outside the offline CI boundary. Do not test against live user data or third-party accounts without explicit authorization.
