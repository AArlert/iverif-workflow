# Changelog

All framework changes land here. From 0.8.0 on there is no sync tool — a
clone tracks its own history and pulls upstream commits by `git
cherry-pick` when it wants them.

## 0.8.0 — 2026-07-29

**Distillation.** 0.7.x guarded 24 scattered contracts (constitution +
axiom layer + mechanism index, per-profile docs, a rendering pipeline, a
hash-pin/manifest/three-drift-state sync tool) with a state machine built to
keep them from drifting. 0.8.0 answers the same problem a cheaper way:
shrink the framework surface to a size a person can hold in their head, and
let git's own history replace the state machine. User ruling — full design
rationale and the audit trail behind every cut in `DESIGN.md`.

- **Repo is the template.** `git clone` + rename is now the entire
  onboarding story; `doc/`, `design-prompt/`, `rtl/`, `tb/`, `sim/` ship as
  empty shells. `CLAUDE.md` (one page: five invariants, the loop, the make
  table, dispatch grading) is the only required read.
- **24 contracts → 4.** `loop/` (13 files: taxonomy, failure record, rca
  template, three dispatch tables, evidence/testplan contracts, six
  questions, rubric, discipline, two profiles) merges into
  `workflow/{discipline,bugs,records,review}.md`. The two profiles
  (learning/copilot) retire — who executes a card is a field on the card,
  not two parallel doc trees.
- **`kernel/` → `scripts/`.** `fwsync.py` (init/pull/render/manifest/
  divergence) and `regress.py` are deleted outright; regress's judgment
  logic survives as `svacheck.py --judge <log>` (the shared one-log,
  two-leg primitive), its loop logic as a reference-pattern comment in
  `scripts/make/vcs-2018.mk` — canon owns the judgment, projects own the
  loop.
- **`chain` / `chain-audit` / `signoff-check` → one `check` command**,
  narrowed by `SCEN=`/`MILESTONE=`. New invariant 5 ("no kill, no trust")
  gets a machine backing: `make check MILESTONE=<n>` now also requires at
  least one `KILL` row in `doc/bugs.md` tagged to that milestone.
- **`harness/` (agent-card + skill rendering) → 5 static `.claude/agents/`
  cards** (`orch` new; `arch`/`de`/`dv`/`rev` un-rendered from their
  `.copilot.md` sources), no rendering step.
- **`CONSTITUTION.md` retires**: its four invariants (now five) live
  directly in `CLAUDE.md`; the axiom table and mechanism index survive only
  as history in `DESIGN.md`.
- **`governance/` folds into one root `DESIGN.md`** (canon-only, safe to
  delete after cloning); `governance/reviews/` moves to root `reviews/`
  unchanged.
- `make commit` replaces `make git` — add+commit only, never push; `git
  push` stays a separate, manual, human action.
- `scripts/tests/test_budgets.py` drops its 24-row per-file byte table for
  one aggregate cap over `CLAUDE.md` + `workflow/`'s 4 files;
  `test_constitution.py` and `test_fwsync.py` are deleted (they tested
  machinery this release removes).

## 0.7.1 — 2026-07-29

Two deferred rows graduate **by user ruling**, ahead of their triggers,
to be stress-walked by the adopters. The ruling refutes 0.4.6's observer
design: *nobody complaining about process weight does not mean the
process is light — every subagent sees only its own card, chain weight
is visible only to orch, and orch does not hurt.* Zero recordings ≠
zero weight. Generating axioms: consumption (the frontier and the
overhead both get real observers), pain-gating (chain weight matched to
risk), recording (grade and mismatch land in records, not impressions).

