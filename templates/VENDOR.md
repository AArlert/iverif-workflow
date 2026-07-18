# Vendored DUT snapshot

Upstream code under `vendor/` is a **read-only snapshot**, SHA-locked below.
Never edit vendored files directly; behavioral deviations go through the
P-xxx patch flow so every delta from upstream is recorded, justified, and
rev-reviewed.

## Locked upstream versions

| Component | Upstream repo | Version/tag | Commit SHA | License |
| --- | --- | --- | --- | --- |
| <!-- e.g. axi --> | <!-- github url --> | <!-- v0.39.9 --> | <!-- sha --> | <!-- e.g. SHL-0.51 --> |

## Patches (P-xxx)

Applied only when the snapshot cannot run in this environment (tool
compatibility) or a confirmed upstream bug blocks work. Behavior-equivalent
unless the linked bug record says otherwise.

| ID | File(s) | Reason | Behavior impact | Bug/FL ref | rev review |
| --- | --- | --- | --- | --- | --- |
| <!-- P-001 --> | | | <!-- equivalent / describe --> | | <!-- REV-xxx — backfilled by the main session after review --> |

Flow: patch → register the row here → request rev review → **main session
backfills the review column** (rev has no write access to this file). An
empty review cell on an applied patch is a gate finding.

Confirmed upstream bugs (taxonomy `DUT_BUG`): record as an FL, patch with a
P-xxx row, and consider reporting upstream.
