# Empire OS — reference architecture

**How one person runs 9 governed AI agents on a 2012 Mac mini with 8 GB of RAM — and ships test-gated releases: eight in seven days, v1.0.0 → v1.3.0.**

This repository documents the *architecture* of Empire OS, a self-hosted multi-agent AI operating system in daily production use. It is a reference, not the engine: it explains the tiers, the governance model, the release process and the trade-offs, so you can apply the patterns to your own system. No engine code, agent prompts, configurations, client data or credentials are published here.

> [!IMPORTANT]
> **Status:** Sanitised reference architecture of a multi-agent system in daily production use. Last verified 21 Oct 2026. Not for clinical use as-is. Scope and limits: [TRUST.md](TRUST.md).

**[Architecture](docs/architecture.md) · [Governance](docs/governance.md) · [Release process](docs/release-process.md) · [ADRs](docs/adr/) · [Trust](TRUST.md) · [All showcases](https://github.com/sterilefield) · [Contact](https://www.linkedin.com/in/dr-ravi-teja-thiriveedhi)**

[![CI](https://github.com/sterilefield/empire-os-reference-architecture/actions/workflows/ci.yml/badge.svg)](https://github.com/sterilefield/empire-os-reference-architecture/actions/workflows/ci.yml) [![Live demo](https://img.shields.io/badge/live_demo-open-1a7f37)](https://sterilefield.github.io/empire-os-reference-architecture/) [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sterilefield/empire-os-reference-architecture) [![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/sterilefield/empire-os-reference-architecture/badge)](https://scorecard.dev/viewer/?uri=github.com/sterilefield/empire-os-reference-architecture)

## At a glance

| Measure | Value | Evidence |
|---|---|---|
| Governed agents in production | 9 | live fleet, release notes |
| Commits (Oct 2026) | 626 | private repository history |
| Releases | 8 in 7 days (v1.0.0 → v1.3.0, 13 Oct 2026) | tagged releases |
| Release-gate suites | 99 / 99 passed at v1.3.0 (gate grew from 48 suites) | promotion report |
| Automated tests | 1,026 passing, 0 failing (v1.3.0) | test run |
| Pre-release browser sweep | 116 pages, no priority-1 defects | sweep report |
| Control-plane host | 2012 Mac mini, 8 GB RAM | — |
| Heartbeat tokens | 12.0 M → 1.0 M a day (−91%) | token telemetry |
| Disaster-recovery rebuild | 127 GB SHA-verified capsule, zero data loss | DR drill record |

## The five tiers

```mermaid
flowchart LR
    subgraph T1["Tier 1 · Seat — MacBook M3"]
        P["Planner"] --> B["AI builders<br/>under guard rules"]
    end
    subgraph T2["Tier 2 · Control plane — Mac mini 8 GB"]
        G["Gateway<br/>9 governed agents"] --- GOV["Governor · kill switch<br/>approvals · audit log"]
        G --- OBS["Telemetry · alerts<br/>backups · DR drills"]
    end
    subgraph T3["Tier 3 · Compute (planned)"]
        R["Workstation<br/>not yet onboarded"]
    end
    subgraph T4["Tier 4 · Client edge"]
        C["Client platforms<br/>isolated per client"]
    end
    subgraph T5["Tier 5 · Free cloud"]
        F["Git hosting · encrypted backup<br/>Tailscale tailnet · messaging"]
    end
    B -- "test-gated releases" --> G
    G -- "one-way observation" --> C
    G -.-> R
    G --> F
```

| Tier | Role | Key constraint |
|---|---|---|
| 1 · Seat | Where plans and code are written. AI builders work only from task cards with acceptance criteria. | Builders never touch production directly. |
| 2 · Control plane | Runs the agent gateway, the RAM governor, the kill switch, approvals, telemetry and backups. | 8 GB RAM: every process has a written budget. |
| 3 · Compute | Heavier jobs, when onboarded. | Planned; not yet in service. |
| 4 · Client edge | Each client system runs on its own node. | The control plane observes; it never writes into client systems. |
| 5 · Free cloud | Git hosting, encrypted off-site backup, private network, notifications. | Free tiers only; no single provider is load-bearing. |

Full detail: [docs/architecture.md](docs/architecture.md).

## Governance in one table

| Control | What it does |
|---|---|
| Autonomy levels L0–L4 | Agents run from L0 Observer to L3 Delegate; L4 Autonomous is deliberately unused. |
| Risk classes R0–R4 | From R0 read-only to R4 external sends, money, clinical, deletion or secrets, which need the owner every time. |
| Kill switch | Freezes agent processes from a messaging command or the CLI. |
| Append-only audit log | Records every approval, change and release. |
| RAM governor | Defers non-urgent work under memory pressure (about 12 deferrals a week, no crashes). |
| Standards mapped | OWASP Top 10 for Agentic Applications, NIST AI RMF, ISO/IEC 42001, India DPDP Act 2023. |

Full model: [docs/governance.md](docs/governance.md).

## How releases happen

```mermaid
flowchart LR
    S["Spec + task card<br/>acceptance criteria"] --> A["AI builder<br/>under guard rules"]
    A --> R["Independent review"]
    R --> T{"Release gate<br/>all suites green?"}
    T -- yes --> SHIP["Tagged release<br/>+ evidence file"]
    T -- no --> S
```

Details: [docs/release-process.md](docs/release-process.md).

## Decisions

Architecture decisions are recorded as ADRs in [docs/adr/](docs/adr/):

- [ADR-001](docs/adr/ADR-001-constrained-control-plane.md) — run the control plane on an 8 GB machine, on purpose
- [ADR-002](docs/adr/ADR-002-one-way-observation.md) — the control plane observes client systems but never writes to them
- [ADR-003](docs/adr/ADR-003-test-gated-releases.md) — no tag without every gate suite green

## What is deliberately not here

The engine, the governor's implementation, agent prompts and configurations, internal dashboards, and every client or clinical module stay private. This repository is released through the five-gate [Sterile Field](https://github.com/sterilefield) release check: allow-list, secret and deny-list scan, fresh history, independent review, owner gate.

## Try it

**[Control plane playground](https://sterilefield.github.io/empire-os-reference-architecture/)**: a release gate that ships only when every suite is green, a memory governor on an 8 GB host and an owner-only kill switch. It runs in your browser on invented data.

<a href="https://sterilefield.github.io/empire-os-reference-architecture/"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/img/demo-page-dark.png">
  <img alt="Screenshot of the Control plane playground demo page, showing invented data" src="docs/img/demo-page-light.png" width="100%">
</picture></a>

Or run the same logic yourself (Python 3, standard library only, nothing to install):

```bash
git clone https://github.com/sterilefield/empire-os-reference-architecture.git
cd empire-os-reference-architecture
python3 demo/control_plane_sim.py
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/img/demo-terminal-dark.svg">
  <img alt="Terminal recording of python3 demo/control_plane_sim.py: the real output of the demo" src="docs/img/demo-terminal-light.svg" width="100%">
</picture>

The terminal image is the real output of that command, rendered by `scripts/term_svg.py`. Everything in `demo/` and `site/` is a toy written for this repository on invented data. It is not production code, and the tests in `tests/` run on every pull request.

## How this was built

I write the specifications, architecture, acceptance criteria and review gates; AI coding agents (Claude Code and Codex) write most of the code under those specifications. I own every review, test gate, release decision and production operation. Text in this repository was drafted with AI assistance and passed gate G4, a review by a fresh-context AI agent that did not write it, before my own approval (G5).

## Verify this release

Every release carries a build-provenance attestation for its source archive and an SPDX SBOM.

```bash
gh release download v0.1.0 -R sterilefield/empire-os-reference-architecture -p 'empire-os-reference-architecture-v0.1.0.tar.gz'
gh attestation verify empire-os-reference-architecture-v0.1.0.tar.gz -R sterilefield/empire-os-reference-architecture
```

## Author

**Dr. Ravi Teja Thiriveedhi** — clinician turned AI systems architect; 20 years of clinical practice and hospital operations. [GitHub](https://github.com/Raviteja2k2k) · [LinkedIn](https://www.linkedin.com/in/dr-ravi-teja-thiriveedhi)

## Licence

Documentation in this repository is licensed under [CC BY-NC-ND 4.0](LICENSE): share it with credit, no commercial use, no derivatives.
