# ADR-003: No tag without every gate suite green

- **Status:** accepted
- **Date:** 2026-10

## Context
Most code is written by AI coding agents. Speed is high; so is the chance of confident mistakes. Review alone does not scale with agent output.

## Decision
A release tag can be cut only when every gate suite passes (99 of 99 at v1.3.0). Builders cannot tag. A red suite sends the work back to the task card.

## Consequences
- Easier: eight releases in seven days, each one small and reviewable; rollback is "keep the previous tag".
- Harder: gate suites must be maintained as the system grows.
- Watch: gate run time; flaky suites are fixed or removed, never ignored.
