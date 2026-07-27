# Changelog

All framework changes land here. Project repos decide when to `fwsync --pull`
based on this file; the version they carry is recorded in their `iverif.json`.

## 0.2.1 — 2026-07-27

Bug/doc fixes flowed back from `pulp_axi_xbar_copilot`'s first real-world
adoption (FB-1~FB-7 in its `doc/fw-feedback.md`); no new mechanism.

- **`kernel/evidence.py`** (the one real logic fix): non-UVM tb (ucli
  `run;exit`-driven `$stop`, e.g. upstream `tb_axi_xbar`) scoreboard verdict
  lines ("Simulation has ended!", "Tests Failed: 0") commonly print well
  above the old 2-line `PLAIN_MARK` summary window and matched none of
  `KEY_LINE_RE` — registered evidence's `## Key check lines` section came up
  empty even though the underlying two-leg verdict was sound. Widened the
  plain-VCS summary window (`idx - 2` → `idx - 20`) and added `tests
  failed`/`ended`/`mismatch` to `KEY_LINE_RE`. New kernel test
  `test_plain_nonuvm_verdict_line_captured` (`kernel/tests/test_evidence.py`
  + a `PLAIN_NONUVM_VERDICT_LOG` fixture) pins the regression (FB-6, closes
  FB-3's open question as a side effect: the native `-assert verbose`
  `Summary:` line was already confirmed present for this tb shape, it was
  just outside the old window too).
- **`agents/de.copilot.md`**: DE now sets bug status **FIXING** (not
  FIX_READY) at delivery — the fix-commit column and FIX_READY don't exist
  yet at DE's delivery time (orch hasn't committed), so the old wording
  tripped `docs-check`'s FIX_READY-needs-fix_commit gate every time.
  FIX_READY is now explicitly orch's to set once the commit hash is known
  (FB-5).
- **`taxonomy/failure_taxonomy.md`**: added an explicit "registration is
  unconditional" sentence — a taxonomy-class anomaly gets a `doc/bugs.md`
  row regardless of whether it blocked evidence, was fixed inline in the
  same card, or looked like "just" a tool quirk.
  **`agents/{arch,de,dv,rev}.copilot.md`**: each delivery-report format now
  carries a mandatory "taxonomy-class anomaly hit this card (including
  worked-around-inline ones): yes/no + BUG-ID" field, closing the gap where
  only DV's "on a mismatch" case and DE/arch's self-encountered-ambiguity
  case were covered (FB-7).
- **`docs/adoption.md`**: playbook 1 documents the move-aside workaround for
  `--init`'s (deliberate — see `docs/deferred.md`) rejection of a target dir
  that already has a few bootstrap files (`LICENSE`/`README`/
  `.claude/settings.local.json`) in it (FB-1); and notes that Claude Code's
  `.claude/agents/` type registration lags `--init` by a short delay, so the
  first arch/de/dv/rev dispatch right after init may need a session restart
  or a short wait (FB-4).
- **`make/vcs-2018.mk`**: the `LM_LICENSE_FILE` fallback comment now states
  plainly that it is a placeholder that MUST be overridden per-environment,
  not a value expected to work as-is (FB-2).
- FB-3 (whether `-assert verbose`'s native `Summary:` line appears for ucli
  `run;exit`-driven `$stop` tb) closed via FB-6: downstream confirmed it
  does appear — the gap was evidence.py's window/regex, not the tool
  option. No separate change.

## 0.2.0 — 2026-07-27

Canonical copilot agent suite + the SVA-verdict lessons absorbed from
ppa-lite-copilot 0.4.0 → 0.5.8.

- **Copilot suite canonicalized** (graduated early from deferred.md by user
  ruling: one `rev` cannot run a pure-agent workflow):
  `agents/{arch,de,dv,rev}.copilot.md` rendered into project
  `.claude/agents/` by `fwsync --pull`/`--init`; `skills/`
  (handover/evidence/closeout for both profiles, `dispatch` — the orch
  card manual — copilot-only) vendored hash-pinned into
  `.claude/skills/`; `templates/CLAUDE.project.{learning,copilot}.md`
  split with hard isolation rules on the copilot side.
- **SVA leg of the log verdict** (`kernel/svacheck.py`, ppa BUG-014 with
  the BUG-017/018 adversarial hardenings): assertion failures never
  increment UVM_ERROR, so `evidence.py`/`regress.py` now judge two legs —
  engine failure lines / severity lines / native `-assert verbose` Summary
  counts / optional registered baseline floor (`sva_baseline`,
  fail-closed once configured, catches `$assertoff` and dropped-sva-file
  bypasses). New `iverif.json` keys: `sva_enforce` (default true),
  `sva_baseline`. `make/vcs-2018.mk` pins `SIM_OPTS_2018 := -assert
  verbose` into the run pattern.
- Evidence excerpts now archive the native SVA Summary lines (independently
  re-judgeable) and anchor test identity via the `Running test` line
  (ppa BUG-017 R7: high-verbosity-only checks left the key-line section
  empty). `regress.py` reports per-entry failure reasons with a stable
  first-column token set.
- xverif probing protocol corrected everywhere (ppa BUG-016 era lesson):
  NOT on PATH — `$XVERIF_ROOT/tools/` (exported by `vcs-2018.mk`,
  default `/home/open_tools/xverif`), `export VERDI_HOME` first, probe
  with `test -x`, never `command -v`.
- Adoption playbooks updated: config-first ordering (the pull reads
  `iverif.json` to pick vendor set + agent suite), floo `sva_enforce:
  false` until its flow adopts `-assert verbose`, ppa carries its baseline
  file over unchanged.
- Tests: 38 → 46 (SVA quadrants incl. the BUG-014 fuse, copilot init
  renders the full suite, learning init excludes the dispatch manual).

## 0.1.0 — 2026-07-19

Initial usable skeleton.

- Reference layer: `schema/`, `taxonomy/`, `dispatch/`, `signoff/`, `agents/`.
- Canonical script kernel (`kernel/`): `docs.py`, `evidence.py`, `bump.py`,
  `regress.py`, `fwsync.py` — ported from ppa-lite-copilot / floo_axi_chimney,
  parametrized via `iverif.json`, all known fixes folded in (incl. the
  milestone-signoff `any(generator)` bug that had drifted back into
  floo_axi_chimney).
- Kernel regression tests (`kernel/tests/`) + framework CI.
- Drift control: `kernel.manifest.json` + `fwsync --check` hash verification.
- Project scaffolding: `fwsync --init`, `make/` includes, `templates/`.
