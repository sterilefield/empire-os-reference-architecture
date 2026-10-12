# ADR-001: Run the control plane on an 8 GB machine, on purpose

- **Status:** accepted
- **Date:** 2026-10

## Context
The control plane hosts the agent gateway, governor, approvals, telemetry and backups. The available always-on machine is a 2012 Mac mini with 8 GB of RAM. Buying new hardware or renting cloud servers adds recurring cost and a new dependency.

## Decision
Keep the control plane on the 8 GB machine and design for it: written RAM budgets per process, a governor that defers non-urgent work under pressure, and heavy work moved to the seat or a future compute tier.

## Consequences
- Easier: near-zero running cost; every process has a known budget; overload behaviour is designed, not accidental.
- Harder: some jobs wait; heavy local models cannot run here.
- Watch: governor deferrals per week (currently about 12, with no crashes).
