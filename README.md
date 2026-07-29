# iverif-workflow

**A verification workflow where the evidence chain is the runtime
interface** — between the engineer, the review agent, and the tools.

Every claim a project makes ("this scenario passes", "this bug is closed",
"this milestone is done") must be backed by a machine-generated, replayable
evidence record. Scripts read the evidence chain to derive project state and
the next action; agents read it to review; humans read it to trust. Nothing
is tracked by memory, chat history, or hand-edited status flags.

**Start with [CLAUDE.md](CLAUDE.md)** — the whole framework on one page: the
five invariants, the machine loop, and the make target table. It is the
only file a new session has to read before working.

## This repo *is* the template

There is no separate scaffolding tool. `git clone` this repo, rename it, and
you have a working project — `doc/`, `design-prompt/`, `rtl/`, `tb/`, `sim/`
already exist as empty shells; `scripts/`, `workflow/`, `.claude/agents/`
are the real machinery, ready to run.

```bash
git clone https://github.com/AArlert/iverif-workflow.git my_dut
cd my_dut
# read CLAUDE.md — the whole framework, one page
make handoff          # project state, derived from the docs — never stale
make next             # mechanically derived next actions
```

The daily loop is the one CLAUDE.md describes:

```
register scenario → write code → make run → make evidence → (review) → make next
```

## Repository map

| Path | What it is |
|---|---|
| `CLAUDE.md` | The whole framework, one page: invariants, loop, make table, dispatch grading |
| `workflow/` | 4 contracts: `discipline.md` · `bugs.md` (5-class taxonomy) · `records.md` (evidence + testplan contract) · `review.md` (six questions + rubric) |
| `.claude/agents/` | 5 role cards: `orch` · `arch` · `de` · `dv` · `rev`, each ≤1 page |
| `scripts/` | Mechanical layer (stdlib-only Python ≥3.8): `evidence.py`, `docs.py`, `svacheck.py`, `bump.py`, `iverif_config.py`; `scripts/tests/` (functional + fuse tests); `scripts/make/vcs-2018.mk` (tool-quirk authority) |
| `doc/` | Project state: `spec.md` (sha256-pinned) · `feature-matrix.md` · `testplan.md` · `bugs.md`+`bugs/` · `evidence/` (machine-written only) · `archive/` · `VENDOR.md` (vendored-DUT patch tracking) |
| `DESIGN.md` | Canon-only genealogy: why the shape is what it is, and what got cut. Never shipped to a fork; safe to delete after cloning |
| `reviews/` | Historical external reviews of the framework, with dispositions |

## Upgrading

`workflow/` and `scripts/` are upstream files — a clone can edit them
freely, and that is on the clone to maintain (each carries a one-line
"upstream file" header, not a hash pin). To pull an improvement: keep this
repo as a remote and `git cherry-pick` the commits you want. There is no
sync tool, no manifest, no declared-divergence state — you either pull a
commit or you don't, and not pulling never turns anything red.

## Why this exists

The machinery originally lived inside a single project and was hand-copied
into a second one. The copies drifted: a milestone-gate bug already fixed
upstream reappeared in the copy, a CI workflow got lost, tracked junk files
crept back in. The earlier fix was a hash-pinned snapshot + a drift-detection
state machine (fwsync); it worked, but the machine guarding 24 contracts
became a second thing to keep straight. 0.8.0 changes the answer: shrink the
framework surface to a size a person can hold in their head — one CLAUDE.md
page, four contracts, five agent cards — and let git's own history do what
the state machine used to do. See [DESIGN.md](DESIGN.md) for the full
adjudication trail, including what got cut and why.

## Design principles

**Effective · lean · clear · token-cheap** — for this repo and for every
clone. Corollaries:

- **Write it as short as it can be.** The rule and its check, one line of
  why at most. The story lives in `DESIGN.md`, never in operative docs.
  `scripts/tests/test_budgets.py` caps CLAUDE.md + workflow/'s total bytes.
- **Thick storage, thin read surface.** Full history is archived; sessions
  read only rolling summaries (`status.jsonl` head, last `log.md` block,
  testplan table).
- **Mechanics to scripts, semantics to humans/agents.** Anything a script can
  derive (state counts, next actions, evidence excerpts, table backfills) is
  never done by hand.
- **No infrastructure ahead of pain.** A mechanism gets built when a real
  pain point forces it, not on spec — see `DESIGN.md` for the ledger of what
  never needed building.

## License

MIT