- **Spec-gap explorer** (`docs.py --explore` / `make explore`): planning
  view of the chain-audit graph — uncited spec subsections listed with
  their heading titles as candidate testplan rows, sourceless scenarios
  flagged for anchoring. `--next` gains a planning-time nag (both
  profiles, `explore` phrase key) that fires only while the current
  milestone has **zero** registered rows and falls silent once planning
  exists — no permanent nag (the FB-19 skimming shape). New copilot card
  type: **arch spec-gap sweep** (must include the explore list verbatim;
  must not include orch's scenario ideas); arch converts gaps into
  proposed rows or written per-section declines — a decline is a
  narrowing, rev gates either way. Chain-audit unchanged (shared
  `chain_gaps()` computation).
- **L0–L3 risk grades** (dispatch manual): L0 docs/build · L1
  TB/sequence/coverage · L2 RTL/SVA/scoreboard · L3
  spec/waiver/signoff. The grade table absorbs the old model-tier list;
  grades tune the *chain* only — taxonomy registration and evidence
  gates stay unconditional at every grade; in doubt, grade up. Every
  card states its grade; the collection check records grade-vs-reality
  mismatches **per card** (the structurally sighted observer the 0.4.6
  design lacked). The adopter walk-through is expected to generate
  exactly this mismatch data — that is the point of shipping early.
- Budgets: dispatch SKILL cap 4300 → 4900 (reviewed: grade table +
  card row + observer are operative contract). Tests: 79 → 82.

## 0.7.0 — 2026-07-29

**Structural refactor: the layout is the mental model.** Origin: the
author could no longer rebuild the framework in their head — conceptual
drift, the disease fw-check kills at file level, one level up. Generating
axioms (a convention this entry inaugurates): self-application (the repo
now passes its own gates on its own shape), recording (the mental model is
written down and shipped), consumption (every shipped doc must name its
consumer — test-enforced).

- **`CONSTITUTION.md`** (new, ships as `workflow/constitution.md`,
  4800-byte hard cap): five axioms (self-application 自反 · independence
  独立 · recording 落盘 · consumption 消费 · pain-gating 痛点), the one
  machine loop, the four core invariants' canonical home (moved from
  README), and the mechanism index (doc · axioms · consumer). Read order
  in every project is now constitution → discipline → profile.
- **Canon re-laid so `ls` shows the model**: contracts under `loop/`
  (≡ project `workflow/`, one strip-prefix mapping rule; `review/` =
  the review station, `fail/` = the whole failure branch — old
  `schema/` + `taxonomy/` + `dispatch/` genre dirs dissolved);
  Claude-coupled render sources under `harness/`; canon-only
  self-application layer under `governance/` (deferred ledger,
  design-notes, adoption, external reviews).
- **Unified provenance header** on all 29 shipped docs:
  `Canonical: <path> — pinned snapshot. Axioms: <…>. Consumer: <…>.`
  New gate `kernel/tests/test_constitution.py`: header well-formed,
  axiom names ⊆ the five, consumer non-empty, and the constitution's
  index covers the snapshot. Budgets +200B table-wide (reviewed: header
  tax, not prose growth).
- **fwsync**: single mapping rule replaces `SNAPSHOT_REF_DIRS`;
  completeness probe additionally requires `workflow/constitution.md`
  (fail-closed against pre-0.7.0 pulls); orphan sweep now also drops
  directories it emptied. New fuse: `test_pull_migrates_old_layout`
  pins the exact 0.6.x → 0.7.0 adopter experience.
- Cross-reference convention: shipped docs cite snapshot paths
  (`workflow/…`, `scripts/…`); canon-only docs cite canon paths. Three
  pre-existing dangling refs fixed in passing (`config/presets/
  columns.zh.json`, `templates/CLAUDE.project.md` header, discipline's
  "(README)" invariant pointer — dead in every project copy).
