# Changelog

All framework changes land here. Project repos decide when to `fwsync --pull`
based on this file; the version they carry is recorded in their `iverif.json`.

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
