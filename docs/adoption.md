# Adoption playbooks

Three scenarios, each ≤30 minutes. In every case the framework clone lives
next to your project clones (host and VM both work; hashes are line-ending
independent).

## 1. Brand-new project (pulp_axi_xbar, *_agent, ppa_lite redo)

```bash
python3 iverif-workflow/kernel/fwsync.py --init <dir> \
        --profile learning|copilot --columns en [--project <name>]
cd <dir>
git init && git config core.hooksPath .githooks
make docs-check && make handover        # both pass on the seed
```

Then fill in the project half: vendor the DUT (`templates/VENDOR.md` flow),
write `sim/flist/*.f` + the sim rules (patterns at the tail of
`scripts/make/vcs-2018.mk`), distill `doc/spec.md` v0 and get it
rev-reviewed before pinning, and complete the TODO section of `CLAUDE.md`.
First VM session: `make smoke`, then the first real
`make evidence SCEN=... TEST=... SEED=...`.

## 2. Existing learning repo (floo_axi_chimney, at M1 start)

1. Create `iverif.json` **first** (the pull reads it to pick the vendor set
   and render the agent suite):

```json
{
  "framework": "0.2.0",
  "profile": "learning",
  "project_name": "floo_axi_chimney",
  "columns_preset": "zh",
  "columns_override": {"fm_module": "组件"},
  "delivery": {"glob": "tb/{name}.sv"},
  "signoff_glob": "review-M{m}*.md",
  "fl_schema_enforce": false,
  "sva_enforce": false
}
```

   (`signoff_glob` keeps the legacy filename; switch to the canonical
   `signoff-M{m}*.md` at the next milestone. `fl_schema_enforce` off until
   existing bug pages are restructured. `sva_enforce` off because the
   legacy sim flow predates the pinned `-assert verbose` — flip to `true`
   the moment the run rule adopts `$(SIM_OPTS_2018)`; detected assertion
   failures are fatal either way.)
2. `python3 <fw>/kernel/fwsync.py --pull --into <proj>` — replaces
   `scripts/` (this alone retires the drifted milestone-signoff bug), lays
   down `workflow/` + `.claude/skills/`, and re-renders
   `.claude/agents/rev.md` from the canonical template.
3. Root Makefile: replace the doc-target block with
   `include scripts/make/core.mk` + `include scripts/make/evidence.mk`;
   keep the sim forwarding block.
4. Restore CI from `templates/ci.yml`; `git rm --cached .Makefile.swp` and
   append the junk patterns from `templates/gitignore`.
5. `make docs-check && make fw-check` green → commit.

## 3. Existing copilot repo (ppa-lite-copilot, on its next dev session)

Same as scenario 2 with `"profile": "copilot"`, plus:
- `"columns_preset": "zh"`, `"delivery": {"glob": "rtl/{name}.sv"}`,
  `"signoff_glob": "review-m{m}*-milestone.md"`, `"archive_dir": "doc"`.
- `"sva_enforce": true` and
  `"sva_baseline": "sim/regress/sva_baseline.json"` — ppa's flow already
  pins `-assert verbose` and registers a baseline; the kernel's
  `svacheck.py` reads the same `total_min`/`attempted_min` keys, so the
  existing baseline file carries over unchanged.
- The pull **replaces** `scripts/svacheck.py` with the kernel port and
  **overwrites** `.claude/agents/{arch,de,dv,rev}.md` with the rendered
  canonical (English) suite. Diff before committing; anything
  project-specific in the old agents (register-defs path, module naming
  conventions) moves to `CLAUDE.md` §Project specifics — rendered agent
  files are regenerated on every pull and never hand-edited.
- Project-local extras (`scripts/report.py`, presentation line) stay — they
  are not in the manifest. `report.py` imports `svacheck`; the kernel port
  keeps `scan_text`/`scan_file`/`SUMMARY_RE` compatible, but re-run
  `report.py --check` after the pull to confirm.
- Optionally migrate archives into `doc/archive/` (then drop the
  `archive_dir` override) — do it in a dedicated commit.
- **Line-ending landmine**: ppa has no `.gitattributes`, and `doc/spec.md`
  is stored CRLF in the object store (the only such file; harmless while
  untouched — the spec pin hashes raw bytes, which are stable in the VM).
  If you add the template `.gitattributes` during migration, renormalizing
  will rewrite spec.md's bytes and break the sha256 pin — re-pin
  (`python3 scripts/docs.py --pin-spec`) in the same commit, with a
  change-record row noting "line-ending normalization, no content change".

## Upgrading later (any repo)

```bash
python3 scripts/fwsync.py --pull <framework-clone>   # updates snapshot + iverif.json version
make docs-check                                       # behavior changes surface here
git add -A && git commit                              # snapshot bump is one clean commit
```

Framework-side release ritual: edit → `make selftest` → `make manifest` →
bump `VERSION` + `CHANGELOG.md` → commit + tag.

## Environment notes

- **Windows host + Ubuntu 22.04 VM**: `.gitattributes` pins LF for
  everything the VM executes. Never hand-convert line endings.
- **xverif toolkit** (VM): `xdebug`/`xcov`/`xsva`/`xloc` are referenced by
  the dispatch tables and the agents. It is NOT on PATH (learned the hard
  way — ppa BUG-016 era): entry `$XVERIF_ROOT/tools/` with
  `XVERIF_ROOT ?= /home/open_tools/xverif` exported by
  `scripts/make/vcs-2018.mk`; export VERDI_HOME before xdebug/xcov; probe
  with `test -x $XVERIF_ROOT/tools/xcov`, never `command -v`. Its tested
  Verdi baseline (V-2023.12) is newer than the VM's Verdi 2018 — if a tool
  misbehaves there, record it as a `TOOL_ENV` failure record rather than
  debugging blind.
- **Python**: kernel floor is 3.8 (VM default 3.10 is fine); stdlib only —
  never add a pip dependency to the kernel.
