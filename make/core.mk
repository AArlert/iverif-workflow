# iverif core targets: doc mechanical layer + drift check.
# Pinned into scripts/make/core.mk; include from the project root Makefile:
#   include scripts/make/core.mk
.PHONY: handover next docs-check docs-archive bump bump-minor fw-check fw-pull

handover:
	@python3 scripts/docs.py --handover

next:
	@python3 scripts/docs.py --next

docs-check:
	@python3 scripts/docs.py --check

docs-archive:
	@python3 scripts/docs.py --archive

bump:
	@python3 scripts/bump.py

bump-minor:
	@python3 scripts/bump.py minor

# Verify the pinned framework snapshot is unmodified (hash-pinned).
# Local edits => improve the framework repo, then: fwsync --pull <fw-clone>
fw-check:
	@python3 scripts/fwsync.py --check

# Refresh the snapshot from the upstream named in iverif.json (framework_repo).
fw-pull:
	@python3 scripts/fwsync.py --pull
