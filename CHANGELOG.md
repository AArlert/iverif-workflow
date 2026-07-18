# Changelog

All framework changes land here. Project repos decide when to `fwsync --pull`
based on this file; the version they carry is recorded in their `iverif.json`.

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