- **What adopters see on `make fw-pull`**: `workflow/` re-lays
  (schema|signoff|taxonomy|dispatch → top level + `review/` + `fail/`),
  `workflow/constitution.md` appears; pristine old-path files are swept
  automatically, locally-edited ones only warn — re-apply on the new
  path, delete the old file, re-key `scripts/iverif.divergence.json`
  entries. `.claude/agents/` regenerates as always; **CLAUDE.md does
  not** — hand-migrate its three framework-owned paths
  (`workflow/schema/testplan_entry.md` → `workflow/testplan_entry.md`,
  `workflow/dispatch/*.md` → `workflow/fail/*.md`,
  `workflow/schema/failure_record.md` → `workflow/fail/failure_record.md`)
  and add the constitution read-first line, or diff against the 0.7.0
  template. `next_phrases_override` values naming `workflow/dispatch/`
  need the same rename. Pre-0.4.2 snapshots (no bootstrap hop): pull
  once via the framework clone directly.
- Tests: 75 → 79.

## 0.6.1 — 2026-07-28

FB-21 + FB-22 (pulp, third strike of the no-consumer family and a
violation of our own visible-truncation rule — both accepted).

- **chain-audit gets its consumer** (FB-21: born for signoff, invoked by
  nothing — wired exactly like the lint that stayed broken through
  M0/M1). Per their prescription "it must be *seen* at signoff, not
  *green*": `docs.py --signoff` now prints the full audit report inline
  (machine makes it unmissable), and rubric #8 requires a disposition or
  written acceptance per gap class (human must answer it); dangling refs
  are fixed, never accepted. Deliberately NOT a hard gate: 0/23 spec_ref
  adoption would turn a gate into exemption pressure.
- **Uncited-sections line: numeric sort, full print** (FB-22): string
  sort + silent `[:15]` cut exactly the highest-numbered chapters —
  §7.4.x/§8.x, the M3 territory, including the two sections §5.2.6
  cites as precedent. The one line that must never be cut, and the cut
  was invisible. Fuse added.
- Side observation (fw-feedback table not column-checked): declined for
  now — the check follows the gates, and no gate reads that table;
  becomes a deferred candidate when one does.
- Rubric budget raised (reviewed: #8 is new contract). Tests: 74 → 75.

## 0.6.0 — 2026-07-28

**Chain audit graduates from the deferred ledger** — its trigger (the
first coverage-driven milestone signoff) fired today with pulp's
signoff-M2.

- `docs.py --chain-audit` / `make chain-audit`: break-link report over
  spec ↔ testplan ↔ feature-matrix ↔ evidence. Spec section ids are
  resolved from headings and inline `§N.M` tokens (a literal-token match
  would have been 100% false positives — no adopter writes `SPEC-` in
  the spec body); refs may anchor at a parent section (reported, not
  failed). **Hard-fail is limited to dangling refs**; sourceless
  scenarios, matrix orphans, parent-only anchors, uncited subsections,
  and missing spec_ref headers are counted gaps — spec_ref adoption is
  0/23 in the field, so enforcement waits (new deferred row).
- First real run, on pulp's M2 docs: 0 dangling, 1 sourceless (the M0
  smoke), 5 parent-anchored refs, and §5.2.6 — the clause REV-011 added
  the same day — correctly flagged as cited by no scenario yet: the M3
  gap the audit exists to surface.
- Deferred: URG-parsing row re-scoped to "the first signoff that ships a
  URG report" (M2 was coverage-driven via FCOV lines alone).
  Tests: 72 → 74.

## 0.5.4 — 2026-07-28

