# Deferred mechanisms

Rule (from the founding design doc, §10): **no infrastructure ahead of
pain.** Every mechanism below is deliberately *not* built yet. Each has a
concrete trigger — the first real occurrence of its pain point in a project
repo. When a trigger fires, build the mechanism **here** (never in the
project repo), add a kernel test, bump the version, and let projects pull.

Keeping this ledger in the repo makes the discipline itself reviewable: if a
mechanism appears in `kernel/` without its trigger having fired, that is a
process bug.

| Deferred mechanism | Trigger (first real occurrence of…) |
|---|---|
| `docs.py --log-entry`: guided prompts that write the `status.jsonl` line and `log.md` block for you (no hand-written JSON) | a learner blocked by `docs-check` over JSON syntax in `status.jsonl` |
| Scenario scaffolding: one command registers a testplan row + feature-matrix link | ghost-reference FAILs (testplan ↔ feature-matrix mismatch) accumulated ≥ 2 times |
| `docs.py --spec-change`: change-record entry + re-pin in one step | someone forgets the 3-step spec dance and gets gate-blocked |
| `regress.list` auto-generation from testplan replay columns | a ✅ scenario found missing from the regression list |
| `make fl` failure-record scaffold + `make guard-verify` (re-inject the original defect, prove the guard fires) | the first FL record with a `regression_guard` lands |
| `spec_ref` / `coverage_delta` header fields promoted from convention to hard `docs-check` validation | the first coverage-driven milestone signoff |
| `coverage_delta` auto-capture via `xcov` (xverif toolkit) | same trigger as above, if xcov output proves stable on the VM's Verdi 2018 |
| Canonical copilot agent suite (arch/de/dv skills + dispatch cards) promoted from ppa-lite-copilot into `agents/` | pulp_axi_xbar_agent repo creation |
| Dedicated `rca` agent | the same failure class recurring after its FL record said it was guarded |
| Learning-line per-scenario review gate (✅ additionally requires a review reference) | a milestone spot-check finds unreviewed code already marked ✅, twice |

## Graduated (formerly deferred, now built)

*(empty — move rows here when their trigger fires and the mechanism ships,
with the framework version that shipped it)*
