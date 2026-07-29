# Design notes (canon-only — never shipped, never pinned into projects)

Genealogy, adaptation records, and the anti-bloat ledger for iverif-workflow.
Nothing in this file is operative: it explains *why* the shape is what it is,
not what the shape currently is. Safe to delete after cloning if you don't
care about the history.

## Release tags backfilled v0.3.1..v0.6.1 (2026-07-29)

The release ritual (edit → `make selftest` → `make manifest` → bump
`VERSION` + `CHANGELOG.md` → commit + tag) mandates a tag per release, but
tagging silently stopped after v0.3.0 — the 17 releases of the rapid
0.3.1–0.6.1 cadence (two days) got commits only; v0.7.0 resumed tagging.
Adjudicated **backfill** over amending the ritual: 0.7.0's upgrade note
tells adopters to pull tags, so the gap is adopter-facing, not cosmetic.
Disposition:

- One annotated tag per CHANGELOG version, on that version's bump commit
  (the commit carrying the version in its subject — e.g. v0.6.1 =
  `87e2eef`, not the later 0.7.0-C1/C2 commits that still read
  `VERSION=0.6.1`).
- Tagger dates set to the tagged commit's date so tag chronology matches
  release chronology; every message carries a "Retroactive tag, backfilled
  2026-07-29" trailer — backdating is disclosed, not disguised.
- All 17 pushed to origin. The ritual text stands unchanged; the rule
  going forward is the tag is part of the release commit's push, not a
  separate later step.

## 0.7.0 structural refactor: the layout is the mental model

Origin: the author reported being unable to rebuild the framework in their
head — conceptual drift, the same disease fw-check kills at file level, one
level up. Adjudications:

- **loop-strip is the one mapping rule**: canon `loop/<p>` ships as
  `workflow/<p>`; the canon directory that defines the machine IS the
  project's workflow tree. Named exceptions only: `CONSTITUTION.md` →
  `workflow/constitution.md` (unconditional, fail-closed) and per-profile
  `profile.*` selection.
- **`fail/` unifies the failure branch**: the old `schema/` + `taxonomy/` +
  `dispatch/` split grouped docs by *genre*; a reader had to know the genre
  taxonomy before finding the failure loop. One directory per branch of the
  machine beats one per document kind.
- **`review/` (station name) over `signoff/`**: the station is rev's
  independent review; milestone signoff is one of its tasks. The old
  canon-level `review/` (external audits) moved to `governance/reviews/`.
- **Numbered station dirs rejected**: sparse stubs for stations 3/6 would
  be infrastructure without content; the loop's order lives in the
  constitution's diagram, not in directory names.
