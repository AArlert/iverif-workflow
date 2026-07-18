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

1. `python3 <fw>/kernel/fwsync.py --pull --into <proj>` — replaces
   `scripts/` (this alone retires the drifted milestone-signoff bug) and
   lays down `workflow/`.
2. Create `iverif.json`:

```json
{
  "framework": "0.1.0",
  "profile": "learning",
  "project_name": "floo_axi_chimney",
  "columns_preset": "zh",
  "columns_override": {"fm_module": "组件"},
  "delivery": {"glob": "tb/{name}.sv"},
  "signoff_glob": "review-M{m}*.md",
  "fl_schema_enforce": false
}
```

   (`signoff_glob` keeps the legacy filename; switch to the canonical
   `signoff-M{m}*.md` at the next milestone. `fl_schema_enforce` off until
   existing bug pages are restructured.)
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
- Optionally migrate archives into `doc/archive/` (then drop the
  `archive_dir` override) — do it in a dedicated commit.
- Keep the existing `.claude/agents/*`; the canonical copilot suite is
  deferred until pulp_axi_xbar_agent (docs/deferred.md).

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
  the dispatch tables and the rev agent; probe availability with
  `command -v xcov`. Its tested Verdi baseline (V-2023.12) is newer than
  the VM's Verdi 2018 — if a tool misbehaves there, record it as a
  `TOOL_ENV` failure record rather than debugging blind.
- **Python**: kernel floor is 3.8 (VM default 3.10 is fine); stdlib only —
  never add a pip dependency to the kernel.
