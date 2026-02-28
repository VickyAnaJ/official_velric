# FT-OPS-TEST-01

## Metadata
- FT_ID: FT-OPS-TEST-01
- Owner: Keilly
- Status: [Done]
- Linked Slices: SLICE-OPS-03

## What this foundation task does (one sentence, plain language)
Provides shared deterministic test harness and coverage plumbing for slice work.

## Scope/Contract
- Shared test harness only.
- Shared fixture/coverage plumbing only.
- No user-visible incident behavior.
- No slice-specific business logic.

## Activity Log
- Reset to planned state after removal of the non-conformant Python implementation.
- Claimed during collaborative Step `3.2` by `Keilly`.
- Contract consumers:
  - `SLICE-OPS-03` -> real shared test-harness implementation owner
  - `SLICE-OPS-01` -> mock consumer until shared harness lands
- `SLICE-OPS-01` was removed as a consumer after closure review confirmed its tests are slice-local and do not depend on this foundation task.
- `SLICE-OPS-03` Step `3.5` advanced this foundation task:
  - added `tests/unit/test_slice_ops_03_contracts.py`
  - added `tests/integration/test_slice_ops_03_prompt_chain_contract.py`
  - updated older bootstrap/layout tests to match the expanded lifecycle and UI contract
  - kept the work harness-focused; slice behavior still lives in `main.jac`

## Verification Evidence
- Claim recorded in `docs/STATUS.md` Foundation Task Registry and Step `3.2` outputs.
- `SLICE-OPS-01` review surfaced and corrected stale UI-copy assertions before final local review pass.
- `./scripts/test_unit.sh` -> Pass.
- `./scripts/test_integration.sh` -> Pass.
- `./scripts/test_coverage.sh` -> Pass (`31.58%` >= `25.00%`).

## Closure
- Result: Complete.
- Notes:
  - shared lifecycle test-harness coverage required by `SLICE-OPS-03` is now present and locally verified
  - no remaining active slice depends on unfinished work in this foundation task