- **Invariants' canonical shipped home moved README → CONSTITUTION.md**
  (discipline.md's "(README)" pointer was a dead ref in every project copy).
- **Uniform +200B budget raise**: the mandatory provenance header
  (Canonical/Axioms/Consumer, checked by `test_constitution`) is contract,
  not prose growth; one reviewed table-wide raise beats 24 per-row notes.
- **Axiom vocabulary is closed** (five names, English in headers, bilingual
  in the constitution): an unknown axiom in a header fails the gate — a
  genuinely new axiom is a constitution amendment first.

## Evidence records: log excerpts, not the design doc's EV-xxxx.yaml

The founding design doc sketched YAML evidence records. The canon keeps the
doc's intent — machine-readable, spec-traceable, replayable — but the
carrier is a log excerpt: already proven in two projects, needs no YAML
parser (kernel is stdlib-only), and is itself the anti-forgery anchor (an
excerpt of a log that never existed is much harder to fake plausibly than a
YAML file). Structured fields ride in `#` header comments.

## Testplan: markdown table, not the design doc's YAML frontmatter

The design doc proposed per-scenario YAML frontmatter
(`status: evidence_collected`, `evidence: [EV-0042]`). The canon keeps the
proven markdown table: same machine-readability (`parse_table()`), one file
to scan for a human. The `planned → asset_ready → evidence_collected →
signed_off` ladder maps onto `🔲/⚠️ → ❌/✅` plus the milestone signoff
record.

## Copilot roles: mapping to the original design doc

The design doc (`icverifagentsframework.md`) names five copilot agents:
planner / coder / runner / rca / rev. The battle-tested implementation in
ppa-lite-copilot used different seams; the canon adopted the implemented
set:

| Design-doc role | Canonical implementation |
|---|---|
| planner | orch + `make next` (most "planning" is derivable from testplan state) |
| coder | arch (design prompts) + de (RTL) + dv (TB) |
| runner | the mechanical layer (`make run` / `make evidence` / `regress.py`) |
| rca | dv + `dispatch/` tables; dedicated rca agent deferred (deferred.md) |
| rev | rev — the only role with signoff authority |

## Article-origin vocabulary purged from operative docs (0.4.4)

The repo bootstrapped from an external evidence-chain article whose
five-role cast (planner / coder / runner / rca / rev) predates the
implemented seams (orch + arch/de/dv/rev + the mechanical layer). 0.4.4
removed the last operative references: dispatch-card copilot columns still
commanded a "rca agent"/"runner"/"planner", roles no downstream repo has;
deferred.md cited the article ("founding design doc §10") as rule
authority. Adjudicated **kept**: `rca` as the FL section / template name —
root-cause analysis is industry vocabulary, not the article's coinage, and
renaming would churn every downstream FL archive for zero clarity gain.
Rule going forward: operative docs use only implemented concepts; borrowed
genealogy lives here.

## Profiles: split into per-profile contracts (0.4.0)

`docs/profiles.md` (both contracts + comparison in one pinned file) was
split into `docs/profile.{learning,copilot}.md`; a project receives only its
own contract as `workflow/profile.md`, selected by the sync parameter —
file-level separation over an in-file marker DSL (user ruling 2026-07-28).
Canon-side comparison stays in README §Two profiles.

## Deferred mechanisms (historical, 0.7.x)

`governance/deferred.md` kept a "no infrastructure ahead of pain" ledger of
roughly fifteen mechanisms deliberately left unbuilt, each gated on a named
trigger — guided `status.jsonl`/`log.md` entry prompts, scenario
scaffolding, a `regress.list` auto-generator, FL guard-verify re-injection,
promoting `spec_ref` headers to a hard docs-check, `coverage_delta` via URG
parsing, a dedicated `rca` agent, gate self-attestation proof properties, a
presentation-layer number-injection script, `sva_baseline` scaffolding, a
learning-line review gate, `fwsync --allow-existing`, an `env-check`
preflight, symptom-fingerprint FL fields, a formal-evidence record schema,
and per-tool capability profiles. Most of these triggers never fired before
0.8.0 retired the whole "pending mechanisms ledger" genre outright — the
few that did fire before retirement are the ones worth keeping, captured
below.

## Graduated (formerly deferred, now built)

| Mechanism | Shipped | Trigger note |
|---|---|---|
| Canonical copilot agent suite (`harness/agents/*.copilot.md` + `harness/skills/` incl. the dispatch-card manual) | 0.2.0 | Trigger revised by user ruling (2026-07-27), ahead of the original "pulp_axi_xbar_agent creation": with only `rev` canonical, a `--init --profile copilot` repo could not run the pure-agent workflow at all — the framework was not the single source of truth for half its own contract. Ported from ppa-lite-copilot at 0.5.8 (includes its BUG-014/016/017 lessons). |
| SVA assertion leg of the log verdict (`kernel/svacheck.py`, two-leg judge in evidence/regress) | 0.2.0 | Trigger fired in ppa-lite-copilot as BUG-014 (assertion failures invisible to UVM_ERROR); absorbed with the BUG-017/018 adversarial hardenings. |
| Chain audit (`docs.py --chain-audit` / `make chain-audit`): break-link report over spec ↔ testplan ↔ feature-matrix ↔ evidence; hard-fail limited to dangling spec refs, everything else reported | 0.6.0 | Trigger fired 2026-07-28: pulp M2, the ecosystem's first coverage-driven milestone signoff. First real run on its docs: 0 dangling, 5 parent-anchored refs, and §5.2.6 (added that very day by REV-011) correctly flagged as cited-by-no-scenario. |
| Risk-graded card paths L0–L3 (grade table + per-card grade line in `harness/skills/dispatch/`, collection check records grade-vs-reality mismatches) | 0.7.1 | Trigger ("overhead inversion recorded twice") overridden by user ruling 2026-07-29: **the 0.4.6 observer was structurally blind** — every subagent sees only its own card, chain weight is visible only to orch, and orch does not hurt; zero recordings ≠ zero weight. Shipped ahead of pain so the adopter walk-through *generates* the mismatch data the trigger was waiting for. |
| Spec-gap explorer (`docs.py --explore` / `make explore`: uncited-section frontier as candidate rows; `--next` planning-time nag while the current milestone has zero rows; arch spec-gap card type) | 0.7.1 | Same 2026-07-29 ruling. Grew out of chain-audit's uncited-sections line (0.6.1) — the audit *showed* the frontier at signoff, nothing *consumed* it at planning time (the FB-21 shape, one level up). Proposal authority stays semantic: arch proposes, rev gates; declining a section is a recorded narrowing. |

## 0.7.x axiom system (retired, historical only)

The five invariants themselves now live directly in the project-root
`CLAUDE.md` (0.8.0) — they are not duplicated here. What follows is the
0.7.x `CONSTITUTION.md` axiom table and mechanism index, kept only as a
record of how that generation of the framework organized its rules. Neither
table is operative: no gate reads it, and the doc paths in the mechanism
index (`workflow/*`, `.claude/skills/*`) reference the pre-0.8.0 layout.

### Axioms (0.7.x)

| # | Axiom | 中文 | The rule |
|---|---|---|---|
| 0 | self-application | 自反 | The axioms below bind the rules, the tools, and this page itself. |
| 1 | independence | 独立 | A claim counts only with evidence independent of the claimant. |
| 2 | recording | 落盘 | What is not written into the repo does not exist — intent included. |
| 3 | consumption | 消费 | A mechanism nobody reads does not exist; a trigger nobody observes never fires. |
| 4 | pain-gating | 痛点 | No infrastructure ahead of pain; everything built pays a byte budget. |

Theorems: narrowing must be declared (waiver / divergence) · diagnose in
cost order (TOOL_ENV → TB/CONSTRAINT → SPEC → DUT) · correct out of the box.

### Mechanism index (0.7.x)

| Doc (project path) | Axioms | Consumer |
|---|---|---|
| workflow/constitution.md | 0 | session start; test_constitution |
| workflow/discipline.md | 2,4 | every role, before first edit |
| workflow/profile.md | 1 | orch/human at session start; fwsync selects it |
| workflow/testplan_entry.md | 2 | docs-check; make next; dv cards |
| workflow/evidence_record.md | 1,2 | evidence.py; docs-check; rev |
| workflow/review/six_questions.md | 1 | rev, in every review |
| workflow/review/rubric.md | 1,3 | rev at signoff; docs.py --signoff |
| workflow/fail/failure_record.md | 2 | docs-check; make guards; dispatch Q1 grep |
| workflow/fail/failure_taxonomy.md | 2 | every FL taxonomy section; dispatch |
| workflow/fail/rca_template.md | 2 | FL rca authors; rev |
| workflow/fail/assertion_failure.md | 1,2 | dv/human when an assertion fires |
| workflow/fail/regression_failure.md | 2 | orch/human when regress FAILs |
| workflow/fail/coverage_hole.md | 2 | dv/human during coverage closure |
| .claude/skills/handover/SKILL.md | 2 | session start |
| .claude/skills/evidence/SKILL.md | 1,2 | before any ✅ or CLOSED |
| .claude/skills/closeout/SKILL.md | 2 | end of every work cycle |
| .claude/skills/dispatch/SKILL.md | 1,3 | orch, before every card |
| .claude/agents/ (rendered on pull) | 1 | Claude Code role dispatch |
| CLAUDE.md (rendered at init) | 0 | every session |
</content>