FB-19 (pulp): the verbatim guard-injection rule was undefined for the
form "the card's FILES is the whole milestone" — their M2 signoff card
hit 22 guards / 413 lines, duplicating what rubric #5 already orders rev
to run live (the card is a snapshot, the ledger is alive; they drift).
The dispatch self-check gains the principled exception (their suggestion
①): when the criteria source itself orders the dispatchee to run the
same query, orch pastes no bodies — deterministic FILES list + the
command that computed it + hit index lines + a count self-check ("your
set differs → stop and report"). Same family as FB-16's CMD=:
self-execution proven beats a relayed snapshot. Functional cards stay
verbatim. Their meta-point recorded: wherever a rule leaves orch to
decide whether to follow the rule, that discretion is the gap — same
shape as FB-18(b). Budget raised (reviewed: new contract).

## 0.5.3 — 2026-07-28

FB-18 (pulp, blocking their M2 signoff card): 0.5.0's ACCEPTED@M<n>
missed rubric.md — the signoff card's criteria source and the tool gave
opposite verdicts on condition 3 (a criteria source that contradicts its
tool devalues every rubric-only item, especially #5's falsification).

- Machine condition 3 in `signoff/rubric.md` now reads "terminal or
  unexpired ACCEPTED@M<n>", matching the tool.
- **New human spot check #7** (the substantive half — FB-17's
  anti-rug-sweep promise was only half-delivered: expiry blocks, but
  nobody ever examined the rationale): each ACCEPTED row's cited REV
  record must state a *falsifiable* rationale (which fact, if refuted,
  voids the ruling); carry-overs re-arbitrated, never auto-extended.
  Isomorphic to #6, as FB-17 originally argued; reference shape:
  pulp REV-011 §5.4. `docs.py --signoff` prints it.
- Fuse: rubric and tool are pinned to agree on condition 3 and both
  carry #7. Rubric budget raised (reviewed: new contract). Tests: 71→72.

## 0.5.2 — 2026-07-28

pulp's FB-11 adversarial prototype refuted the 0.4.1-era candidate stamp
shape — adopted in full.

- **`make/vcs-2018.mk` ld-colon fix** (pulp BUG-0030, snapshot bug):
  `:$(LD_LIBRARY_PATH)` with the parent var empty left a trailing empty
  element and NPI-based tools (xdebug) refuse to initialize on it — any
  project calling them from a make environment inherited the trap. Now a
  conditional append; header workaround list documents it; make-fragment
  fuse test added (skips without `make`).
- **Gate self-attestation doctrine rewritten in the deferred ledger** from
  the prototype's two counterexamples (valid stamp ⇒ tool never ran on a
  file dropped from the flist; rerun + marker present ⇒ changed file
  parsed 0 times): the gate's product is **proof, not acceleration** —
  default is unconditional rerun + per-object execution proof; a stamp is
  admitted only when recheck is unaffordably expensive, and then property
  ④ (proof bound to an object enumeration independent of the tool input)
  is mandatory. Markers must be validated from real tool output — their
  own template example ("elaboration done") occurred 0 times in 15954
  lines. Canon carrier decided at the pattern's second adopter; pulp's
  sim/Makefile is the reference implementation. Tests: 70 → 71.

## 0.5.1 — 2026-07-28

Guard-injection presentation rule, from pulp's second field use (8 hits:
4 hard / 4 context, no skimming yet, projected skimming risk past ~10):
above ~6 hits the dispatch self-check now splits pasted guards into
**hard** (paths match files the card edits) and **context** (boundary
hits) — both verbatim; a boundary hit is help, not noise (their words:
one line of cost turned an ignorable edge into an answerable question).

## 0.5.0 — 2026-07-28

