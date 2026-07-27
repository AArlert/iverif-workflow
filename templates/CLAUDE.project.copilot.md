<!-- Rendered by fwsync from iverif-workflow/templates/CLAUDE.project.copilot.md
     (framework {{FRAMEWORK_VERSION}}). Project-specific sections are marked
     TODO; the framework-owned sections should not be edited here. -->

# {{PROJECT_NAME}} — CLAUDE.md

Profile: **{{PROFILE}}** (see `workflow/profiles.md`). The workflow rules
live in the `workflow/` snapshot — read them there (offline-safe); do not
restate or fork them here.

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
  `workflow/schema/testplan_entry.md`).
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
`workflow/dispatch/*.md`, file in `doc/bugs.md`
(contract: `workflow/schema/failure_record.md`).

## §3 Gate order (dispatch preconditions)

- No DE new-feature card before its design-prompt passed the rev gate
  (behavior-leak check).
- No bug card before the bugs.md row exists (no verbal dispatch).
- No milestone close before `make signoff-check` machine conditions AND the
  rev signoff record (`doc/evidence/v*/signoff-M<n>.md`).

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
tb architecture sketch, the designated register/parameter definitions file
(the single file DV may read values from).
