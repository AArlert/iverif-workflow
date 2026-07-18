# `iverif.json` reference

Every project repo carries one `iverif.json` at its root. It is the **only**
file that varies between projects — the kernel scripts themselves are
byte-identical, hash-pinned copies. (stdlib has no jsonschema; this document
plus `kernel/iverif_config.py`'s load-time checks are the contract.)

Column presets live **inside** `kernel/iverif_config.py` (one vendored file,
one source of truth); `iverif.json` only names a preset and optionally
overrides individual keys.

| Key | Required | Default | Meaning |
|---|---|---|---|
| `framework` | recommended | — | Framework version this project last pulled (informational; `fwsync --pull` updates it, diffs make upgrades visible) |
| `profile` | **yes** | — | `learning` or `copilot` — see docs/profiles.md |
| `project_name` | **yes** | — | Used in handover banners and regression summaries |
| `columns_preset` | no | `en` | `en` or `zh` — table column names (legacy repos keep `zh` and change zero docs) |
| `columns_override` | no | `{}` | Per-key deviations, e.g. `{"fm_module": "组件"}` for floo_axi_chimney |
| `delivery.glob` | no | `rtl/{name}.sv` | Where a feature-matrix entry's deliverable lives; learning repos typically `tb/{name}.sv`. Entries not matching `\w+` (e.g. `(all)`) have no delivery notion |
| `sim_log` | no | `sim/out/{test}_{seed}.log` | Where `make run` leaves logs |
| `signoff_glob` | no | `signoff-M{m}*.md` | Milestone signoff filename pattern inside `doc/evidence/v0.{m}.*/`. Legacy: ppa `review-m{m}*-milestone.md`, floo `review-M{m}*.md` |
| `archive_dir` | no | `doc/archive` | Archive directory (canon). Legacy ppa layout: `doc` (flat `*-archive.md` files) |
| `fl_schema_enforce` | no | `true` | Validate failure-record detail pages of terminal bugs against `schema/failure_record.md`. Legacy repos with free-form pages set `false` |
| `limits` | no | see below | Rolling-file caps; override sparingly |

`limits` defaults: `status_max_lines` 12, `status_keep` 8,
`summary_max_chars` 200, `log_max_blocks` 4, `log_keep` 3, `bug_done_max` 4,
`bug_done_keep` 2, `waiver_done_max` 6, `waiver_done_keep` 2.

## Column semantic keys (for `columns_override`)

testplan: `tp_id` `tp_milestone` `tp_status` `tp_evidence` `tp_repro` ·
feature-matrix: `fm_id` `fm_milestone` `fm_module` `fm_scenes` ·
bugs: `bug_id` `bug_status` `bug_suspect` `bug_summary` `bug_repro`
`bug_fix_commit` `bug_verify` ·
waivers (prefix-matched): `wv_id` `wv_conclusion_prefix` `wv_review_prefix` ·
spec: `spec_change_heading`

Full mapping tables: `COLUMN_PRESETS` in `kernel/iverif_config.py`.

## Examples

See `config/examples/iverif.learning.json` and
`config/examples/iverif.copilot.json`.
