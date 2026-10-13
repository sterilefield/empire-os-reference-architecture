# Release process

## Flow

1. **Task card.** Goal, acceptance criteria, guard rules (allowed files, forbidden commands), and the tests that prove it.
2. **Build.** An AI coding agent implements the card on a branch in the builder lane.
3. **Independent review.** A separate reviewer (a different agent or an adversarial pass) looks for logic errors, race conditions and cost escalations.
4. **Release gate.** Every gate suite must pass — 99 of 99 at v1.3.0. One red suite stops the release.
5. **Tag and evidence.** A tagged release plus an evidence file: what changed, which suites ran, results, and how to roll back.

## Why it works on small hardware

- The gate runs on the seat, not the control plane, so testing does not compete with production for memory.
- Releases are small; eight releases in seven days kept each change reviewable.
- Rollback is "keep the previous tag running", which needs no extra infrastructure.

## Evidence file (shape)

```text
release: v1.3.0
date: <release date>
changes: <summary of the task cards included>
gate: 99/99 suites green
tests: <counts per suite>
rollback: previous tag v1.2.1, no data migration
```
