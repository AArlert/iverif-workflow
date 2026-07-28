# Deferred mechanisms

Rule: **no infrastructure ahead of pain.** Every mechanism below is deliberately *not* built yet. Each has a
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
| Chain audit (`docs.py --chain-audit`): whole-graph break-link check over spec clauses → testplan scenarios → checkers/SVA → coverage → evidence — flags spec clauses no scenario cites, scenarios naming no checker, checkers with no coverage point, coverage claims with no evidence record. Subsumes promoting `spec_ref` / `coverage_delta` from convention to hard validation (external review 2026-07-26 rec 1: `make chain` shows one scenario's links; nothing yet hunts broken ones) | the first coverage-driven milestone signoff (imminent: pulp_axi_xbar_copilot M2 is running the ecosystem's first functional-coverage campaign, F-M2-08) |
| `coverage_delta` auto-capture — carrier revised to parsing the URG text report (`urg` ships with VCS O-2018), **not** the xcov API: empirical finding (pulp_axi_xbar_copilot BUG-0017 `## scope`, 2026-07-28) is that this VM's Verdi 2018 pynpi has no `cov` submodule at all (files absent, not an export issue) — the xverif version wall blocks exactly the coverage dimension while xbit/xsva/xloc/xentry/xdebug all work. Functional-coverage numbers already reach evidence via the `[FCOV_SUMMARY]` canon lines (0.3.3); URG parsing would add the code/assert-coverage dimensions | same trigger as above |
| Dedicated `rca` agent | the same failure class recurring after its FL record said it was guarded. **Trigger fired 2026-07-28** (pulp BUG-0015's guard named `stall_sva.sv` as next victim; defect landed there untouched) — but the pain shape was guard *consumption*, not analysis: built as `docs.py --guards` injection (0.4.1) instead. Row stays for the analysis-shaped recurrence |
| Gate self-attestation ("no proof-of-execution, no gate-pass"): gates emit a source-fingerprint stamp + execution-evidence marker, verified at the `make evidence` choke point (`sva_enforce`-style switch, default on for new repos) | pulp BUG-0022 fired the pain (incremental compile → empty lint log → false green); canon mechanism waits for pulp's project-side prototype (its FB-10) to flow back with measurements |
| Presentation layer: mechanical number injection for report/README/defense materials + consistency gate (`report.py`-style, see ppa-lite-copilot 0.5.x R-line) | the first presentation/portfolio material line in any repo (numbers hand-copied into a document = the pain) |
| `sva_baseline` scaffolding (`make sva-baseline` registers the current floor after rev approval) | the second project to register a baseline by hand |
| Learning-line per-scenario review gate (✅ additionally requires a review reference) | a milestone spot-check finds unreviewed code already marked ✅, twice |
| `fwsync --init --allow-existing`: seed into a target that already holds bootstrap files, by an explicit keep/overwrite whitelist rather than a guess | the second repo to hit it (pulp_axi_xbar_copilot hit it once — 2026-07-27, FB-1: host pre-seeded `LICENSE`/`README`/`.claude/settings.local.json`; move-aside workaround is documented in `docs/adoption.md`). Sooner if a repo host makes an empty initial repo impossible to obtain |
| Risk-graded card paths — L0 docs/build · L1 TB/sequence/coverage · L2 RTL/SVA/scoreboard · L3 signoff/waiver/spec — letting low-risk cards skip parts of the full chain (external review 2026-07-26 rec 4; note the per-card-type dispatch matrix in `skills/dispatch/` already *is* a graded path — a DE fix card never passes through arch, and the implemented rules already approximate L0–L3: no arch/rev is forced on doc/build fixes) | process overhead visibly exceeding the work itself on a low-risk card, recorded twice — the dispatch collection check now *prompts* the recording, so this trigger has an observer (it previously had none: overhead inversion turns nothing red — same failure shape as FB-10's unconsumed guards) |
| `make env-check` preflight: license server reachable, tool homes exist, disk headroom, xverif probe — catch environment faults *before* a sim run instead of as misattributed failures (external review 2026-07-26 risk 7; the TOOL_ENV taxonomy class already separates them after the fact, first in the diagnosis cost order) | the second session blocked by environment rather than DUT/TB (first: FB-2's license-placeholder confusion, 2026-07-27) |
| Symptom-fingerprint fields in the FL schema (assertion name / UVM component / first-anomaly signal / tool error code) + fingerprint-based retrieval, upgrading dispatch Q1's grep (external review 2026-07-26 rec 5 — the Verdi-RDA direction) | the first time grep retrieval misses an existing same-class FL that later surfaces; at today's scale (15 FLs in the largest repo) grep suffices |
| Formal evidence record: schema for property / assumptions / bound-or-proof result / tool+version / replay command, entering the signoff rubric beside sim evidence (external review 2026-07-26 rec 6 — for an AXI xbar, fairness and deadlock-freedom are sim-hostile properties) | the first real formal run in any project repo (today: none, and no formal tool confirmed on the VM) |
| Tool-capability profiles: a second `make/<tool>-<version>.mk` beside `vcs-2018.mk` under a shared variable contract (external review 2026-07-26 risk 6: don't accumulate exceptions in one fragment) | the second tool/version needing its own workaround set — one 88-line fragment *named by its version* is the profile until then |

## Graduated (formerly deferred, now built)

| Mechanism | Shipped | Trigger note |
|---|---|---|
| Canonical copilot agent suite (`agents/*.copilot.md` + `skills/` incl. the dispatch-card manual) | 0.2.0 | Trigger revised by user ruling (2026-07-27), ahead of the original "pulp_axi_xbar_agent creation": with only `rev` canonical, a `--init --profile copilot` repo could not run the pure-agent workflow at all — the framework was not the single source of truth for half its own contract. Ported from ppa-lite-copilot at 0.5.8 (includes its BUG-014/016/017 lessons). |
| SVA assertion leg of the log verdict (`kernel/svacheck.py`, two-leg judge in evidence/regress) | 0.2.0 | Trigger fired in ppa-lite-copilot as BUG-014 (assertion failures invisible to UVM_ERROR); absorbed with the BUG-017/018 adversarial hardenings. |
