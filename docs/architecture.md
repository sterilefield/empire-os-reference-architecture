# Architecture

## Design goals

1. **Run on what you already own.** The control plane is a 2012 Mac mini with 8 GB of RAM. Constraints are a feature: they force budgets, back-pressure and simple components.
2. **Humans decide, agents do.** Every consequential action passes through an autonomy level, a risk class and, above a threshold, a human approval.
3. **Nothing ships untested.** The only way into production is a tagged release that passed every gate suite.
4. **Leave cleanly.** Every component can be rebuilt from a verified backup capsule; no free-tier provider is load-bearing on its own.

## Tiers

### Tier 1 — Seat (MacBook M3)
- The owner plans; AI coding agents build from task cards that state the goal, the acceptance criteria and guard rules (files they may touch, commands they may not run).
- Builders work in a separate lane with fixed hours and turn budgets, and cannot force-push.
- Output is a branch plus an evidence file, never a change to production.

### Tier 2 — Control plane (Mac mini, 8 GB)
- **Gateway:** routes work to 9 governed agents (orchestration, research, engineering lead, job pipeline, education planning, monetisation, communications, site reliability triage, records and audit).
- **Governor:** a RAM budget per process; non-urgent jobs are deferred under pressure instead of risking the host.
- **Kill switch:** freezes agent processes on command.
- **Approvals:** risky actions wait for a human, by tier.
- **Telemetry:** health checks, alerts, token usage; backups and disaster-recovery drills.

### Tier 3 — Compute (planned)
A workstation for heavier jobs. Not yet onboarded; the architecture reserves the slot so that adding it changes routing, not design.

### Tier 4 — Client edge
Client systems run on their own nodes with their own data stores. The control plane may **observe** them (health, metrics) but has no write path into them. See ADR-002.

### Tier 5 — Free cloud
Git hosting for code and releases, encrypted off-site backups, a private Tailscale tailnet between machines (public ingress only for a webhook and an MCP connector), and a messaging channel for alerts and the kill switch.

## Data flow rules

| Rule | Why |
|---|---|
| Client data never leaves the client node | Privacy (DPDP), blast radius |
| One writer per data store | Removes concurrency bugs on small hardware |
| Secrets live in the OS keychain or a secret reference, never in files | Leaks via git or logs become impossible by construction |
| Backups are encrypted before they leave the machine | Free cloud storage is treated as untrusted |

## Failure modes designed for

| Failure | Response |
|---|---|
| Memory pressure | Governor defers non-urgent work; urgent paths keep a reserved budget |
| Runaway agent | Kill switch; approval tiers stop high-risk actions before they run |
| Bad release | Gate blocks the tag; previous release stays live |
| Host loss | Rebuild from the latest SHA-verified capsule (127 GB drill, zero data loss) |
| Provider outage | Each free-cloud role has a documented alternative |
