# Design notes (canon-only — never pinned into projects)

Genealogy and adaptation records. Operative docs state rules and their
checks; the "why we chose this shape" stories live here. Anything in this
file is deliberately invisible to project repos.

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

## Profiles: split into per-profile contracts (0.4.0)

`docs/profiles.md` (both contracts + comparison in one pinned file) was
split into `docs/profile.{learning,copilot}.md`; a project receives only its
own contract as `workflow/profile.md`, selected by the sync parameter —
file-level separation over an in-file marker DSL (user ruling 2026-07-28).
Canon-side comparison stays in README §Two profiles.
