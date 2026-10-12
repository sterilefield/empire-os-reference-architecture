# Release process

## Flow

1. **Task card.** Goal, acceptance criteria, guard rules (allowed files, forbidden commands), and the tests that prove it.
2. **Build.** An AI coding agent implements the card on a branch in the builder lane.
3. **Independent review.** A separate reviewer (a different agent or an adversarial pass) looks for logic errors, race conditions and cost escalations.
4. **Release gate.** Every gate suite must pass — 87 of 87 at v1.2.1. One red suite stops the release.
5. **Tag and evidence.** A tagged release plus an evidence file: what changed, which suites ran, results, and how to roll back.

## Why it works on small hardware

- The gate runs on the seat, not the control plane, so production memory is never spent on testing.
- Releases are small; seven releases in three days kept each change reviewable.
- Rollback is "keep the previous tag running", which needs no extra infrastructure.

## Evidence file (shape)

```text
release: v1.2.1
date: <release date>
changes: <summary of the task cards included>
gate: 87/87 suites green
tests: <counts per suite>
rollback: previous tag v1.2.0, no data migration
```
