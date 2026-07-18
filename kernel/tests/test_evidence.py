"""Four-quadrant tests for evidence.py: {UVM, plain-VCS} x {PASS, FAIL},
plus backfill behavior and the spec_ref header."""
import shutil
import tempfile
import unittest
from pathlib import Path

from fixture import (PLAIN_FAIL_LOG, PLAIN_PASS_LOG, UVM_FAIL_LOG,
                     UVM_PASS_LOG, make_project, run)


class EvidenceBase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="iverif_ev_"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        make_project(self.tmp)
        self.out = self.tmp / "sim" / "out"
        self.out.mkdir(parents=True)

    def write_log(self, content, test="fixture_test", seed="1"):
        p = self.out / ("%s_%s.log" % (test, seed))
        p.write_text(content, encoding="utf-8")
        return p

    def evidence(self, *args):
        return run(self.tmp, "evidence.py", *args)


class TestFourQuadrants(EvidenceBase):
    def test_uvm_pass_registers_and_backfills(self):
        self.write_log(UVM_PASS_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        ev = self.tmp / "doc" / "evidence" / "v0.1.0" / "M1-01.log"
        self.assertTrue(ev.exists())
        first = ev.read_text(encoding="utf-8").splitlines()[0]
        self.assertEqual(first, "make run TEST=fixture_test SEED=1")
        tp = (self.tmp / "doc" / "testplan.md").read_text(encoding="utf-8")
        self.assertIn("✅", tp)
        self.assertIn("doc/evidence/v0.1.0/M1-01.log", tp)
        # evidence.py chains into docs-check, which must have passed
        self.assertIn("docs-check passed", cp.stdout)

    def test_uvm_fail_rejected(self):
        self.write_log(UVM_FAIL_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("FAIL logs are never evidence", cp.stderr + cp.stdout)
        self.assertFalse(
            (self.tmp / "doc" / "evidence" / "v0.1.0" / "M1-01.log").exists())

    def test_plain_pass_registers(self):
        self.write_log(PLAIN_PASS_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        ev = self.tmp / "doc" / "evidence" / "v0.1.0" / "M1-01.log"
        self.assertIn("V C S   S i m u l a t i o n",
                      ev.read_text(encoding="utf-8"))

    def test_plain_fail_rejected(self):
        self.write_log(PLAIN_FAIL_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)

    def test_gibberish_log_rejected(self):
        self.write_log("neither uvm nor vcs\n")
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("cannot judge", cp.stderr + cp.stdout)

    def test_missing_log_rejected(self):
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("no log, no evidence", cp.stderr + cp.stdout)


class TestBackfillDetails(EvidenceBase):
    def test_spec_ref_header(self):
        self.write_log(UVM_PASS_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1", "--spec-ref", "SPEC-1.1")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        ev = self.tmp / "doc" / "evidence" / "v0.1.0" / "M1-01.log"
        self.assertIn("# spec_ref: SPEC-1.1",
                      ev.read_text(encoding="utf-8").splitlines()[2])

    def test_bug_closure_backfill(self):
        from fixture import EN, _table
        (self.tmp / "doc" / "bugs.md").write_text(
            "# Bugs\n\n" + _table(EN["bug_header"], [
                "| BUG-001 | VERIFYING | TB | mismatch | TEST=fixture_test "
                "SEED=1 | bad expect | abc123 | - |"]), encoding="utf-8")
        self.write_log(UVM_PASS_LOG)
        cp = self.evidence("--bug", "BUG-001", "--test", "fixture_test",
                           "--seed", "1")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        bugs = (self.tmp / "doc" / "bugs.md").read_text(encoding="utf-8")
        self.assertIn("CLOSED", bugs)
        self.assertIn("doc/evidence/v0.1.0/BUG-001.log", bugs)
        self.assertIn("closer ≠ fixer", cp.stdout)

    def test_unknown_scenario_id_rejected(self):
        self.write_log(UVM_PASS_LOG)
        cp = self.evidence("--scen", "M9-99", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("no row with id", cp.stderr + cp.stdout)


if __name__ == "__main__":
    unittest.main()
