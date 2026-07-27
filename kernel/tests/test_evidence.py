"""Four-quadrant tests for evidence.py: {UVM, plain-VCS} x {PASS, FAIL},
plus backfill behavior, the spec_ref header, and the SVA leg (assertion
failures never increment UVM_ERROR — they need their own judgment)."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from fixture import (PLAIN_FAIL_LOG, PLAIN_PASS_LOG, UVM_FAIL_LOG,
                     UVM_NOSVA_LOG, UVM_PASS_LOG, UVM_SVA_FAIL_LOG,
                     make_project, run)


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


class TestSvaLeg(EvidenceBase):
    """The BUG-014 fuse: `UVM_ERROR : 0` proves nothing about assertions."""

    def test_sva_failure_rejected_despite_clean_uvm(self):
        self.write_log(UVM_SVA_FAIL_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        out = cp.stderr + cp.stdout
        self.assertIn("SVA failures", out)
        self.assertIn("a_done_hold", out)  # detail names the assertion
        self.assertFalse(
            (self.tmp / "doc" / "evidence" / "v0.1.0" / "M1-01.log").exists())

    def test_missing_native_summary_rejected_by_default(self):
        self.write_log(UVM_NOSVA_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("-assert verbose", cp.stderr + cp.stdout)

    def test_missing_summary_tolerated_when_enforce_off(self):
        # Legacy flows predating -assert verbose set "sva_enforce": false.
        cfg_path = self.tmp / "iverif.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["sva_enforce"] = False
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        self.write_log(UVM_NOSVA_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        ev = self.tmp / "doc" / "evidence" / "v0.1.0" / "M1-01.log"
        self.assertIn("sva_enforce off", ev.read_text(encoding="utf-8"))

    def test_enforce_off_still_rejects_visible_sva_failure(self):
        # enforce=false relaxes only the missing-summary case; a detected
        # engine failure line stays fatal.
        cfg_path = self.tmp / "iverif.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["sva_enforce"] = False
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        self.write_log(UVM_SVA_FAIL_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("SVA failures", cp.stderr + cp.stdout)

    def test_baseline_floor_violation_rejected(self):
        # $assertoff / dropped-sva-file bypass: failures stays 0 while
        # total/attempted sink below the registered floor.
        cfg_path = self.tmp / "iverif.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["sva_baseline"] = "sim/regress/sva_baseline.json"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        bl = self.tmp / "sim" / "regress" / "sva_baseline.json"
        bl.parent.mkdir(parents=True, exist_ok=True)
        bl.write_text('{"total_min": 12, "attempted_min": 12}',
                      encoding="utf-8")
        self.write_log(UVM_PASS_LOG.replace(
            "Summary: 12 assertions, 12 with attempts, 0 with failures",
            "Summary: 12 assertions, 3 with attempts, 0 with failures"))
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("baseline", (cp.stderr + cp.stdout).lower())

    def test_configured_baseline_missing_is_fail_closed(self):
        cfg_path = self.tmp / "iverif.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["sva_baseline"] = "sim/regress/sva_baseline.json"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        self.write_log(UVM_PASS_LOG)
        cp = self.evidence("--scen", "M1-01", "--test", "fixture_test",
                           "--seed", "1")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("fail-closed", cp.stderr + cp.stdout)


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
