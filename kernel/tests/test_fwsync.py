"""fwsync tests: scaffolding produces a gate-clean project; the manifest
detects tampering and missing files; pulls refresh the snapshot; hashes are
line-ending independent (Windows host vs Linux VM)."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parents[2]


def run_py(script, *args, cwd=None):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    return subprocess.run([sys.executable, str(script), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          env=env, cwd=str(cwd) if cwd else None)


class FwsyncBase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="iverif_fw_"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.fw = self.tmp / "fw"
        shutil.copytree(FRAMEWORK, self.fw,
                        ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                      "tests"))
        self.proj = self.tmp / "proj"

    def init_project(self, *extra):
        cp = run_py(self.fw / "kernel" / "fwsync.py", "--init",
                    str(self.proj), *extra)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        return cp


class TestInit(FwsyncBase):
    def test_init_passes_all_gates(self):
        self.init_project()
        cp = run_py(self.proj / "scripts" / "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("fw-check passed", cp.stdout)
        cp = run_py(self.proj / "scripts" / "docs.py", "--handover")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_init_pins_workflow_and_renders_agent(self):
        self.init_project("--project", "my_dut")
        self.assertTrue(
            (self.proj / "workflow" / "review" / "six_questions.md")
            .exists())
        self.assertTrue(
            (self.proj / "workflow" / "constitution.md").exists())
        # Profile contract arrives as workflow/profile.md — only the
        # project's own profile, selected at sync (no in-file markers).
        prof = ((self.proj / "workflow" / "profile.md")
                .read_text(encoding="utf-8"))
        self.assertIn("thinking checklist", prof)
        self.assertNotIn("Instance isolation (hard rules)", prof)
        rev = (self.proj / ".claude" / "agents" / "rev.md")
        self.assertTrue(rev.exists())
        text = rev.read_text(encoding="utf-8")
        self.assertIn("my_dut", text)
        self.assertNotIn("{{PROJECT_NAME}}", text)

    def test_discipline_reaches_project_and_every_role_points_at_it(self):
        # The execution rules are only worth having if they arrive with the
        # snapshot and every actor is told to read them. The text lives in
        # workflow/ alone — CLAUDE.md and the role files carry pointers, so
        # a local restatement can never drift out of sync with canon.
        self.init_project("--profile", "copilot")
        self.assertTrue((self.proj / "workflow" / "discipline.md").exists())
        claude = (self.proj / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("workflow/discipline.md", claude)
        for role in ("arch", "de", "dv", "rev"):
            text = ((self.proj / ".claude" / "agents" / ("%s.md" % role))
                    .read_text(encoding="utf-8"))
            self.assertIn("workflow/discipline.md", text, role)

    def test_init_zh_columns_pass_gates(self):
        self.init_project("--columns", "zh")
        tp = (self.proj / "doc" / "testplan.md").read_text(encoding="utf-8")
        self.assertIn("里程碑", tp)
        cp = run_py(self.proj / "scripts" / "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_learning_init_agent_and_skill_set(self):
        self.init_project()
        agents = self.proj / ".claude" / "agents"
        self.assertTrue((agents / "rev.md").exists())
        self.assertEqual([p.name for p in agents.glob("*.md")], ["rev.md"])
        for f in (self.proj / "CLAUDE.md", agents / "rev.md"):
            self.assertIn("workflow/discipline.md",
                          f.read_text(encoding="utf-8"), f.name)
        skills = self.proj / ".claude" / "skills"
        for name in ("handover", "evidence", "closeout"):
            self.assertTrue((skills / name / "SKILL.md").exists(), name)
        # the orch dispatch manual must NOT reach a learning repo
        self.assertFalse((skills / "dispatch" / "SKILL.md").exists())

    def test_copilot_init_renders_full_suite(self):
        self.init_project("--profile", "copilot", "--project", "my_dut")
        agents = self.proj / ".claude" / "agents"
        for name in ("arch", "de", "dv", "rev"):
            f = agents / ("%s.md" % name)
            self.assertTrue(f.exists(), name)
            text = f.read_text(encoding="utf-8")
            self.assertIn("my_dut", text)
            self.assertNotIn("{{", text)  # no unrendered placeholders
        self.assertTrue((self.proj / ".claude" / "skills" / "dispatch"
                         / "SKILL.md").exists())
        claude = (self.proj / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("orch", claude)
        self.assertIn("Instance isolation", claude)
        prof = ((self.proj / "workflow" / "profile.md")
                .read_text(encoding="utf-8"))
        self.assertIn("Instance isolation (hard rules)", prof)
        self.assertNotIn("thinking checklist", prof)
        # skills are part of the pinned snapshot; the whole init is green
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        cp = run_py(self.proj / "scripts" / "docs.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_init_refuses_nonempty_target(self):
        self.proj.mkdir()
        (self.proj / "stuff.txt").write_text("x", encoding="utf-8")
        cp = run_py(self.fw / "kernel" / "fwsync.py", "--init",
                    str(self.proj))
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("not empty", cp.stderr + cp.stdout)


class TestDriftDetection(FwsyncBase):
    def setUp(self):
        super().setUp()
        self.init_project()

    def test_local_edit_detected(self):
        docs = self.proj / "scripts" / "docs.py"
        docs.write_text(docs.read_text(encoding="utf-8")
                        + "\n# sneaky local tweak\n", encoding="utf-8")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("modified locally", cp.stdout)
        self.assertIn("scripts/docs.py", cp.stdout)

    def test_missing_pinned_file_detected(self):
        (self.proj / "workflow" / "review" / "rubric.md").unlink()
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("missing", cp.stdout)

    def test_crlf_working_tree_still_passes(self):
        # Simulate a Windows checkout: same content, CRLF endings.
        f = self.proj / "workflow" / "review" / "rubric.md"
        data = f.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        f.write_bytes(data)
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)


class TestPull(FwsyncBase):
    def test_pull_refreshes_snapshot_and_version(self):
        self.init_project()
        # Framework evolves: content change + version bump.
        rubric = self.fw / "loop" / "review" / "rubric.md"
        rubric.write_text(rubric.read_text(encoding="utf-8")
                          + "\nnew rubric clause\n", encoding="utf-8")
        (self.fw / "VERSION").write_text("0.2.0\n", encoding="utf-8")

        cp = run_py(self.proj / "scripts" / "fwsync.py", "--pull",
                    str(self.fw))
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

        self.assertIn("new rubric clause",
                      (self.proj / "workflow" / "review" / "rubric.md")
                      .read_text(encoding="utf-8"))
        manifest = json.loads(
            (self.proj / "scripts" / "iverif.manifest.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(manifest["framework"], "0.2.0")
        cfg = json.loads((self.proj / "iverif.json")
                         .read_text(encoding="utf-8"))
        self.assertEqual(cfg["framework"], "0.2.0")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)


class TestSoftAdaptation(FwsyncBase):
    def test_pull_uses_framework_repo_key(self):
        # Fork-as-upstream: --init records the upstream path; a bare
        # `--pull` (make fw-pull) resolves it from iverif.json.
        self.init_project()
        cfg = json.loads((self.proj / "iverif.json")
                         .read_text(encoding="utf-8"))
        self.assertEqual(cfg["framework_repo"], os.path.join("..", "fw"))
        (self.fw / "VERSION").write_text("9.9.9\n", encoding="utf-8")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--pull")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        m = json.loads((self.proj / "scripts" / "iverif.manifest.json")
                       .read_text(encoding="utf-8"))
        self.assertEqual(m["framework"], "9.9.9")

    def test_declared_divergence_yellow_undeclared_red(self):
        self.init_project()
        docs = self.proj / "scripts" / "docs.py"
        docs.write_text(docs.read_text(encoding="utf-8") + "\n# local\n",
                        encoding="utf-8")
        (self.proj / "scripts" / "iverif.divergence.json").write_text(
            json.dumps({"files": {"scripts/docs.py": {
                "reason": "hotfix", "upstream_ref": "FB-99"}}}),
            encoding="utf-8")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)
        self.assertIn("DECLARED", cp.stdout)
        ev = self.proj / "scripts" / "evidence.py"
        ev.write_text(ev.read_text(encoding="utf-8") + "\n# sneaky\n",
                      encoding="utf-8")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("undeclared", cp.stdout)


class TestPullIntegrity(FwsyncBase):
    def test_pull_bootstraps_framework_fwsync(self):
        # FB-12 root cause: a pull executed by the PINNED (older) fwsync
        # applies the old snapshot-pairing logic to the new framework and
        # silently pulls an incomplete set. The hop must make the pinned
        # copy's pairing logic irrelevant.
        self.init_project("--profile", "copilot")
        pinned = self.proj / "scripts" / "fwsync.py"
        pinned.write_text(pinned.read_text(encoding="utf-8").replace(
            "profile.%s.md", "no_such.%s.md"), encoding="utf-8")
        (self.proj / "workflow" / "profile.md").unlink()
        cp = run_py(pinned, "--pull")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertTrue((self.proj / "workflow" / "profile.md").exists())

    def test_pull_fail_closed_on_bad_profile(self):
        self.init_project()
        cfgp = self.proj / "iverif.json"
        cfg = json.loads(cfgp.read_text(encoding="utf-8"))
        cfg["profile"] = "copliot"  # typo — must refuse, not degrade
        cfgp.write_text(json.dumps(cfg), encoding="utf-8")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--pull")
        self.assertNotEqual(cp.returncode, 0)
        self.assertIn("refusing a partial pull", cp.stderr + cp.stdout)

    def test_orphan_sweep_and_incomplete_manifest_detected(self):
        import hashlib
        self.init_project()
        orphan = self.proj / "workflow" / "obsolete.md"
        orphan.write_text("old doc\n", encoding="utf-8")
        mpath = self.proj / "scripts" / "iverif.manifest.json"
        m = json.loads(mpath.read_text(encoding="utf-8"))
        m["files"]["workflow/obsolete.md"] = hashlib.sha256(
            b"old doc\n").hexdigest()
        mpath.write_text(json.dumps(m), encoding="utf-8")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--pull")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertFalse(orphan.exists())
        self.assertIn("removed orphan", cp.stdout)
        # An incomplete manifest (profile contract not pinned) must fail
        # fw-check even though every listed hash is self-consistent.
        m = json.loads(mpath.read_text(encoding="utf-8"))
        del m["files"]["workflow/profile.md"]
        mpath.write_text(json.dumps(m), encoding="utf-8")
        (self.proj / "workflow" / "profile.md").unlink()
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("manifest incomplete", cp.stdout)

    def test_constitution_missing_from_manifest_fails_check(self):
        # The constitution ships to every profile; a manifest without it
        # was written by a pre-0.7.0 fwsync — fail-closed, like profile.md.
        self.init_project()
        mpath = self.proj / "scripts" / "iverif.manifest.json"
        m = json.loads(mpath.read_text(encoding="utf-8"))
        del m["files"]["workflow/constitution.md"]
        mpath.write_text(json.dumps(m), encoding="utf-8")
        (self.proj / "workflow" / "constitution.md").unlink()
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 1)
        self.assertIn("manifest incomplete", cp.stdout)

    def test_pull_migrates_old_layout(self):
        # 0.6.x → 0.7.0 fuse: the snapshot re-lay (workflow/schema|signoff|
        # taxonomy|dispatch → top level + review/ + fail/) must sweep
        # pristine old-path files and leave locally edited ones with a
        # warning — the exact adopter upgrade experience.
        import hashlib
        self.init_project()
        old_pristine = (self.proj / "workflow" / "schema"
                        / "evidence_record.md")
        old_edited = self.proj / "workflow" / "signoff" / "rubric.md"
        old_pristine.parent.mkdir(parents=True, exist_ok=True)
        old_edited.parent.mkdir(parents=True, exist_ok=True)
        old_pristine.write_text("old contract\n", encoding="utf-8")
        old_edited.write_text("locally adapted\n", encoding="utf-8")
        mpath = self.proj / "scripts" / "iverif.manifest.json"
        m = json.loads(mpath.read_text(encoding="utf-8"))
        m["files"]["workflow/schema/evidence_record.md"] = hashlib.sha256(
            b"old contract\n").hexdigest()
        m["files"]["workflow/signoff/rubric.md"] = hashlib.sha256(
            b"what was pinned\n").hexdigest()  # on-disk copy differs
        mpath.write_text(json.dumps(m), encoding="utf-8")
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--pull")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertFalse(old_pristine.exists())
        self.assertIn("removed orphan", cp.stdout)
        self.assertTrue(old_edited.exists())
        self.assertIn("locally modified", cp.stdout)
        self.assertTrue(
            (self.proj / "workflow" / "evidence_record.md").exists())
        cp = run_py(self.proj / "scripts" / "fwsync.py", "--check")
        self.assertEqual(cp.returncode, 0, cp.stdout)


class TestGenManifest(FwsyncBase):
    def test_gen_manifest_covers_snapshot_set(self):
        cp = run_py(self.fw / "kernel" / "fwsync.py", "--gen-manifest")
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        m = json.loads((self.fw / "kernel" / "kernel.manifest.json")
                       .read_text(encoding="utf-8"))
        keys = set(m["files"])
        self.assertIn("scripts/docs.py", keys)
        self.assertIn("scripts/svacheck.py", keys)
        self.assertIn("scripts/make/vcs-2018.mk", keys)
        self.assertIn("workflow/constitution.md", keys)
        self.assertIn("workflow/evidence_record.md", keys)
        self.assertIn("workflow/review/rubric.md", keys)
        self.assertIn("workflow/fail/failure_record.md", keys)
        self.assertIn("workflow/profile.learning.md", keys)
        self.assertIn("workflow/profile.copilot.md", keys)
        self.assertIn(".claude/skills/handover/SKILL.md", keys)
        self.assertIn(".claude/skills/dispatch/SKILL.md", keys)
        self.assertNotIn("scripts/iverif.manifest.json", keys)


if __name__ == "__main__":
    unittest.main()
