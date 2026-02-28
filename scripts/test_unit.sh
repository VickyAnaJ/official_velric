#!/usr/bin/env bash
set -euo pipefail

python3 -m unittest discover -s tests/unit -p 'test_*.py' -v
