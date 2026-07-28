"""Constitution gate (axiom 0, self-application): every shipped doc names
its generating axioms and its consumer in a unified provenance header, and
CONSTITUTION.md's mechanism index covers the whole snapshot. A mechanism
nobody reads does not exist — this test makes that axiom machine-checked
for the framework's own docs."""
import re
import sys
import unittest
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(FRAMEWORK / "kernel"))
import fwsync  # noqa: E402

AXIOMS = {"self-application", "independence", "recording",
          "consumption", "pain-gating"}

HDR = re.compile(
    r"<!--\s*Canonical:\s*iverif-workflow/(\S+)\s+—\s+"
    r"(?:pinned snapshot|rendered[^.]*)\.\s+"
    r"Axioms:\s*([^.]+)\.\s+Consumer:\s*([^>]*?\S)\.\s*-->", re.S)


def shipped_md():
    """Every canon .md that reaches a project: the pinned snapshot set plus
    the rendered sources (agents, CLAUDE templates)."""
    docs = [src for src, _ in fwsync.snapshot_pairs(FRAMEWORK, profile="all")
            if src.suffix == ".md"]
    docs += sorted((FRAMEWORK / "harness" / "agents").glob("*.md"))
    docs += sorted((FRAMEWORK / "harness" / "templates")
                   .glob("CLAUDE.project.*.md"))
    return docs


class TestProvenanceHeaders(unittest.TestCase):
    def test_every_shipped_doc_carries_header(self):
        bad = []
        for doc in shipped_md():
            rel = doc.relative_to(FRAMEWORK).as_posix()
            head = "\n".join(doc.read_text(encoding="utf-8")
                             .split("\n")[:15])
            m = HDR.search(head)
            if not m:
                bad.append("%s: no unified header in the first 15 lines"
                           % rel)
                continue
            if m.group(1) != rel:
                bad.append("%s: header claims canon path %s"
                           % (rel, m.group(1)))
            axioms = {a.strip() for a in m.group(2).split(",")}
            unknown = axioms - AXIOMS
            if not axioms or unknown:
                bad.append("%s: unknown/empty axioms %s" % (rel, unknown))
        self.assertFalse(bad, "\n".join(bad))

    def test_index_covers_snapshot(self):
        text = (FRAMEWORK / "CONSTITUTION.md").read_text(encoding="utf-8")
        missing = []
        for src, dest in fwsync.snapshot_pairs(FRAMEWORK, profile="all"):
            if src.suffix != ".md":
                continue
            key = fwsync.rel_key(dest)
            # both profile variants are covered by the selected-file row
            if key.startswith("workflow/profile."):
                key = "workflow/profile.md"
            if key not in text:
                missing.append(key)
        for grouped in (".claude/agents/", "CLAUDE.md"):
            if grouped not in text:
                missing.append(grouped)
        self.assertFalse(
            missing, "mechanism index rows missing from CONSTITUTION.md "
            "(a mechanism without a listed consumer does not ship): %s"
            % missing)


if __name__ == "__main__":
    unittest.main()
