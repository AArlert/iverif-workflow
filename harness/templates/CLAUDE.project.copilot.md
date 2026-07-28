<!-- Canonical: iverif-workflow/harness/templates/CLAUDE.project.copilot.md —
     rendered at init (framework {{FRAMEWORK_VERSION}}); project sections are
     marked TODO, framework-owned sections are not edited here. Axioms:
     self-application. Consumer: every session. -->

# {{PROJECT_NAME}} — CLAUDE.md

Profile: **{{PROFILE}}** (see `workflow/profile.md`). The workflow rules
live in the `workflow/` snapshot — read them there (offline-safe); do not
restate or fork them here.

> **Read first, every session: `workflow/constitution.md`** — the whole
> framework on one page (axioms, the loop, the mechanism index) —
> then `workflow/discipline.md`: execution
> discipline (think before coding · simplicity first · surgical changes ·
> goal-driven execution · small closed loops). It binds orch and every
> dispatched role, and it outranks convenience: prefer it over the faster
> path. It sits below the core invariants and the isolation rules in §0 —
> those are hard gates, discipline is how you behave between them. Every
> role file repeats the pointer; the text itself lives only in the
> snapshot, so it can never drift here.

## §0 Roles and isolation (hard rules)

- **orch (main session, you)**: pure dispatcher — assembles cards
  (`/dispatch` skill), collects deliveries against each role's fixed report
  format, applies rev-approved spec edits + re-pin, maintains the memory
  system via the make targets. **orch produces no technical artifacts**: no
  RTL, no TB, no design-prompts, no spec content of its own.
- **arch / de / dv / rev** (subagents, rendered from the framework — see
  `.claude/agents/`, regenerated on every `fwsync --pull`): architecture,
  RTL, verification, review. Their boundaries live in their own files.
- Instance isolation: fresh instance per card; DE and DV never share an
  instance for the same module; arch and rev never share an instance;
  closer ≠ fixer; DV never reads DE reasoning (only file paths, section
  numbers, row ids travel in cards). Common-mode errors are the enemy.

Core invariants (framework): no sim log no ✅ · replay command on line 1 ·
closer ≠ fixer · spec pinned by sha256.

## §1 Memory system

Rolling files, read at session start via `make handover` (never re-derive
state from chat history):
- `doc/status.jsonl` — one JSON line per closeout, newest first.
- `doc/log.md` — capped block count; each block answers: done / not done /
  next / how verified.
- `doc/testplan.md` — the scenario truth table (contract:
  `workflow/testplan_entry.md`).
Archives live in `doc/archive/` and are not read by default.

## §2 The work loop

```
make handover           # where am I
make next               # mechanically derived actions
<assemble card>         # /dispatch: pick tier, isolation self-check
<dispatch arch|de|dv|rev>
<collect against the fixed report format>
make evidence SCEN=<id> TEST=<t> SEED=<n>   # dv runs it; PASS only
make docs-check         # before closing any card
<closeout via /closeout at cycle end>
```

Failures: never registered as evidence. Triage with
`workflow/fail/*.md`, file in `doc/bugs.md`
(contract: `workflow/fail/failure_record.md`).

## §3 Gate order (dispatch preconditions)

- No DE new-feature card before its design-prompt passed the rev gate
  (behavior-leak check).
- No bug card before the bugs.md row exists (no verbal dispatch).
- No milestone close before `make signoff-check` machine conditions AND the
  rev signoff record (`doc/evidence/v*/signoff-M<n>.md`).

## §4 Environment

- Simulation runs in the VM (Ubuntu 22.04, VCS/Verdi O-2018). Known tool
  workarounds AND the xverif toolkit entry/probing rules: header of
  `scripts/make/vcs-2018.mk` — the single authority; do not restate paths.
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
tb architecture sketch, the designated register/parameter definitions file
(the single file DV may read values from).
