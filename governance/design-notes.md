# Design notes (canon-only — never pinned into projects)

Genealogy and adaptation records. Operative docs state rules and their
checks; the "why we chose this shape" stories live here. Anything in this
file is deliberately invisible to project repos.

## Release tags backfilled v0.3.1..v0.6.1 (2026-07-29)

The release ritual (adoption.md: edit → `make selftest` → `make manifest` →
bump `VERSION` + `CHANGELOG.md` → commit + tag) mandates a tag per release,
but tagging silently stopped after v0.3.0 — the 17 releases of the rapid
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
