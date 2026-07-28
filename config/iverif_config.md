# `iverif.json` reference

Every project repo carries one `iverif.json` at its root. It is the **only**
file that varies between projects — the kernel scripts themselves are
byte-identical, hash-pinned copies. (stdlib has no jsonschema; this document
plus `kernel/iverif_config.py`'s load-time checks are the contract.)

Column presets live **inside** `kernel/iverif_config.py` (one pinned file,
one source of truth); `iverif.json` only names a preset and optionally
overrides individual keys.

| Key | Required | Default | Meaning |
|---|---|---|---|
| `framework` | recommended | — | Framework version this project last pulled (informational; `fwsync --pull` updates it, diffs make upgrades visible) |
| `profile` | **yes** | — | `learning` or `copilot` — see docs/profiles.md |
| `project_name` | **yes** | — | Used in handover banners and regression summaries |
| `columns_preset` | no | `en` | `en` or `zh` — table column names (legacy repos keep `zh` and change zero docs) |
| `columns_override` | no | `{}` | Per-key deviations, e.g. `{"fm_module": "组件"}` for floo_axi_chimney |
| `next_phrases_override` | no | `{}` | **Escape hatch** — remap individual `--next` phrases for genuinely project-specific wording. The common case (who owns deliverables) needs no override: it derives from `delivery` (see `delivery.owner`). Keys must exist in the profile's phrase set (`NEXT_PHRASES` in `kernel/docs.py`; unknown keys are a hard error, not a silent no-op) and values must keep the original `%(...)s` placeholders |
| `key_line_extra` | no | `[]` | **Escape hatch** — extra regexes for evidence key-line extraction. The canon convention needs no config: functional-coverage summary lines tagged `[FCOV_SUMMARY]` (schema/evidence_record.md row 6) are captured out of the box. Use only for further project-invented tags. Invalid regexes are a hard error at registration time |
| `delivery.glob` | no | `rtl/{name}.sv` | Where a feature-matrix entry's deliverable lives; learning repos typically `tb/{name}.sv`. Entries not matching `\w+` (e.g. `(all)`) have no delivery notion |
| `delivery.owner` | no | derived | Which role owns feature-matrix deliverables — drives `--next` card wording in the copilot profile. Default derives from `delivery.glob`: `tb/`-rooted → `dv` (vendored-DUT repos where deliverables are tb code), else `de`. Set explicitly only when the derivation is wrong |
| `sim_log` | no | `sim/out/{test}_{seed}.log` | Where `make run` leaves logs |
| `signoff_glob` | no | `signoff-M{m}*.md` | Milestone signoff filename pattern inside `doc/evidence/v0.{m}.*/`. Legacy: ppa `review-m{m}*-milestone.md`, floo `review-M{m}*.md` |
| `archive_dir` | no | `doc/archive` | Archive directory (canon). Legacy ppa layout: `doc` (flat `*-archive.md` files) |
| `fl_schema_enforce` | no | `true` | Validate failure-record detail pages of terminal bugs against `schema/failure_record.md`. Legacy repos with free-form pages set `false` |
| `sva_enforce` | no | `true` | SVA leg of the log verdict (`svacheck.py`): a log without the native `-assert verbose` Summary line is FAIL (fail-closed — assertion failures never increment UVM_ERROR, so the Summary line is the only structured proof of cleanliness). Legacy flows predating `-assert verbose` set `false` until they adopt the pinned run pattern; detected assertion-failure lines stay fatal either way |
| `sva_baseline` | no | — | Optional path to a registered assertion floor file (`{"total_min": N, "attempted_min": M}`). Catches the `$assertoff` / dropped-sva-file bypass class (failures stays 0 while total/attempted sink). Once configured, a missing/corrupt file is a hard error — deleting the baseline is not a bypass. Register at the first milestone that carries SVA; maintain by hand, never auto-adapt |
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
