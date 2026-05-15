# Decision Log

This file records important project decisions for Local Scriptorium.

The goal is not to document every small action. The goal is to preserve the reasoning behind decisions that affect scope, tooling, architecture, privacy, or delivery.

---

## Decision 001: Use Jira Scrum-lite

Date: 2026-05-15

Context:
I want to manage Local Scriptorium like a small company project, with a backlog, estimates, roadmap, and weekly execution.

Options considered:
- Kanban board
- Scrum board with one-week sprints
- Simple spreadsheet
- Notion/Linear-style lightweight planning

Decision:
Use Jira Scrum-lite with one-week sprints.

Reason:
Jira gives me a structured way to manage tickets, estimates, sprint planning, and roadmap-style work. This is also useful professional practice for PM/TPM workflows.

Consequences:
Jira maintenance must stay lightweight. The project should not become fake PM theater. Jira is for tracking execution, not replacing actual building.

Review later?
Yes. If Jira becomes too heavy, consider Linear or a simpler tool.

---

## Decision 002: Use a public GitHub repo with private sources excluded

Date: 2026-05-15

Context:
I want the project to be visible as a portfolio artifact for job applications, but the project may involve private notes, copyrighted books, or unclear-rights source material.

Options considered:
- Private GitHub repo
- Public GitHub repo with all files
- Public GitHub repo with strict source controls

Decision:
Use a public GitHub repo, but keep private/copyrighted/unclear-rights sources out of Git.

Reason:
A public repo makes the project easier to show in applications and interviews. However, the repo should only contain code, documentation, public-domain/openly licensed sources, project-authored sample material, and safe outputs.

Consequences:
The project will use `sources_public/` for safe public sources and `sources_private/` for local-only material. `sources_private/` is ignored by Git.

Review later?
Yes, before adding any real source texts or generated outputs.

---

## Decision 003: Use the current Mac for MVP

Date: 2026-05-15

Context:
I considered using an older MacBook Air as a separate local inference machine, but the MVP should stay simple and avoid hardware/setup distractions.

Options considered:
- Current Mac only
- Old MacBook Air as remote test box
- Buy new hardware
- Cloud-only implementation

Decision:
Use the current Mac only for MVP.

Reason:
The project goal is to learn the local inference/RAG implementation loop, not to manage multiple machines. Using the current Mac keeps the setup simple and reduces distractions.

Consequences:
The MVP will demonstrate single-device local inference, not true distributed edge deployment. Hardware limitations will be documented as part of the learning.

Review later?
Yes. MVP+1 may test QVAC, another device, or more realistic edge/delegated inference.

---

## Decision 004: Use Ollama or a simple local model runner before QVAC

Date: 2026-05-15

Context:
QVAC is relevant to the Tether/local-first AI angle, but it may create setup complexity before the core MVP is working.

Options considered:
- Ollama/simple local model runner first
- QVAC first
- llama.cpp directly
- Cloud API only

Decision:
Use the simplest reliable local inference stack first, likely Ollama. Treat QVAC as an MVP+1 spike or comparison after the core local RAG loop works.

Reason:
The MVP goal is to understand and demonstrate the source → chunk → retrieve → answer → evaluate loop. Tooling complexity should not block the learning.

Consequences:
The MVP will not depend on QVAC. QVAC remains important but will be tested after the basic local Scriptorium works.

Review later?
Yes, after the MVP can generate grounded answers from retrieved chunks.