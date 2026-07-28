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
    # layout; caps unchanged by the move itself.
    "CONSTITUTION.md": 4800,  # the one-page mental model — hard cap
    "loop/fail/assertion_failure.md": 2450,
    "loop/fail/coverage_hole.md": 1950,
    "loop/fail/regression_failure.md": 1650,
    "loop/discipline.md": 5400,
    "loop/profile.copilot.md": 2200,
    "loop/profile.learning.md": 2200,
    # Raised 0.5.0 (reviewed): CMD-form records + ACCEPTED@M<n> are new
    # operative contracts, not prose growth.
    "loop/evidence_record.md": 3400,
    "loop/fail/failure_record.md": 4400,
    "loop/testplan_entry.md": 2100,
    # Raised 0.5.3 (#7, FB-18) and 0.6.1 (#8, FB-21): new operative
    # contract, not prose growth.
    "loop/review/rubric.md": 2950,
    "loop/review/six_questions.md": 2600,
    "harness/skills/closeout/SKILL.md": 1850,
    # Raised 0.5.4 (reviewed): the signoff-card injection exception is
    # new operative contract from field data (FB-19), not prose growth.
    "harness/skills/dispatch/SKILL.md": 4100,
    "harness/skills/evidence/SKILL.md": 1800,
    "harness/skills/handover/SKILL.md": 1100,
    "loop/fail/failure_taxonomy.md": 4100,
    "loop/fail/rca_template.md": 1800,
    "harness/agents/arch.copilot.md": 4100,
    "harness/agents/de.copilot.md": 4150,
    "harness/agents/dv.copilot.md": 5050,
    "harness/agents/rev.copilot.md": 4300,
    "harness/agents/rev.learning.md": 4300,
    "harness/templates/CLAUDE.project.copilot.md": 4950,
    "harness/templates/CLAUDE.project.learning.md": 4800,
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
