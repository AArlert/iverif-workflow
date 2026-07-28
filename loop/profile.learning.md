# Profile contract: learning

<!-- Canonical: iverif-workflow/docs/profile.learning.md — pinned snapshot. -->

The human writes all RTL/TB code and runs `make evidence`. The only agent is
`rev`: reviews evidence against the six questions, mentors with principles —
never code. The main session may scaffold compilable skeletons (signatures +
TODOs), nothing more. `--next` speaks to you ("write…", "run…", "request a
review of…").

## Non-negotiable (both profiles)

- The four core invariants: no sim log no ✅ · replay command on line 1 ·
  closer ≠ fixer · spec pinned.
- Record schemas (`workflow/schema/`), failure taxonomy, dispatch tables,
  six questions, signoff rubric.
- Rolling memory: `doc/status.jsonl` + `doc/log.md` + `doc/testplan.md`,
  archives under `doc/archive/`.

## Guard set (core checks only)

1. A ✅ scenario references an existing evidence file whose line 1 is a
   replay command.
2. A CLOSED bug carries re-verification evidence.
3. `spec.md` matches its pinned sha256.
4. Rolling-file limits (status/log/bugs).
5. Version sync across `version.json` / `status.jsonl` / `log.md`.
6. Junk-file hygiene.

Copilot-only checks (design-prompt files, inter-agent handoff policing) are
off — they protect agent pipelines, not human learning.

## The thinking checklist

Instance isolation degrades, for one human, into a checklist against the
same failure mode — checker and design agreeing because both looked at the
same wrong thing:

- Derive expected values from `spec.md`, never from the RTL under test. A
  silent spec gap is a SPEC_ISSUE to log, not a license to copy behavior.
- Before closing your own bug: re-run the original failing seed plus one
  neighboring scenario; write the evidence before touching status.
- A test that passes on the first try: name what would have made it fail.
  If nothing could, tighten the check.
- Write review requests as if the reviewer knows nothing you did not write
  down.
