# ADR-002: The control plane observes client systems but never writes to them

- **Status:** accepted
- **Date:** 2026-10

## Context
Client platforms hold client data and serve the client's customers. A shared control plane with write access would put every client inside one blast radius and complicate data-protection duties.

## Decision
Client systems run on their own nodes with their own stores. The control plane may read health and metrics through one-way observation. Changes reach a client only through that client's own release process.

## Consequences
- Easier: data stays where it belongs (DPDP); a control-plane fault cannot corrupt a client.
- Harder: fixes need a per-client release; cross-client automation is limited by design.
- Watch: any request for a write path is an architecture change and needs a new ADR.
