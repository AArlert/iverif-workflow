# iverif-workflow

**A verification workflow framework where the evidence chain is the runtime
interface** — between the engineer, the review agent, and the tools.

Every claim a project makes ("this scenario passes", "this bug is closed",
"this milestone is done") must be backed by a machine-generated, replayable
evidence record. Scripts read the evidence chain to derive project state and
the next action; agents read it to review; humans read it to trust. Nothing
is tracked by memory, chat history, or hand-edited status flags.

**Start with [CONSTITUTION.md](CONSTITUTION.md)** — the whole framework on
one page: five axioms, one machine loop, and the mechanism index. It ships
into every project as `workflow/constitution.md`, its size is capped by a
kernel test, and every shipped doc must name its generating axioms and its
consumer (also test-enforced). The four core invariants (no sim log no ✅ ·
replay command on line 1 · closer ≠ fixer · spec pinned) live there in
their canonical form.

This repository is the **single source of truth** for the machinery. Project
repos pin a hash-anchored snapshot of it and are forbidden from editing the
snapshot in place — improvements flow back here first, then out to every
project. That is how mechanism drift (the reason this repo exists — see
[Why this exists](#why-this-exists)) stays dead.

## Repository map — the layout is the mental model

| Path | Altitude | What it is |
|---|---|---|
| `CONSTITUTION.md` | constitution | Axioms · loop · mechanism index; ships as `workflow/constitution.md` |
| `loop/` | mechanism | The machine's contracts, shipped 1:1 as project `workflow/`: record contracts (`testplan_entry`, `evidence_record`) · `review/` (six questions, signoff rubric) · `fail/` (the whole failure branch: failure record, taxonomy, RCA template, dispatch tables) · `discipline.md` · `profile.*.md` |
| `kernel/` | mechanism | Canonical Python scripts (stdlib-only, ≥3.8): `docs.py`, `evidence.py`, `bump.py`, `regress.py`, `fwsync.py`; `kernel/tests/` including fuse tests for bugs that have already drifted once |
| `make/` | facts | Includable make fragments: `core.mk`, `evidence.mk`, `vcs-2018.mk` (its header is the tool-quirk authority) |
| `harness/` | mechanism | Claude-coupled render sources: `agents/` (role definitions), `skills/` (session skills), `templates/` (project seeds) |
| `config/` | facts | `iverif.json` reference + column presets |
| `governance/` | canon-only | The framework's self-application layer, never shipped: `deferred.md` (trigger ledger), `design-notes.md` (adjudications), `adoption.md` (playbooks), `reviews/` (external reviews + dispositions) |

## 60-second start (new project)

```bash
git clone https://github.com/AArlert/iverif-workflow.git
python3 iverif-workflow/kernel/fwsync.py --init my_dut --profile learning --columns en
cd my_dut
# read workflow/constitution.md — the map
make handover        # project state, derived from the docs — never stale
make next            # mechanically derived next actions
```

`--init` lays down `scripts/` (kernel snapshot), `workflow/` (constitution +
loop contracts, readable offline inside the VM), `doc/` seeds, make
includes, git hygiene files, and `iverif.json`. From then on the daily loop
is the machine loop from the constitution:

```
register scenario → write code → make run → make evidence → (review) → make next
```

## Two profiles, one framework

| | `learning` | `copilot` |
|---|---|---|
| Who writes the UVM code | the human | agents |
| Agent role | `rev` only: reviews evidence against the six questions, mentors with principles — never code | full chain: orch dispatches arch / de / dv / rev (canonical suite in `harness/agents/`, dispatch-card manual in `harness/skills/dispatch/`) |
| Guard strictness | few, high-value checks | full check set |

Set once in `iverif.json`; the kernel branches internally. The multi-role
isolation rules that protect agent pipelines from common-mode errors degrade,
in the learning profile, into a thinking checklist (e.g. *"derive expected
values from the spec, never from the RTL you are testing"*).

## First adopters

The framework is DUT-agnostic. Its first adopters run each DUT twice — an
agent-driven repo (reference answer, workflow stress-test) and a human
learning repo (same evidence discipline, `rev` agent reviews only):

```
                    iverif-workflow  (this repo — canon)
                          │  fwsync --pull (hash-pinned snapshot)
      ┌───────────┬───────┴────────┬─────────────────┐
      ▼           ▼                ▼                 ▼
 ppa-lite-copilot pulp_axi_xbar_agent floo_axi_chimney_agent   (copilot line)
 ppa_lite         pulp_axi_xbar       floo_axi_chimney         (learning line)
```

Both lines share this framework, so their evidence is comparable and neither
can quietly lower the bar.

## Drift control & forks

The enemy is silent drift, not adaptation. Three sanctioned states:

- **Pristine** (green): `scripts/iverif.manifest.json` pins version + sha256
  per file; `make fw-check` re-hashes (warn in pre-commit, hard-fail in CI).
- **Declared divergence** (yellow): a local edit registered in
  `scripts/iverif.divergence.json` (reason + upstream ref). fw-check lists
  it and passes. A declaration is a loan — feed it back via the project's
  fw-feedback, or graduate to a fork.
- **Fork** (green again): clone this repo, point `framework_repo` in
  `iverif.json` at your fork; `make fw-pull` now tracks it. Feedback
  upstream stays welcome.

Undeclared edits stay red. The kernel has its own regression tests; any bug
fixed once gets a fuse test so it can never silently return via a stale
copy.

## Why this exists

The machinery originally lived inside ppa-lite-copilot and was hand-copied
into floo_axi_chimney. The copies drifted: floo kept running a milestone-gate
bug (`any(generator)` — always truthy, so the "rev signoff exists" check was
a silent no-op) that ppa had already found and fixed, lost the CI workflow in
the copy, and picked up tracked junk files. One repo of truth, hash-pinned
snapshots, and kernel self-tests are the structural answer.

## Design principles

**Effective · lean · clear · token-cheap** (有效·精炼·清晰·省token) — for
this repo and for every pinned snapshot it ships. Corollaries:

- **Write it as short as it can be.** Snapshot text is contract: the rule
  and its check, one line of why at most. The story lives in the CHANGELOG
  or `governance/design-notes.md`, never in operative docs. Canon CI holds
  a byte budget per pinned doc.
- **Thick storage, thin read surface.** Full history is archived; sessions
  read only rolling summaries (`status.jsonl` head, last `log.md` block,
  testplan table).
- **Mechanics to scripts, semantics to humans/agents.** Anything a script can
  derive (state counts, next actions, evidence excerpts, table backfills) is
  never done by hand.
- **No infrastructure ahead of pain.** Mechanisms are added when a real pain
  point triggers them; the waiting list and its triggers live in
  [governance/deferred.md](governance/deferred.md).

## License

MIT
