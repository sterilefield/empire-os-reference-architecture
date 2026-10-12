# Governance model

Agents are useful only if you can trust what they do unattended. This model makes trust explicit and checkable.

## Autonomy levels

| Level | Name | The agent may | Example |
|---|---|---|---|
| L0 | Observe | Read and report only | Health check summary |
| L1 | Suggest | Draft; a human executes | Drafted reply for review |
| L2 | Act with approval | Execute after an explicit human yes | Send an outreach message |
| L3 | Act and report | Execute, then report immediately | Restart a stuck job |
| L4 | Act silently within budget | Execute routine work inside a written budget | Rotate logs, defer a batch job |

## Risk classes

| Class | Meaning | Approval needed |
|---|---|---|
| R0 | No external effect, reversible | None |
| R1 | Internal effect, reversible | None; logged |
| R2 | External effect, reversible | Owner approval, single |
| R3 | External effect, hard to reverse (money, public posts, deletions) | Owner approval per action |
| R4 | Irreversible or regulated (clinical, legal, credentials) | Not delegated to agents |

An action runs only when its agent's autonomy level allows it **and** its risk class's approval is satisfied.

## Controls

- **Kill switch** — one command freezes agent processes; resuming is a deliberate owner action.
- **Append-only audit log** — approvals, changes and releases are recorded and never edited in place.
- **Budgets** — every agent has token, time and memory budgets; overruns are deferred or stopped, never silently extended.
- **Separation of duties** — the agent that writes code is not the one that reviews it, and neither can tag a release.

## Standards mapping

| Standard | Where it shows up |
|---|---|
| OWASP Top 10 for Agentic Applications | Tool-permission limits, approval tiers, memory isolation, audit |
| NIST AI RMF (Govern · Map · Measure · Manage) | Risk classes, telemetry, release gates, incident drills |
| ISO/IEC 42001 | Documented roles, change control, records |
| India DPDP Act 2023 | Client data stays on client nodes; consent-first patterns; no clinical advice by agents |

This mapping shows design intent; it is not a certification.
