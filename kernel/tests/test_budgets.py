"""Token-budget gate: every doc that ships to projects stays within its
byte cap. Guards against documented prose growing back (rule + provenance +
backstory). Over budget? Trim, or move the story to CHANGELOG /
governance/design-notes.md — raising a cap is a reviewed decision, not a
fix."""
import sys
import unittest
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(FRAMEWORK / "kernel"))
import fwsync  # noqa: E402

BUDGETS = {  # bytes, ~12% headroom over the 0.4.0 diet
    # 0.7.0 re-key (structural refactor): canon paths follow the new
    # layout. All rows +200 at 0.7.0 (reviewed): the unified provenance
    # header (Canonical/Axioms/Consumer, machine-checked by
    # test_constitution) is mandatory contract, not prose growth.
    "CONSTITUTION.md": 4800,  # the one-page mental model — hard cap
    "loop/fail/assertion_failure.md": 2650,
    "loop/fail/coverage_hole.md": 2150,
    "loop/fail/regression_failure.md": 1850,
    "loop/discipline.md": 5600,
    "loop/profile.copilot.md": 2400,
    "loop/profile.learning.md": 2400,
    # Raised 0.5.0 (reviewed): CMD-form records + ACCEPTED@M<n> are new
    # operative contracts, not prose growth.
    "loop/evidence_record.md": 3600,
    "loop/fail/failure_record.md": 4600,
    "loop/testplan_entry.md": 2300,
    # Raised 0.5.3 (#7, FB-18) and 0.6.1 (#8, FB-21): new operative
    # contract, not prose growth.
    "loop/review/rubric.md": 3150,
    "loop/review/six_questions.md": 2800,
    "harness/skills/closeout/SKILL.md": 2050,
    # Raised 0.5.4 (reviewed): the signoff-card injection exception is
    # new operative contract from field data (FB-19), not prose growth.
    # Raised 0.7.1 (reviewed): the L0-L3 grade table (absorbing the old
    # tier list), the spec-gap card row, and the per-card mismatch
    # observer are new operative contract (user ruling 2026-07-29).
    "harness/skills/dispatch/SKILL.md": 4900,
    "harness/skills/evidence/SKILL.md": 2000,
    "harness/skills/handover/SKILL.md": 1300,
    "loop/fail/failure_taxonomy.md": 4300,
    "loop/fail/rca_template.md": 2000,
    "harness/agents/arch.copilot.md": 4300,
    "harness/agents/de.copilot.md": 4350,
    "harness/agents/dv.copilot.md": 5250,
    "harness/agents/rev.copilot.md": 4500,
    "harness/agents/rev.learning.md": 4500,
    "harness/templates/CLAUDE.project.copilot.md": 5150,
    "harness/templates/CLAUDE.project.learning.md": 5000,
}


class TestSnapshotBudgets(unittest.TestCase):
    def test_every_shipped_doc_within_budget(self):
        over = []
        for rel, cap in sorted(BUDGETS.items()):
            size = (FRAMEWORK / rel).stat().st_size
            if size > cap:
                over.append("%s: %d > %d" % (rel, size, cap))
        self.assertFalse(
            over, "over budget (trim, or move prose to design-notes/"
            "CHANGELOG):\n" + "\n".join(over))

    def test_budget_table_covers_snapshot_docs(self):
        missing = [
            src.relative_to(FRAMEWORK).as_posix()
            for src, _ in fwsync.snapshot_pairs(FRAMEWORK, profile="all")
            if src.suffix == ".md"
            and src.relative_to(FRAMEWORK).as_posix() not in BUDGETS]
        self.assertFalse(
            missing, "snapshot docs missing a budget row: %s" % missing)


if __name__ == "__main__":
    unittest.main()
