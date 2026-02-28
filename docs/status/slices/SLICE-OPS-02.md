# SLICE-OPS-02

## Metadata
- Slice ID: SLICE-OPS-02
- Capability: Policy-gated remediation planning and bounded execution.
- Owner: Ana
- Included FR IDs: FR-06, FR-07, FR-08, FR-09, FR-10
- Relevant NFR IDs: NFR-S-01, NFR-S-02, NFR-S-03, NFR-R-03, NFR-P-02
- Status: [WIP]
- Start Gate: Active

## 3.1 Planning and Activation Output
### Source mapping from `docs/SYSTEM_DESIGN_PLAN.md`
- Phase alignment: Phase 2 planning and bounded execution expansion
- Architecture components owned in this slice:
  - `plan_walker`
  - Policy Engine
  - `execute_walker`
  - Action Executor
- Walker/data-flow boundaries owned in this slice:
  - read typed `IncidentHypothesis`
  - generate typed `RemediationPlan`
  - enforce action allowlist, confidence threshold, and approval requirement
  - execute only allowlisted actions and update graph state after each action
  - stop before verification, rollback, audit summary, and final MTTR visibility
- FR/NFR set assigned here:
  - FRs: `FR-06`, `FR-07`, `FR-08`, `FR-09`, `FR-10`
  - NFRs: `NFR-S-01`, `NFR-S-02`, `NFR-S-03`, `NFR-R-03`, `NFR-P-02`
- Planning verdict:
  - Valid planned slice.
  - Activated in collaborative mode because typed graph and triage contracts from `SLICE-OPS-01` can be consumed as explicit mocks/contracts until the owning implementation lands.

## 3.2 Dependency Output
### Dependency header
- Slice ID: `SLICE-OPS-02`
- External reference sources used for this dependency check:
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`

### Physical dependency list
| Resource | Required capability | Status | Handling decision | Owner |
|---|---|---|---|---|
| Jac runtime in `.venv` | execute `plan_walker`/`execute_walker` and local REST/frontend flows | Available | Use | Ana |
| `main.jac` bootstrap entrypoint | place for walkers, policy checks, action executor contracts, frontend polling state | Available | Use | Ana |
| mock vLLM metrics endpoint | post-plan and later execution/verification signal compatibility | Available | Use | Ana |
| approval-gated local endpoint path | supervised execution pause/approval contract | Missing | Mock | Ana |

### Shared dependency list
| Task ID | Current status | Owner | Handling decision | Interface contract reference | Foundation Detail File |
|---|---|---|---|---|---|
| FT-OPS-INFRA-01 | [WIP] | Shivaganesh | Mock | shared runtime/bootstrap contract and common endpoint skeleton | `docs/status/foundation/FT-OPS-INFRA-01.md` |

### Upstream slice contract dependencies
| Dependency | Current status | Owner | Handling decision | Contract reference |
|---|---|---|---|---|
| Typed `IncidentHypothesis` on Incident node | [WIP] | Shivaganesh | Mock | `docs/SYSTEM_DESIGN_PLAN.md` walker/contracts sections for triage output |
| Typed graph entity schema (`Incident`, `Alert`, `Deployment`, `Route`, `Config`, `Policy`) | [WIP] | Shivaganesh | Mock | `docs/SYSTEM_DESIGN_PLAN.md` entity and data-flow sections |

### Mandatory dependency prompt requirements for Step 3.4/3.5
| Prompt purpose | Linked dependency | Required ordering/gate |
|---|---|---|
| Define `RemediationPlan` and policy evaluation contracts against triage output mock | Typed `IncidentHypothesis` | Must precede any real execution-path implementation |
| Build plan/policy/execute logic without competing runtime scaffold | FT-OPS-INFRA-01 | Must consume mock/shared contract only; no competing real bootstrap implementation |
| Define approval pause behavior | approval-gated local endpoint path | Mock contract must exist before execute-flow prompts |

### Dependency readiness verdict
- Verdict: `Ready`

### Blockers
- None. Upstream triage and runtime contracts are explicit enough to mock safely.

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
