# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Dr. Ravi Teja Thiriveedhi
"""Tests for demo/control_plane_sim.py (standard library unittest)."""
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "demo"))
import control_plane_sim as cp  # noqa: E402


class Gate(unittest.TestCase):
    def test_all_green_ships(self):
        ok, ev = cp.release_gate("v1", "v0", cp.DEMO_SUITES)
        self.assertTrue(ok)
        self.assertIn("decision: SHIP", ev)

    def test_one_red_suite_stops(self):
        ok, ev = cp.release_gate("v1", "v0", cp.DEMO_SUITES + [cp.Suite("x", 3, 1)])
        self.assertFalse(ok)
        self.assertIn("STOP (red: x)", ev)

    def test_empty_suite_is_not_green(self):
        self.assertFalse(cp.Suite("empty", 0).green)


class GovernorTest(unittest.TestCase):
    def test_non_urgent_respects_floor_and_urgent_runs(self):
        g = cp.Governor()
        g.submit(cp.Job("big", 4500, True))
        self.assertTrue(g.submit(cp.Job("batch", 1000, False)).startswith("DEFER"))
        self.assertTrue(g.submit(cp.Job("live", 500, True)).startswith("ACT"))
        self.assertGreaterEqual(g.free(), 0)

    def test_deferred_resume_after_release(self):
        g = cp.Governor()
        g.submit(cp.Job("big", 4500, True))
        g.submit(cp.Job("batch", 1000, False))
        g.finish("big")
        self.assertEqual([j.name for j in g.running], ["batch"])
        self.assertEqual(g.deferred, [])


class KillSwitch(unittest.TestCase):
    def test_only_owner_restores(self):
        f = cp.Fleet()
        f.kill("owner", "test")
        self.assertTrue(f.act("agent-1", "x").startswith("STOPPED"))
        self.assertTrue(f.restore("agent-1").startswith("DENIED"))
        self.assertTrue(f.frozen)
        f.restore("owner")
        self.assertFalse(f.frozen)


class Cli(unittest.TestCase):
    def test_runs_and_is_labelled(self):
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cp.main(["x"]), 0)
        self.assertIn("synthetic, not the real engine", out.getvalue())


if __name__ == "__main__":
    unittest.main()
