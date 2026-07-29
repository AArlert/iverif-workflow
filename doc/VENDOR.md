# Vendored DUT snapshot

("vendor" in this ecosystem refers ONLY to upstream DUT RTL under `vendor/`.
The framework itself — `scripts/` + `workflow/` — is a separate mechanism;
this file does not track it.)

Upstream code under `vendor/` is a **read-only snapshot**, SHA-locked below.
Never edit vendored files directly; behavioral deviations go through the
P-xxx patch flow so every delta from upstream is recorded, justified, and
rev-reviewed.

## Locked upstream versions

| Component | Upstream repo | Version/tag | Commit SHA | License |
| --- | --- | --- | --- | --- |
| example_ip | https://example.org/example_ip | v1.2.3 | 0123abcd... | Apache-2.0 |

## Patches (P-xxx)

Applied only when the snapshot cannot run in this environment (tool
compatibility) or a confirmed upstream bug blocks work. Behavior-equivalent
unless the linked bug record says otherwise.

| ID | File(s) | Reason | Behavior impact | Bug/FL ref | rev review |
| --- | --- | --- | --- | --- | --- |
| P-001 | | | equivalent / describe | | REV-xxx — backfilled by the main session after review |

Flow: patch → register the row here → request rev review → **main session
backfills the review column** (rev has no write access to this file). An
empty review cell on an applied patch is a gate finding.

Confirmed upstream bugs (taxonomy `DUT_BUG`): record as an FL, patch with a
P-xxx row, and consider reporting upstream.