FB-16 + FB-17 (pulp): the framework's shape assumption "defects reproduce
in simulation" breaks for vendored-DUT + external-toolchain projects
(7/28 of pulp's bugs verify via compile/lint/tool output). Two mechanisms:

- **CMD-form evidence** (FB-16): `make evidence BUG=<ID> CMD='<cmd>'
  EXPECT='<regex>'` runs the re-verification command now — line 1 is
  `CMD: <command>` (the replay command), fail-closed twice (nonzero exit
  is never evidence; output with no matched signature is "no visible
  error", not "checked"). Sim path unchanged; docs-check accepts the
  CMD-form line 1.
- **`ACCEPTED@M<n>` bug state** (FB-17): analyzed + rev-signed rationale
  (docs-check requires a REV reference on the row) + scheduled. Signoff
  condition 3 passes unexpired accepted debt and blocks due-or-overdue
  debt; overdue rows fail docs-check; `--next` surfaces due debt in both
  profiles. Never terminal, never archived — WONTFIX may not mean
  "later", OPEN may not mean "decided" (their REV-004/REV-010 rulings,
  now representable instead of forced into a wrong terminal).
- Budget caps raised for the two schema files (reviewed: new operative
  contracts, not prose growth). Tests: 62 → 70.

## 0.4.6 — 2026-07-28

Risk-grading trigger gets an observer (user audit of review rec 4). The
deferred L0-L3 row's trigger ("overhead inversion recorded twice") had no
one instructed to record it — overhead turns nothing red, so it would
never fire; same failure shape as FB-10's unconsumed guards. One line in
the dispatch collection check now prompts the recording. The mechanism
itself stays deferred: the implemented per-card-type rules already
approximate L0-L3 (no arch/rev forced on doc/build fixes), and zero of
pulp's 15 FBs complain about process weight.

## 0.4.5 — 2026-07-28

FB-15 (pulp): `fix_commit` implied "the fix happened in this repo" —
external fixes (framework pulls, tool/VM upgrades) have no local sha, and
an environment upgrade produces no commit anywhere. The column now holds
any *traceable* fix reference — `<sha>` / `<repo>@<sha>` / `env: <change>`
— schema and gate wording updated; the check stays non-empty; the column
name stays (renaming = downstream churn, same adjudication as `rca`).

## 0.4.4 — 2026-07-28

Article-origin vocabulary purged from operative docs (user audit). The
bootstrap article's five-role cast (planner/coder/runner/rca/rev) still
leaked into instructions: dispatch-card copilot columns commanded a "rca
agent"/"runner"/"planner" — roles that do not exist in the implemented
suite; a downstream orch following them would dispatch cards to nobody.
Rewritten to implemented seams (orch / dv / `make run`). deferred.md no
longer cites the article as rule authority. Kept by adjudication: `rca` as
FL section/template name (industry vocabulary, downstream archives carry
it). The adjudication and the going-forward rule live in
`docs/design-notes.md`.

## 0.4.3 — 2026-07-28

FB-13 + FB-14 (pulp). FB-14 is the third sample of the "didn't run / data
corrupt, still green" family (FB-11 lint, FB-12 pull).

- **Table structure gate** (FB-14, blocking): docs-check fails any data
  row whose cell count differs from its header's (testplan /
  feature-matrix / bugs / waivers) — an unescaped `|` in a cell (RTL
  or-expressions) shifted columns and CLOSED-state checks could read the
  wrong cell. Schema now says: escape `|` as `\|`.
- **Key-line classification** (FB-13): `-assert verbose` per-assertion
  detail lines no longer eat the 30-line cap as an arbitrary prefix —
  aggregated per source file (`x_sva.sv: N properties/covers, A attempts,
  M match`), verdict lines keep the cap, truncation prints
  `... (K more key lines truncated)` instead of dropping silently.
- Tests: 60 → 62.

## 0.4.2 — 2026-07-28

FB-12 (pulp, blocking): a pull executed by the *pinned* fwsync applies the
old snapshot-pairing logic to the new framework — 0.3.0's copy looks for
`docs/profiles.md` (gone in 0.4.x), silently skips the profile contract,
writes a 25-file manifest, and fw-check passes on the incomplete manifest.
(The reporter's `--profile` attribution was coincidental — that flag only
feeds `--init` in every version; the second pull worked because it ran the
freshly pulled script.) Same failure family as FB-11: "didn't run" shown
as "passed". Four layers:

- **Bootstrap hop**: a project-side `--pull` now re-execs the framework's
  own fwsync — the pinned copy's pairing logic can never decide a pull
  again.
- **Fail-closed profile**: iverif.json present but profile invalid/missing
  → refuse the pull instead of degrading to the common set.
- **Orphan sweep**: previously-pinned files no longer in the set are
  deleted when pristine (reported when locally edited) — no more stale
  `workflow/profiles.md` surviving a set change.
- **fw-check completeness probe**: hash self-consistency cannot see an
  incompletely-written manifest; the profile contract's presence in the
  manifest is now itself checked.
- Schema (from pulp's backfill experience): `paths:` is the *note's
  scope*, not `ref:`'s location — the width beyond the birth file is the
  dangerous part. Tests: 57 → 60. Budget gate fired once during this
  change (failure_record.md +62B) and was answered by trimming, not by
  raising the cap.

## 0.4.1 — 2026-07-28

Guard injection — registered guards get a forced consumer (gap reported by
pulp_axi_xbar_copilot with a complete判例: BUG-0015's guard named its next
victim file in `## similar`; no mechanism carried it into the REV card that
reviewed exactly that file; the defect landed as predicted). Isolation
rightly blocks *reasoning* from crossing cards; constraints must cross as
*registered facts* — bugs.md was always the carrier, consumption was the
missing half.

- **`## regression_guard` gains `paths:`** (machine-matched globs); `ref:`
  stays the artifact anchor. Authoring rule: a checklist guard is a
  mechanization TODO, not a terminus.
- **`docs.py --guards <paths…>` / `make guards FILES=…`**: prints every
  guard whose globs match — pure path intersection, no interpretation, so
  orch stays non-technical and no common-mode channel opens.
- **Two consumption hooks**: dispatch self-check (matched blocks pasted
  into the card verbatim) and rubric #5 (every guard hit by the
  milestone's touched files is review scope; falsify ≥1 — replacing the
  1-of-N sample).
- Deferred: rca-agent row annotated (trigger fired; pain shape was
  consumption → built this instead); new row for gate self-attestation
  ("no proof-of-execution no gate-pass", pulp BUG-0022) awaiting pulp's
  FB-10 prototype measurements before the canon mechanism lands.
- Tests: 56 → 57 (the BUG-0015判例 as a fuse).

## 0.4.0 — 2026-07-28

Lean-and-turnkey overhaul. Governing principles (user ruling): effective ·
lean · clear · token-cheap, for this repo and every pinned snapshot.

- **Naming**: the framework snapshot is "pinned snapshot" everywhere;
  "vendor" now refers only to upstream DUT RTL (`templates/VENDOR.md` draws
  the line). fwsync internals renamed accordingly. Pinned-doc examples
  de-flavored (no DUT-specific names).
- **Profile contracts split**: `docs/profile.{learning,copilot}.md`, pinned
  as `workflow/profile.md` — a project receives only its own contract,
  selected at sync (file selection, no marker DSL). `docs/profiles.md`
  removed; genealogy sections moved to canon-only `docs/design-notes.md`,
  which never ships.
- **Diet**: xverif entry/probing rules live once (vcs-2018.mk header; six
  restatements became pointers); chronicle left the snapshot; README
  §Design principles now leads with the four principles + "write it as
  short as it can be"; discipline rule 2 gains the prose corollary.
  Same-basis reference-doc set: 34.9KB → 29.7KB.
- **Budget gate**: `kernel/tests/test_budgets.py` caps every shipped doc's
  bytes (~12% headroom); table coverage is itself tested. Raising a cap is
  a reviewed decision, not a fix.
- **Soft adaptation**: `framework_repo` in iverif.json (written by
  `--init`) → argument-free `make fw-pull`, and a fork becomes a
  first-class upstream. `scripts/iverif.divergence.json` declares local
  edits: fw-check lists them and passes (yellow); undeclared edits stay
  red. Fork playbook: `docs/adoption.md` §4.
- Tests: 52 → 56.

## 0.3.3 — 2026-07-28

User ruling on 0.3.2's design: **zero-config correctness beats config
hooks** — an adopting repo must be right out of the box, not after
discovering which `iverif.json` keys to patch. The two hooks stay, demoted
to escape hatches; the common cases move into canon.

- **`[FCOV_SUMMARY]` promoted to canon convention** (supersedes 0.3.2's
  wait-for-a-second-project stance): the tb prints one line per
  covergroup — `[FCOV_SUMMARY] <cg> samples=<n> inst_cov=<pct>` — and
  canon `KEY_LINE_RE` captures it with no project config.
  `schema/evidence_record.md` row 6 is the contract;
  `agents/dv.copilot.md` instructs the convention at authoring time.
  pulp_axi_xbar_copilot already prints exactly this tag — zero change on
  pull. The 0.3.2 fuse that pinned hook-only capture is deliberately
  flipped; the escape-hatch fuse now uses a neutral `[MYCOV]` tag.
- **`--next` deliverable-owner wording derives from delivery config**
  (FB-8 root fix): tb/-rooted `delivery.glob` → DV-owned deliverables,
  else DE; explicit `delivery.owner` ("de"/"dv", validated) overrides.
  The copilot `undelivered`/`prompt_missing` phrases are now
  role-parametric — a vendored-DUT repo gets "dispatch DV card" with
  zero config, no `next_phrases_override` needed.
- Tests: 50 → 52. `config/iverif_config.md` updated (both hooks
  re-labelled escape hatches, `delivery.owner` documented).

## 0.3.2 — 2026-07-28

Second-round feedback from `pulp_axi_xbar_copilot` (FB-8, FB-9 in its
`doc/fw-feedback.md`): two config hooks in the `columns_override` mold —
projects tune the vendored scripts' advisory wording and evidence
extraction via `iverif.json`, never by editing `scripts/`.

Folded ahead of the "collect the batch at wrap-up" plan of record
(`review/*.disposition.md`) because FB-9 is time-boxed: the fix must be
*available* before the adopter's M2 signoff, or the first coverage-driven
milestone's evidence permanently lacks its coverage numbers (the
no-retroactive-rewrite rule, cf. FB-6's surviving empty v0.0.1 records).
Landing it in canon touches nothing downstream — the pull remains the
project's own decision.

- **`next_phrases_override`** (FB-8): remap individual `--next` phrases
  whose role assumptions don't fit — the copilot `undelivered` default
  says "dispatch DE card", wrong for a vendored-DUT repo whose
  feature-matrix deliverables are DV-owned tb code. Unknown keys are a
  hard error (a typo'd override that silently no-ops would recreate the
  exact advisory drift FB-8 reports); values keep the original
  `%(...)s` placeholders. `kernel/docs.py` + `kernel/iverif_config.py`.
- **`key_line_extra`** (FB-9): extra project-side regexes for evidence
  key-line extraction. Canon `KEY_LINE_RE` stays generic on purpose —
  project-invented tags (pulp's `[FCOV_SUMMARY]` functional-coverage
  lines) ride the hook, so coverage numbers land in the excerpt and the
  evidence stays a self-sufficient reviewable artifact. Invalid regexes
  are a hard registration-time error. `kernel/evidence.py`. If a second
  project independently invents a coverage-summary tag, promoting a
  shared convention into canon becomes a deferred-ledger candidate.
- Tests: 48 → 50, one fuse per hook. The FB-9 fuse also pins the
  negative: without the hook, `[FCOV_SUMMARY]` must NOT appear in the
  excerpt — canon staying generic is itself the guarded behavior.
- `config/iverif_config.md` documents both keys.

## 0.3.1 — 2026-07-28

First external review disposed (`review/20260726_gpt_5.6_terra_grill.md`,
gpt 5.6). Doc-only — no kernel change; version bumped because a vendored
file (`docs/profiles.md` → `workflow/profiles.md`) changed content.

- **`review/` established** as the audit trail for external reviews: the
  original text is committed verbatim, beside a disposition record
  (`*.disposition.md`) that maps every recommendation to exactly one of
  already-covered (with citation) / build-at-trigger (deferred row) /
  declined (with written rationale). No recommendation may end up
  unaccounted — the same rule the deferred ledger applies to mechanisms.
- **`docs/deferred.md`**: the `spec_ref`/`coverage_delta` promotion row
  expanded into a full **chain audit** (`docs.py --chain-audit`,
  whole-graph break-link check spec → scenario → checker → coverage →
  evidence; review rec 1). Five new rows from the review, each with a
  concrete trigger: risk-graded card paths, `make env-check` preflight,
  FL symptom-fingerprint fields, formal evidence record, tool-capability
  profiles. The chain-audit trigger (first coverage-driven milestone
  signoff) is imminent — pulp_axi_xbar_copilot's M2 functional-coverage
  campaign (F-M2-08) is in flight.
- **`docs/profiles.md`**: the files-not-conversation handoff rule now
  carries its rationale, and the review's relaxation request ("ephemeral
  collaboration, only conclusions filed") is declined on the record: the
  cost (duplicate digging) is answered by dispatch Q1's grep-the-archive
  rule, not by reopening the common-mode channel between DE and DV.
- Out-of-repo items routed, not dropped: error-signature clustering and
  transaction-timeline summaries belong to the xverif toolkit — the
  framework's job is to bind them into dispatch cards once they exist.

## 0.3.0 — 2026-07-27

Execution discipline promoted to canon and given priority over convenience.

- **New `docs/discipline.md`**, vendored to every project as
  `workflow/discipline.md` (26th pinned file): five rules — think before
  coding · simplicity first · surgical changes · goal-driven execution ·
  small closed loops. Rules 1–4 are adapted from Andrej Karpathy's
  LLM-coding guidelines (multica-ai/andrej-karpathy-skills), each fused to
  the pain this framework already banked rather than pasted: "don't assume"
  binds to SPEC_ISSUE + the spec-not-RTL input boundary; "simplicity first"
  binds to the deferred ledger and carves out an explicit exception for
  fail-closed gates (never simplify a gate open to pass your own card);
  "surgical changes" binds to unconditional taxonomy registration and to
  the fw-check no-local-edit rule; "goal-driven" binds to the machine
  verdict (*if you cannot state the goal as a gate that passes, restate the
  goal*). Rule 5 is framework-native, contributed by pulp_axi_xbar_copilot.
- **Priority is explicit**: above convenience, below the four core
  invariants and the role isolation boundaries — discipline governs the
  space between the gates, where no script is watching.
- **Propagation**: `CLAUDE.project.{learning,copilot}.md` carry a
  read-first pointer under the profile line; all five role templates
  (`agents/*.copilot.md`, `agents/rev.learning.md`) repeat it above their
  first instruction, rev additionally review-enforces it. Only pointers
  travel — the text lives solely in the snapshot, so it cannot drift into a
  stale local restatement (the failure mode 0.2.1 had just cleaned up
  twice: FB-7's duplicated taxonomy rule and FB-5's contradictory role
  wording).
- Tests: 47 → 48 (the doc reaches `workflow/`, and CLAUDE.md + every
  rendered role file point at it, in both profiles).

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
  FIX_READY is now explicitly orch's to set once the commit hash is known.
  **`kernel/docs.py`**: the copilot `bug_fixing` next-action phrase said
  "awaiting DE root cause + fix commit" — the same role confusion, relocated
  to the mechanically-derived surface `make next`, where it would have kept
  pointing at DE for a hash DE cannot have. Now names orch as the committer
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
  `.claude/settings.local.json`) in it — and `docs/deferred.md` now carries
  the `--allow-existing` row with its trigger, so the decision not to build
  it is registered where the ledger says such decisions live, not only in
  adoption prose (FB-1); and notes that Claude Code's
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
