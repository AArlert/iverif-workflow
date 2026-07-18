# Framework self-maintenance. Project-facing targets live in make/*.mk.

.PHONY: selftest manifest

selftest:
	cd kernel/tests && python3 -m unittest discover -v

# Regenerate kernel.manifest.json after any kernel/ change, then bump VERSION.
manifest:
	python3 kernel/fwsync.py --gen-manifest
