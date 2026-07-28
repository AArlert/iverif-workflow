"""Guard tests for docs.py — including the fuse test for the
milestone-signoff bug that drifted once (ppa BUG-011: `any(generator)` is
always truthy, so the signoff-file check silently passed)."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from fixture import (make_project, run, set_scenario_green, _table, EN, ZH)


class DocsBase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="iverif_test_"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        make_project(self.tmp)

    def doc(self, name):
        return self.tmp / "doc" / name


class TestCheck(DocsBase):
    def test_clean_fixture_passes(self):
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("docs-check passed", cp.stdout)

    def test_green_without_evidence_fails(self):
        set_scenario_green(self.tmp, with_evidence=False)
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("evidence file missing", cp.stdout)

    def test_evidence_without_replay_line_fails(self):
        set_scenario_green(self.tmp,
                           evidence_first_line="just some excerpt text")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("not a replay command", cp.stdout)

    def test_ghost_reference_fails(self):
        fm = self.doc("feature-matrix.md")
        fm.write_text("# Feature matrix\n\n" + _table(EN["fm_header"], [
            "| F-001 | M1 | smoke | (all) | M1-99 |"]), encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("ghost reference", cp.stdout)

    def test_closed_bug_without_verify_fails(self):
        bugs = self.doc("bugs.md")
        bugs.write_text("# Bugs\n\n" + _table(EN["bug_header"], [
            "| BUG-001 | CLOSED | TB | x | TEST=t SEED=1 | y | abc123 | - |"]),
            encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("closure", cp.stdout)

    def test_bad_status_json_fails(self):
        self.doc("status.jsonl").write_text('{"date": broken\n',
                                            encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("not valid JSON", cp.stdout)

    def test_spec_sha_mismatch_fails(self):
        spec = self.doc("spec.md")
        spec.write_text(spec.read_text(encoding="utf-8") + "\nsneaky edit\n",
                        encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("pinned sha256", cp.stdout)

    def test_tracked_junk_file_fails(self):
        subprocess.run(["git", "init", "-q", str(self.tmp)], check=True)
        (self.tmp / ".Makefile.swp").write_text("junk", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.tmp), "add", "-f",
                        ".Makefile.swp"], check=True)
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("junk file tracked by git", cp.stdout)

    def test_fl_page_schema_enforced_for_terminal_bug(self):
        set_scenario_green(self.tmp)
        ev_rel = "doc/evidence/v0.1.0/M1-01.log"
        self.doc("bugs.md").write_text(
            "# Bugs\n\n" + _table(EN["bug_header"], [
                "| BUG-001 | CLOSED | TB | see doc/bugs/BUG-001.md | "
                "TEST=t SEED=1 | y | abc123 | %s |" % ev_rel]),
            encoding="utf-8")
        page = self.doc("bugs") / "BUG-001.md"
        page.write_text("# BUG-001\n\n## symptom\nmismatch\n",
                        encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("regression_guard", cp.stdout)
        # A complete chart passes.
        page.write_text(
            "# BUG-001\n"
            "\n## symptom\nmismatch\n"
            "\n## first_anomaly\nsignal: x time: 10ns\n"
            "\n## taxonomy\nTB_BUG\n"
            "\n## rca\nchain\n"
            "\n## fix\ncommit: abc123\n"
            "\n## rerun\n%s\n"
            "\n## regression_guard\ntype: directed_test ref: t\n"
            "\n## similar\nnone searched-on: mismatch\n" % ev_rel,
            encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)

    def test_zh_preset_passes(self):
        zh = Path(tempfile.mkdtemp(prefix="iverif_zh_"))
        self.addCleanup(shutil.rmtree, zh, True)
        make_project(zh, columns="zh")
        cp = run(zh, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        set_scenario_green(zh, columns="zh")
        cp = run(zh, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)


class TestSignoffGate(DocsBase):
    """Fuse for the drifted-once bug: with every scenario green and the
    evidence dir existing, `--next` must still demand the signoff file, and
    only report completion once it exists. Under the buggy `any(generator)`
    the first assertion fails — which is exactly the point."""

    def _green_with_regress_summary(self):
        set_scenario_green(self.tmp)
        ev_dir = self.tmp / "doc" / "evidence" / "v0.1.0"
        (ev_dir / "result_summary.txt").write_text(
            "fixture regression passed=1/1\n", encoding="utf-8")
        return ev_dir

    def test_signoff_missing_is_reported(self):
        self._green_with_regress_summary()
        cp = run(self.tmp, "docs.py", "--next", check=True)
        self.assertIn("still missing", cp.stdout)
        self.assertIn("signoff", cp.stdout)

    def test_signoff_present_completes_milestone(self):
        ev_dir = self._green_with_regress_summary()
        (ev_dir / "signoff-M1.md").write_text("# signoff\nverdict: pass\n",
                                              encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--next", check=True)
        self.assertNotIn("still missing", cp.stdout)
        self.assertIn("three hard conditions met", cp.stdout)

    def test_signoff_command_lists_conditions(self):
        self._green_with_regress_summary()
        cp = run(self.tmp, "docs.py", "--signoff")
        self.assertEqual(cp.returncode, 0, cp.stdout)
        self.assertIn("[PASS] 1.", cp.stdout)
        self.assertIn("[PASS] 2.", cp.stdout)
        self.assertIn("[PASS] 3.", cp.stdout)
        self.assertIn("not yet", cp.stdout)  # signoff file itself

    def test_signoff_command_fails_with_open_scenario(self):
        cp = run(self.tmp, "docs.py", "--signoff")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("[FAIL] 1.", cp.stdout)
        self.assertIn("M1-01", cp.stdout)


class TestArchive(DocsBase):
    def test_archive_roundtrip(self):
        # Inflate log.md to 6 blocks and status.jsonl to 14 lines.
        log = self.doc("log.md")
        blocks = "".join("## [0.1.0] 2026-07-%02d block%d\n\n- x\n\n"
                         % (18 - i, i) for i in range(6))
        log.write_text("# Work log\n\n" + blocks, encoding="utf-8")
        st = self.doc("status.jsonl")
        lines = [json.dumps({"date": "2026-07-01", "version": "0.1.0",
                             "summary": "s%d" % i}) for i in range(14)]
        st.write_text("\n".join(lines) + "\n", encoding="utf-8")

        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("docs-archive", cp.stdout)

        run(self.tmp, "docs.py", "--archive", check=True)
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)
        # Rolling files trimmed to keep limits; archives newest-first.
        self.assertEqual(len([l for l in st.read_text(encoding="utf-8")
                              .splitlines() if l.strip()]), 8)
        arch = (self.tmp / "doc" / "archive" / "status-archive.jsonl")
        archived = [l for l in arch.read_text(encoding="utf-8").splitlines()
                    if l.strip()]
        self.assertEqual(len(archived), 6)
        self.assertIn("s8", archived[0])

    def test_archive_idempotent(self):
        run(self.tmp, "docs.py", "--archive", check=True)
        cp = run(self.tmp, "docs.py", "--archive", check=True)
        self.assertIn("nothing to archive", cp.stdout)


class TestAcceptedState(DocsBase):
    """FB-17: scheduled debt — neither WONTFIX-as-later nor OPEN-as-decided."""
    def add_bug(self, status, root="REV-002 accepted, do in M2"):
        bugs = self.doc("bugs.md")
        bugs.write_text(bugs.read_text(encoding="utf-8")
                        + "| BUG-0009 | %s | TB | corner x | TEST=x SEED=1 "
                        "| %s | - | - |\n" % (status, root),
                        encoding="utf-8")

    def test_accepted_unexpired_passes_and_due_surfaces(self):
        self.add_bug("ACCEPTED@M2")   # fixture milestone is M1: unexpired
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)
        cp = run(self.tmp, "docs.py", "--next", check=True)
        self.assertNotIn("accepted debt due", cp.stdout)

    def test_accepted_due_this_milestone_surfaces_in_next(self):
        self.add_bug("ACCEPTED@M1")   # == current: check ok, next surfaces
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)
        cp = run(self.tmp, "docs.py", "--next", check=True)
        self.assertIn("accepted debt due", cp.stdout)
        cp = run(self.tmp, "docs.py", "--signoff")
        self.assertIn("accepted debt due", cp.stdout)

    def test_accepted_overdue_fails_check(self):
        self.add_bug("ACCEPTED@M0")   # < current milestone: expired
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("expired", cp.stdout)

    def test_rubric_and_tool_agree_on_condition3(self):
        # FB-18(a): 0.5.0 updated the tool but not rubric.md — the card's
        # criteria source and the tool gave opposite verdicts on the same
        # gate. Pin both surfaces to the ACCEPTED-aware wording, and pin
        # the #7 rationale spot check (FB-18(b)) on both.
        rubric = (Path(__file__).resolve().parents[2] / "signoff"
                  / "rubric.md").read_text(encoding="utf-8")
        self.assertIn("ACCEPTED@M<n>", rubric)
        self.assertIn("7. **Accepted debt is real debt.**", rubric)
        cp = run(self.tmp, "docs.py", "--signoff")
        self.assertIn("ACCEPTED-unexpired", cp.stdout)
        self.assertIn("7. accepted debt", cp.stdout)

    def test_accepted_without_rev_reference_fails(self):
        self.add_bug("ACCEPTED@M2", root="just later")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("rev-signed rationale", cp.stdout)


class TestTableStructure(DocsBase):
    def test_unescaped_pipe_row_fails_check(self):
        # pulp FB-14: an unescaped | in a cell shifts later columns and
        # state gates read the wrong cells — docs-check must catch both
        # directions (too many / too few cells).
        bugs = self.doc("bugs.md")
        bugs.write_text(bugs.read_text(encoding="utf-8")
                        + "| BUG-1 | OPEN | TB | full=|cnt busted | r "
                        "| - | - | - |\n", encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("escape literal |", cp.stdout)
        self.assertIn("bugs.md", cp.stdout)


class TestChainAudit(DocsBase):
    def test_dangling_ref_fails(self):
        self.doc("spec.md").write_text("# Spec\n\n## 1. intro\n",
                                       encoding="utf-8")
        (self.doc("testplan.md")).write_text(
            "# Testplan\n\n" + _table(EN["tp_header"], [
                "| M1-01 | M1 | checks SPEC-9.9 | base | 🔲 | - | - |"]),
            encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--chain-audit")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("SPEC-9.9", cp.stdout)
        self.assertIn("FAIL", cp.stdout)

    def test_clean_audit_reports_gaps_without_failing(self):
        self.doc("spec.md").write_text(
            "# Spec\n\n## 1. x\n### 1.1 y\nrule §1.2.3 inline\n",
            encoding="utf-8")
        (self.doc("testplan.md")).write_text(
            "# Testplan\n\n" + _table(EN["tp_header"], [
                "| M1-01 | M1 | SPEC-1.1 basic | base | 🔲 | - | - |",
                "| M1-02 | M1 | SPEC-1.2.3.4 deep | base | 🔲 | - | - |",
                "| M1-03 | M1 | no ref here | base | 🔲 | - | - |"]),
            encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--chain-audit")
        self.assertEqual(cp.returncode, 0, cp.stdout)
        self.assertIn("dangling spec refs (cited, no such section): 0",
                      cp.stdout)
        self.assertIn("citing no spec clause: 1 — M1-03", cp.stdout)
        self.assertIn("M1-02 SPEC-1.2.3.4→§1.2.3", cp.stdout)
        self.assertIn("scenarios in no feature-matrix row: 2", cp.stdout)


class TestGuards(DocsBase):
    def test_guards_query_matches_paths(self):
        # pulp BUG-0015判例 fuse: a guard that names its victim files must
        # surface when those files are about to be touched.
        page = self.doc("bugs") / "BUG-0001.md"
        page.write_text(
            "# BUG-0001\n\n## regression_guard\ntype: checklist\n"
            "paths: tb/sva/*.sv, sim/Makefile\n"
            "note: fold tracked-state reads before property use\n",
            encoding="utf-8")
        cp = run(self.tmp, "docs.py", "--guards", "tb/sva/stall_sva.sv",
                 "rtl/core.sv", check=True)
        self.assertIn("BUG-0001", cp.stdout)
        self.assertIn("fold tracked-state reads", cp.stdout)
        self.assertIn("1 guard(s) matched", cp.stdout)
        cp = run(self.tmp, "docs.py", "--guards", "rtl/core.sv", check=True)
        self.assertIn("0 guard(s) matched", cp.stdout)


class TestChainRepro(DocsBase):
    def test_chain_and_repro(self):
        set_scenario_green(self.tmp)
        cp = run(self.tmp, "docs.py", "--chain", "M1-01", check=True)
        self.assertIn("evidence head", cp.stdout)
        self.assertIn("make run TEST=fixture_test SEED=1", cp.stdout)
        cp = run(self.tmp, "docs.py", "--repro", "M1-01", check=True)
        self.assertEqual(cp.stdout.strip(),
                         "make run TEST=fixture_test SEED=1")

    def test_repro_without_command_fails(self):
        cp = run(self.tmp, "docs.py", "--repro", "M1-01")
        self.assertNotEqual(cp.returncode, 0)


class TestProfiles(DocsBase):
    def test_learning_next_speaks_to_human(self):
        cp = run(self.tmp, "docs.py", "--next", check=True)
        self.assertIn("learning profile", cp.stdout)
        self.assertNotIn("dispatch", cp.stdout.lower())

    def test_next_phrases_override(self):
        # FB-8 (pulp_axi_xbar): `--next` wording carries role assumptions
        # ("dispatch DE card") that a vendored-DUT project cannot correct
        # without editing scripts/. The iverif.json hook remaps a phrase;
        # an unknown key fails loudly instead of silently no-opping.
        ov = Path(self.tmp.parent) / (self.tmp.name + "_np")
        self.addCleanup(shutil.rmtree, ov, True)
        make_project(ov, overrides={"next_phrases_override": {
            "unverified": "OVERRIDDEN %(mod)s -> %(scenes)s"}})
        cp = run(ov, "docs.py", "--next", check=True)
        self.assertIn("OVERRIDDEN (all) -> M1-01", cp.stdout)
        bad = Path(self.tmp.parent) / (self.tmp.name + "_npbad")
        self.addCleanup(shutil.rmtree, bad, True)
        make_project(bad, overrides={"next_phrases_override": {
            "no_such_phrase": "x"}})
        cp = run(bad, "docs.py", "--next")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("no_such_phrase", cp.stderr + cp.stdout)

    def test_copilot_next_derives_deliverable_owner(self):
        # FB-8 root fix (user ruling 2026-07-28): the deliverable-owning
        # role in `--next` copilot wording derives from delivery config the
        # project already declares — tb/-rooted glob → DV (vendored-DUT
        # repos), zero config needed. Explicit delivery.owner overrides.
        def co_project(suffix, cfg_overrides, with_prompt):
            p = Path(self.tmp.parent) / (self.tmp.name + suffix)
            self.addCleanup(shutil.rmtree, p, True)
            make_project(p, profile="copilot", overrides=cfg_overrides)
            (p / "doc" / "feature-matrix.md").write_text(
                "# Feature matrix\n\n" + _table(EN["fm_header"], [
                    "| F-001 | M1 | smoke bring-up | (all) | M1-01 |",
                    "| F-002 | M1 | widget feature | widget | M1-01 |"]),
                encoding="utf-8")
            if with_prompt:
                (p / "doc" / "design-prompt" / "widget.md").write_text(
                    "# widget\n", encoding="utf-8")
            return p

        # fixture glob is tb/{name}.sv → derived owner DV, both phrases
        p = co_project("_dv", {}, with_prompt=True)
        cp = run(p, "docs.py", "--next", check=True)
        self.assertIn("dispatch DV card", cp.stdout)
        p = co_project("_dvp", {}, with_prompt=False)
        cp = run(p, "docs.py", "--next", check=True)
        self.assertIn("rev gate before any DV card", cp.stdout)
        # explicit owner beats the derivation
        p = co_project("_de", {"delivery": {"glob": "tb/{name}.sv",
                                            "owner": "de"}},
                       with_prompt=True)
        cp = run(p, "docs.py", "--next", check=True)
        self.assertIn("dispatch DE card", cp.stdout)
        # invalid owner fails loudly
        p = co_project("_bad", {"delivery": {"glob": "tb/{name}.sv",
                                             "owner": "orch"}},
                       with_prompt=True)
        cp = run(p, "docs.py", "--next")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("delivery.owner", cp.stderr + cp.stdout)

    def test_copilot_requires_design_prompt_dir(self):
        co = Path(self.tmp.parent) / (self.tmp.name + "_co")
        self.addCleanup(shutil.rmtree, co, True)
        make_project(co, profile="copilot")
        cp = run(co, "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)
        (co / "doc" / "design-prompt" / "README.md").unlink()
        cp = run(co, "docs.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("design-prompt", cp.stdout)


if __name__ == "__main__":
    unittest.main()
