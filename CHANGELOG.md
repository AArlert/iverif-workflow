# Changelog

All framework changes land here. Project repos decide when to `fwsync --pull`
based on this file; the version they carry is recorded in their `iverif.json`.

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
