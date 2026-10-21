# Trust, scope and limitations

> [!WARNING]
> Sanitised public showcase. Not for clinical use as-is, not legal or regulatory advice, and not a product. Last verified 21 Oct 2026.

## What this repository is
Documentation (architecture, decisions, process). A reference for architects and engineering leads who run AI agents on constrained hardware and want governed, test-gated releases.

## Out of scope
It is not the engine, not installable software and not a product. It contains no code that runs agents; `demo/` and `site/` are small teaching toys written for publication, on invented data.

## Limitations
- Figures describe one owner-operated system on one host; they are not benchmarks and may not transfer.
- The engine, governor, prompts and configurations are private, so the patterns here are described, not executable.
- Counts come from the private repository, release notes and telemetry at the dates stated; they are refreshed only at a showcase release.

## Data provenance
No client data, patient data, prompts, configurations or credentials. Numbers come from the author's own release notes, test runs and token telemetry. Every release passes five gates before it is public: G1 allow-list of files, G2 secret and deny-list scan, G3 fresh history (no private commits travel), G4 fresh-context AI review (an agent that did not write the material), G5 owner approval (the human check) with a licence check. See the [publication policy](https://github.com/sterilefield/.github/blob/main/PUBLICATION_POLICY.md).

## Privacy and regulation
No personal data is processed by anything in this repository. Where the text discusses India's DPDP Act and Rules, systems are described as *designed toward* those requirements, never as certified or compliant.

## AI assistance
AI coding agents (Claude Code and Codex) drafted much of the material under the author's specifications; the author reviewed every change and owns every claim.

## Report a problem
Security issues: see [SECURITY.md](SECURITY.md). Factual errors or overclaims: open an issue; corrections are welcome.
