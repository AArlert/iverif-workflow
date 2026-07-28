<!-- Rendered by fwsync from iverif-workflow/templates/CLAUDE.project.md
     (framework {{FRAMEWORK_VERSION}}). Project-specific sections are marked
     TODO; the framework-owned sections should not be edited here. -->

# {{PROJECT_NAME}} — CLAUDE.md

Profile: **{{PROFILE}}** (see `workflow/profile.md`). The workflow rules
live in the `workflow/` snapshot — read them there (offline-safe); do not
restate or fork them here.

> **Read first, every session: `workflow/discipline.md`** — execution
> discipline (think before coding · simplicity first · surgical changes ·
> goal-driven execution · small closed loops). It binds the main session
> and rev, and it outranks convenience: prefer it over the faster path. It
> sits below the core invariants and §0's role split — those are hard
> gates, discipline is how you behave between them. The text lives only in
> the snapshot, so it can never drift here.

## §0 Roles

<!-- learning profile -->
- **User**: the DV engineer. Writes ALL core UVM logic by hand — sequences,
  drivers, monitors, scoreboards, covergroups, SVA. This is the point of the
  repo.
- **Main session (you)**: infrastructure only — directories, Makefiles,
  flists, compilable skeletons (class files + phase signatures + TODO
  comments, nothing more), mechanical spec distillation, dispatching rev,
  maintaining the memory system via the make targets. Guidance is
  principles + direction, never pasted implementations.
- **rev** (only subagent): reviewer and mentor. Written reviews to
  `doc/review/REV-<seq>.md`, milestone signoffs to
  `doc/evidence/v*/signoff-M<n>.md`. Never edits code.

Core invariants (framework): no sim log no ✅ · replay command on line 1 ·
closer ≠ fixer · spec pinned by sha256.

## §1 Memory system

Rolling files, read at session start via `make handover` (never re-derive
state from chat history):
- `doc/status.jsonl` — one JSON line per closeout, newest first.
- `doc/log.md` — capped block count; each block answers: done / not done /
  next / how verified.
- `doc/testplan.md` — the scenario truth table (contract:
  `workflow/schema/testplan_entry.md`).
Archives live in `doc/archive/` and are not read by default.

## §2 The daily loop

```
make handover           # where am I
make next               # mechanically derived actions
<register scenario row> # before writing any test code
<write code>            # user writes; main session may scaffold skeletons
make run TEST=<t> SEED=<n>       # in the VM
make evidence SCEN=<id> TEST=<t> SEED=<n>   # PASS only; backfills testplan
<request rev review at component/scenario milestones>
make bump && <fill skeletons> && make docs-check && commit && push  # closeout
```

Failures: never registered as evidence. Triage with
`workflow/dispatch/*.md`, file in `doc/bugs.md`
(contract: `workflow/schema/failure_record.md`).

## §3 Thinking checklist (single-human substitute for role isolation)

- Derive expected values from `doc/spec.md`, never from the RTL under test.
- Before closing your own bug: re-run the original failing seed + one
  neighboring scenario; evidence first, status second (the script does the
  status anyway).
- A test that cannot plausibly fail is decoration — tighten the checker.
- Write review requests as if the reviewer knows nothing you did not write
  down.

## §4 Environment

- Simulation runs in the VM (Ubuntu 22.04, VCS/Verdi O-2018). Known tool
  workarounds: `scripts/make/vcs-2018.mk` header. The xverif toolkit
  (`xdebug`/`xcov`/`xsva`/`xloc`) is NOT on PATH: entry
  `$XVERIF_ROOT/tools/` (default `/home/open_tools/xverif`, exported by
  `scripts/make/vcs-2018.mk`); export VERDI_HOME first; probe with
  `test -x $XVERIF_ROOT/tools/xcov`, never `command -v`.
- This repo is developed on the host and cloned into the VM; line endings
  are pinned by `.gitattributes` — do not fight it.

## §5 Git

- Conventional commits. Evidence lands in the same commit as the code it
  certifies. Push after closeout.
- Hooks: `git config core.hooksPath .githooks` once per clone.
- `scripts/`, `workflow/`, and `.claude/skills/` are a hash-pinned
  framework snapshot (`make fw-check`); `.claude/agents/` is regenerated on
  every pull. Improvements flow to the framework repo first:
  <https://github.com/AArlert/iverif-workflow>

## §6 Project specifics

TODO: DUT description, spec source materials, milestone plan, flist layout,
tb architecture sketch.
