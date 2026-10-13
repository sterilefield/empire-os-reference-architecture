# Governance model

Agents are useful only if you can trust what they do unattended. This model makes trust explicit and checkable.

## Autonomy levels

| Level | Name | What it means |
|---|---|---|
| L0 | Observer | Reads and reports only |
| L1 | Proposer | Proposes; a human decides and acts |
| L2 | Operator | Acts on routine, reversible work |
| L3 | Delegate | Acts on delegated work within its remit |
| L4 | Autonomous | **Deliberately unused** |

Health, money, external sends, deletions and secrets are never handled above L3.

## Risk classes

| Class | Covers | Who approves |
|---|---|---|
| R0 | Read | None needed |
| R1 | Workspace write | None needed; logged |
| R2 | Reversible operations | Logged; reversible by design |
| R3 | Configuration changes | Orchestrator review plus the owner |
| R4 | External sends, money, clinical, deletion or secrets | The owner, every time |

## Human-in-the-loop tiers

| Tier | Applies to |
|---|---|
| Hard stop | Anything involving spend, external messages, irreversible actions or security |
| Soft stop | Lower-risk actions, with a 3-minute window to object |
| Silent proceed | Routine work |

An action runs only when its agent's autonomy level allows it **and** its risk class's approval is satisfied.

## Controls

- **Kill switches** — stop one agent or all agents by command or from the dashboard; restore is a deliberate owner action; problem agents are quarantined, never deleted.
- **Append-only audit log** — every agent action is recorded with OpenTelemetry GenAI fields, kept for at least a year and backed up encrypted off-site.
- **Promotion gate** — an agent moves up a level only after at least 30 days and 20 actions with zero critical incidents, an evaluation suite that includes prompt-injection tests, and an owner decision. Any R3 or R4 incident demotes it automatically.
- **Prompt-injection defence** — agent output is treated as data, never as instructions; known injection patterns trigger an immediate stop.
- **Budgets** — agents are designed to run within token, time and memory budgets; overruns are deferred or stopped rather than silently extended.
- **Separation of duties** — the agent that writes code is not the one that reviews it, and neither can tag a release.

## Standards mapping

| Standard | Where it shows up |
|---|---|
| OWASP Top 10 for Agentic Applications | Tool-permission limits, approval tiers, memory isolation, audit |
| NIST AI RMF (Govern · Map · Measure · Manage) | Risk classes, telemetry, release gates, incident drills |
| ISO/IEC 42001 | Documented roles, change control, records |
| India DPDP Act 2023 | Client data stays on client nodes; consent-first patterns; no clinical advice by agents |

This mapping shows design intent; it is not a certification.
