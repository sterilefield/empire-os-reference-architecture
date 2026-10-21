#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Dr. Ravi Teja Thiriveedhi
"""control_plane_sim: a toy model of three patterns from this reference architecture.

    python3 demo/control_plane_sim.py          # run all three
    python3 demo/control_plane_sim.py gate     # only the release gate
    python3 demo/control_plane_sim.py governor # only the memory governor
    python3 demo/control_plane_sim.py kill     # only the kill switch

1. Release gate (ADR-003): no tag unless every gate suite is green; the result is an evidence file.
2. Memory governor (ADR-001): each job has a memory budget; under pressure, non-urgent jobs wait.
3. Kill switch: one command freezes every agent; only the owner restores.

This is a teaching model written for this repository. It is not the engine or the governor, which
stay private; every suite, job and number below is invented. Standard library only.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------- 1. release gate


@dataclass
class Suite:
    name: str
    passed: int
    failed: int = 0

    @property
    def green(self) -> bool:
        return self.failed == 0 and self.passed > 0


def release_gate(version: str, previous: str, suites: list[Suite]) -> tuple[bool, str]:
    red = [s for s in suites if not s.green]
    ok = not red
    lines = [
        f"release: {version}",
        f"gate: {len(suites) - len(red)}/{len(suites)} suites green",
        f"tests: {sum(s.passed for s in suites)} passed, {sum(s.failed for s in suites)} failed",
        f"decision: {'SHIP' if ok else 'STOP'}" + ("" if ok else " (red: " + ", ".join(s.name for s in red) + ")"),
        f"rollback: keep {previous} running",
    ]
    return ok, "\n".join(lines)


DEMO_SUITES = [  # invented suite names and counts
    Suite("suite-a-unit", 120), Suite("suite-b-integration", 40), Suite("suite-c-policy", 21),
    Suite("suite-d-security", 9), Suite("suite-e-ui", 30), Suite("suite-f-recovery", 5),
]

# ---------------------------------------------------------------- 2. memory governor


@dataclass
class Job:
    name: str
    mb: int
    urgent: bool


@dataclass
class Governor:
    total_mb: int = 8192
    reserved_mb: int = 2048  # invented: operating system and an always-on service
    floor_mb: int = 1024     # below this much free memory, non-urgent work waits
    running: list[Job] = field(default_factory=list)
    deferred: list[Job] = field(default_factory=list)

    def free(self) -> int:
        return self.total_mb - self.reserved_mb - sum(j.mb for j in self.running)

    def submit(self, job: Job) -> str:
        after = self.free() - job.mb
        if job.urgent and after >= 0:
            self.running.append(job)
            return f"ACT    {job.name:<18}{job.mb:>5} MB urgent, runs now ({after} MB free)"
        if not job.urgent and after >= self.floor_mb:
            self.running.append(job)
            return f"ACT    {job.name:<18}{job.mb:>5} MB runs ({after} MB free)"
        self.deferred.append(job)
        why = "would breach the free-memory floor" if not job.urgent else "no room even for urgent work"
        return f"DEFER  {job.name:<18}{job.mb:>5} MB {why}; queued"

    def finish(self, name: str) -> list[str]:
        self.running = [j for j in self.running if j.name != name]
        out = [f"done   {name:<18}      memory released ({self.free()} MB free)"]
        for job in list(self.deferred):
            if self.free() - job.mb >= (0 if job.urgent else self.floor_mb):
                self.deferred.remove(job)
                self.running.append(job)
                out.append(f"ACT    {job.name:<18}{job.mb:>5} MB resumed from the queue ({self.free()} MB free)")
        return out


# ---------------------------------------------------------------- 3. kill switch


@dataclass
class Fleet:
    agents: dict[str, str] = field(default_factory=lambda: {f"agent-{i}": "running" for i in range(1, 10)})
    frozen: bool = False
    audit: list[str] = field(default_factory=list)

    def kill(self, by: str, reason: str) -> None:
        self.frozen = True
        self.agents = {a: "frozen" for a in self.agents}
        self.audit.append(f"kill by {by}: {reason}")

    def act(self, agent: str, action: str) -> str:
        if self.frozen:
            return f"STOPPED {agent} tried '{action}': refused, kill switch is on"
        return f"ACT     {agent} '{action}'"

    def restore(self, by: str, owner: str = "owner") -> str:
        if by != owner:
            self.audit.append(f"restore refused for {by}")
            return f"DENIED  restore by {by}: only the owner restores"
        self.frozen = False
        self.agents = {a: "running" for a in self.agents}
        self.audit.append(f"restore by {by}")
        return f"OK      restored by {by} after reading why it stopped"


# ---------------------------------------------------------------- demo


def demo_gate() -> None:
    print("1 · Release gate (invented suites)")
    ok, ev = release_gate("v0.9.0", "v0.8.2", DEMO_SUITES)
    print("   " + ev.replace("\n", "\n   "))
    broken = DEMO_SUITES[:-1] + [Suite("suite-f-recovery", 4, 1)]
    ok2, ev2 = release_gate("v0.9.1", "v0.9.0", broken)
    print("   ---")
    print("   " + ev2.replace("\n", "\n   "))


def demo_governor() -> None:
    print("2 · Memory governor on an 8 GB host (invented jobs)")
    g = Governor()
    for job in [Job("gateway-agents", 2600, True), Job("nightly-index", 1800, False), Job("report-builder", 900, False),
                Job("live-intake", 500, True), Job("backup-verify", 700, False)]:
        print("   " + g.submit(job))
    for line in g.finish("nightly-index"):
        print("   " + line)


def demo_kill() -> None:
    print("3 · Kill switch")
    f = Fleet()
    print("   " + f.act("agent-3", "write daily summary"))
    f.kill("owner", "unexpected loop in agent-3")
    print(f"   KILLED  all {len(f.agents)} agents frozen by the owner")
    print("   " + f.act("agent-7", "send status update"))
    print("   " + f.restore("agent-3"))
    print("   " + f.restore("owner"))
    print("   " + f.act("agent-7", "send status update"))
    print(f"   audit: {len(f.audit)} entries, append-only")


def main(argv: list[str]) -> int:
    print("Empire OS reference architecture: toy control plane (synthetic, not the real engine)")
    parts = argv[1:] or ["gate", "governor", "kill"]
    for p in parts:
        {"gate": demo_gate, "governor": demo_governor, "kill": demo_kill}[p]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
