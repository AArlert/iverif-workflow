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
| Dedicated `rca` agent | the same failure class recurring after its FL record said it was guarded |
| Presentation layer: mechanical number injection for report/README/defense materials + consistency gate (`report.py`-style, see ppa-lite-copilot 0.5.x R-line) | the first presentation/portfolio material line in any repo (numbers hand-copied into a document = the pain) |
| `sva_baseline` scaffolding (`make sva-baseline` registers the current floor after rev approval) | the second project to register a baseline by hand |
| Learning-line per-scenario review gate (✅ additionally requires a review reference) | a milestone spot-check finds unreviewed code already marked ✅, twice |

## Graduated (formerly deferred, now built)

| Mechanism | Shipped | Trigger note |
|---|---|---|
| Canonical copilot agent suite (`agents/*.copilot.md` + `skills/` incl. the dispatch-card manual) | 0.2.0 | Trigger revised by user ruling (2026-07-27), ahead of the original "pulp_axi_xbar_agent creation": with only `rev` canonical, a `--init --profile copilot` repo could not run the pure-agent workflow at all — the framework was not the single source of truth for half its own contract. Ported from ppa-lite-copilot at 0.5.8 (includes its BUG-014/016/017 lessons). |
| SVA assertion leg of the log verdict (`kernel/svacheck.py`, two-leg judge in evidence/regress) | 0.2.0 | Trigger fired in ppa-lite-copilot as BUG-014 (assertion failures invisible to UVM_ERROR); absorbed with the BUG-017/018 adversarial hardenings. |
