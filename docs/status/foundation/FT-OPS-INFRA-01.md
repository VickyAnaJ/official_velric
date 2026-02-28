# FT-OPS-INFRA-01

## Metadata
- FT_ID: FT-OPS-INFRA-01
- Owner: Shivaganesh
- Status: [Done]
- Linked Slices: SLICE-OPS-01, SLICE-OPS-02, SLICE-OPS-03

## What this foundation task does (one sentence, plain language)
Provides shared Jac/Jaseci runtime plumbing and slice-neutral contracts needed by active slices.

## Scope/Contract
- Shared runtime wiring only.
- Shared environment/config/bootstrap contracts only.
- No user-visible incident behavior.
- No slice-specific business logic.

## Activity Log
- Reset to planned state after removal of the non-conformant Python implementation.
- Claimed during collaborative Step `3.2` by `Shivaganesh`.
- Contract consumers:
  - `SLICE-OPS-01` -> real shared runtime/bootstrap implementation owner
  - `SLICE-OPS-02` -> mock consumer
  - `SLICE-OPS-03` -> mock consumer
- Step `3.3` strategy alignment for `SLICE-OPS-01` selected a single-file Jac-native implementation path:
  - keep `main.jac` as the canonical runtime locus
  - keep shared runtime/bootstrap concerns slice-neutral
  - do not reintroduce a separate Python orchestration service
  - foundation work must expose common runtime/bootstrap contracts that downstream slices can consume or mock without owning the implementation
- Step `3.5` `PR1-01` runtime contract finalization:
  - added explicit runtime contract metadata helper in `main.jac`
  - aligned published bootstrap surfaces to Phase 1 contract metadata
  - kept all changes slice-neutral and avoided real triage/business behavior
- Step `3.5` `PR1-02` signal-path alignment:
  - aligned mock vLLM payload shape with labeled Phase 1 metrics
  - added Jac-side Phase 1 parsing helpers in `main.jac`
- Step `3.5` `PR1-03` typed graph schema:
  - added `Metric` node plus expanded Phase 1 `Incident` state fields
  - added root-persistence helper for the incident neighborhood
- Step `3.5` `PR1-04` triage runtime path:
  - implemented `triage_walker` body for the bounded Phase 1 hypothesis path
  - preserved fail-closed behavior for unsupported incidents
- Step `3.5` `PR1-05` trigger/read path:
  - connected persisted incident state to the Phase 1 trigger and incident-state endpoints
  - updated minimal UI copy to match active slice behavior

## Verification Evidence
- Claim recorded in `docs/STATUS.md` Foundation Task Registry and Step `3.2` outputs.
- Strategy dependency recorded in `docs/status/slices/SLICE-OPS-01.md` Step `3.3`.
- `tests/unit/test_bootstrap_artifacts.py` covers runtime contract metadata presence.
- `make build` -> Pass.
- `./scripts/test_unit.sh` -> Pass.
- `./scripts/test_integration.sh` -> Pass.
- `./scripts/test_coverage.sh` -> Pass (`30.97%` >= `25.00%`).
- `tests/unit/test_phase1_slice_contracts.py` -> Pass.
- `tests/integration/test_phase1_slice_layout.py` -> Pass.
- Latest full prompt-chain verification:
  - `make build` -> Pass.
  - `./scripts/test_unit.sh` -> Pass.
  - `./scripts/test_integration.sh` -> Pass.
  - `./scripts/test_coverage.sh` -> Pass (`31.58%` >= `25.00%`).
  - `.venv/bin/jac run main.jac` -> Pass.

## Closure
- Result: Complete.
- Notes:
  - shared Jac runtime/bootstrap contracts have now been consumed by all three slices
  - no remaining active slice depends on unfinished shared runtime plumbing
