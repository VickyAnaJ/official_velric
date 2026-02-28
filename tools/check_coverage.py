#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import trace
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "tools" / "coverage_threshold.json"
sys.path.insert(0, str(ROOT))


def count_source_lines(path: Path) -> int:
    total = 0
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        total += 1
    return total


def main() -> int:
    cfg = json.loads(CONFIG_PATH.read_text())
    threshold = float(cfg["threshold_percent"])

    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"))

    tracer = trace.Trace(count=True, trace=False)
    result = tracer.runfunc(unittest.TextTestRunner(verbosity=0).run, suite)
    if not result.wasSuccessful():
        print("Coverage gate aborted: tests failed")
        return 1

    counts = tracer.results().counts
    source_files = [ROOT / "mock_vllm.py", ROOT / "tools" / "bootstrap_check.py"]

    executable = 0
    executed = 0
    for src in source_files:
        lines_total = count_source_lines(src)
        executable += lines_total
        src_str = os.path.abspath(src)
        touched = {lineno for (filename, lineno), _ in counts.items() if os.path.abspath(filename) == src_str}
        executed += len(touched)

    percent = (executed / executable * 100.0) if executable else 0.0
    print(f"Coverage (approx): {percent:.2f}% (threshold {threshold:.2f}%)")
    return 0 if percent >= threshold else 2


if __name__ == "__main__":
    raise SystemExit(main())
