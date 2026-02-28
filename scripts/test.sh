#!/usr/bin/env bash
set -euo pipefail

./scripts/test_unit.sh
./scripts/test_integration.sh
