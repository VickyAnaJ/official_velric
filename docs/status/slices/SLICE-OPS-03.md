# SLICE-OPS-03

## Metadata
- Slice ID: SLICE-OPS-03
- Capability: Verification, rollback safety, audit timeline, and demo visibility.
- Owner: Keilly
- Included FR IDs: FR-11, FR-12, FR-13, FR-14, FR-15
- Relevant NFR IDs: NFR-P-03, NFR-P-04, NFR-U-01, NFR-U-02, NFR-R-02
- Status: [WIP]
- Start Gate: Active

## 3.1 Planning and Activation Output
### Source mapping from `docs/SYSTEM_DESIGN_PLAN.md`
- Phase alignment: Phase 2 closure plus Phase 3 polish/demo visibility
- Architecture components owned in this slice:
  - `verify_walker`
  - `rollback_walker`
  - `audit_walker`
  - Jac frontend expansion for 4 panels and MTTR dashboard
- Walker/data-flow boundaries owned in this slice:
  - re-poll post-action metrics
  - compare recovery condition
  - invert prior allowlisted actions on verification failure
  - append audit entries on every success/failure path
  - expose verification, audit, and MTTR state through polled incident view
- FR/NFR set assigned here:
  - FRs: `FR-11`, `FR-12`, `FR-13`, `FR-14`, `FR-15`
  - NFRs: `NFR-P-03`, `NFR-P-04`, `NFR-U-01`, `NFR-U-02`, `NFR-R-02`
- Planning verdict:
  - Valid planned slice.
  - Activated in collaborative mode because execution outputs and lifecycle state from `SLICE-OPS-02` can be consumed as explicit mocks/contracts until the owning implementation lands.

## 3.2 Dependency Output
### Dependency header
- Slice ID: `SLICE-OPS-03`
- External reference sources used for this dependency check:
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`

### Physical dependency list
| Resource | Required capability | Status | Handling decision | Owner |
|---|---|---|---|---|
| Jac runtime in `.venv` | run verify/rollback/audit walkers and `cl {}` polling UI | Available | Use | Keilly |
| `main.jac` bootstrap entrypoint | place for lifecycle walkers, audit entities, frontend panels, MTTR display state | Available | Use | Keilly |
| mock vLLM metrics endpoint | re-poll post-action recovery metrics | Available | Use | Keilly |
| frontend polling state contract | 1-second poll shape for current stage, verification state, audit log, MTTR | Missing | Claim | Keilly |

### Shared dependency list
| Task ID | Current status | Owner | Handling decision | Interface contract reference | Foundation Detail File |
|---|---|---|---|---|---|
| FT-OPS-INFRA-01 | [WIP] | Shivaganesh | Mock | shared runtime/bootstrap contract and common endpoint skeleton | `docs/status/foundation/FT-OPS-INFRA-01.md` |
| FT-OPS-TEST-01 | [WIP] | Keilly | Claim | deterministic test harness and coverage plumbing for lifecycle, audit, and UI state checks | `docs/status/foundation/FT-OPS-TEST-01.md` |

### Upstream slice contract dependencies
| Dependency | Current status | Owner | Handling decision | Contract reference |
|---|---|---|---|---|
| `ActionResult` and execution lifecycle state | [WIP] | Ana | Mock | `docs/SYSTEM_DESIGN_PLAN.md` entities, data flow, and failure-mode sections |
| `RemediationPlan` verification contract | [WIP] | Ana | Mock | `docs/SYSTEM_DESIGN_PLAN.md` communication/contracts section |

### Mandatory dependency prompt requirements for Step 3.4/3.5
| Prompt purpose | Linked dependency | Required ordering/gate |
|---|---|---|
| Define verification/rollback/audit contracts against mocked execution outputs | `ActionResult` and execution lifecycle state | Must precede any real lifecycle walker implementation |
| Establish shared deterministic test harness for lifecycle flows | FT-OPS-TEST-01 | Must run before reviewable lifecycle implementation prompts |
| Define polled incident-state visibility contract | frontend polling state contract | Must exist before UI/audit/MTTR prompts |

### Dependency readiness verdict
- Verdict: `Ready`

### Blockers
- None. Upstream execution contracts are explicit enough to mock safely.

## 3.3 Strategy Evaluation + Final Convergence
- Not started.

## 3.3.1 Pattern Evaluation + Final Convergence
- Not started.

## 3.4 Prompt Chain
- Not started.

## 3.5 Prompt Execution Reports
- Not started.

## 3.6 Slice Review Output
- Not started.

## 3.7 Retry/Escalation Log
- Not started.

## 3.8 Slice Closure Output
- Not started.
