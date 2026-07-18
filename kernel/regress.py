#!/usr/bin/env python3
# One-shot regression: read the regression list, `make run` each entry, judge
# each log, write sim/result_summary.txt.
# List format (sim/regress/regress.list): one "<TEST> <SEED>" per line,
# '#' starts a comment.
import subprocess
import sys
from datetime import date

from iverif_config import load_config, log_verdict


def main():
    cfg = load_config()
    sim = cfg.root / "sim"
    default_list = sim / "regress" / "regress.list"
    summary_path = sim / "result_summary.txt"

    cov = "1" if "COV=1" in sys.argv[1:] else "0"
    pos = [a for a in sys.argv[1:] if not a.startswith("COV=")]
    list_file = (cfg.root / pos[0]) if pos else default_list
    entries = []
    for lineno, line in enumerate(
            list_file.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            sys.exit("regression list line %d malformed (expected "
                     "'<TEST> <SEED>'): %s" % (lineno, line))
        entries.append((parts[0], parts[1]))
    if not entries:
        sys.exit("regression list is empty")

    # Clean before regressing: VCS reuses incremental build products under
    # out/ (.daidir, csrc, ...) across sessions; mixing products from
    # different option sets (e.g. a prior `make lint`) corrupts the build
    # database and produces false failures (VFS_SDB_ERROR class). Regression
    # evidence must start from a clean slate rather than rely on the caller
    # remembering to `make clean`.
    subprocess.run(["make", "-C", str(sim), "clean"], check=True)

    results = []
    for test, seed in entries:
        print("== regress: %s SEED=%s ==" % (test, seed), flush=True)
        rc = subprocess.run(
            ["make", "-C", str(sim), "run", "TEST=%s" % test,
             "SEED=%s" % seed, "COV=%s" % cov],
        ).returncode
        log = cfg.sim_log_path(test, seed)
        if not log.exists():
            verdict = "NOLOG"
        else:
            verdict = log_verdict(
                log.read_text(encoding="utf-8", errors="replace"))
        if rc != 0 and verdict == "PASS":
            verdict = "FAIL"  # abnormal sim exit never counts as a pass
        results.append((test, seed, verdict))

    passed = sum(1 for _, _, v in results if v == "PASS")
    lines = ["%s regression  date=%s  passed=%d/%d"
             % (cfg.project, date.today(), passed, len(results))]
    lines += ["%-6s %s SEED=%s" % (v, t, s) for t, s, v in results]
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + "\n".join(lines))
    print("\nsummary written to %s" % summary_path.relative_to(cfg.root))
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
