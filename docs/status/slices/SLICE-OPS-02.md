# SLICE-OPS-02

## Metadata
- Slice ID: SLICE-OPS-02
- Capability: Policy-gated remediation planning and bounded execution.
- Owner: anajaramillo
- Included FR IDs: FR-06, FR-07, FR-08, FR-09, FR-10
- Relevant NFR IDs: NFR-S-01, NFR-S-02, NFR-S-03, NFR-R-03, NFR-P-02
- Status: [WIP]
- Start Gate: [WIP] (activated in Step 3.1 during Step 4.0 repeat cycle)
- Demo/Test Condition: System generates typed remediation plans, enforces policy gates, and executes only allowlisted actions with graph-state updates.
- Linked Foundation Task IDs: FT-OPS-INFRA-01 ([WIP])

## 3.1 Planning and Activation Output
### Candidate slice set context
- Prior slice (`SLICE-OPS-01`) is complete and closed through Step 3.8.
- Remaining planned slices from registry:
  - `SLICE-OPS-02` (policy-gated plan + execute)
  - `SLICE-OPS-03` (verify + rollback + audit + visibility)

### Activation decision
- Activated slice: `SLICE-OPS-02`
- Reason: directly follows completed triage slice and delivers the next required pipeline capability (plan + policy + bounded execution).
- Owner: anajaramillo (solo mode)
- Status transition: `[Planned]` -> `[WIP]`

## 3.2 Dependency Output
### Dependency header
- Slice ID: `SLICE-OPS-02`

### Physical dependency list
| Resource | Required capability | Status | Handling decision | Owner |
|---|---|---|---|---|
| Existing incident graph state from `SLICE-OPS-01` | Read typed incident/hypothesis context before plan/execute | Available | Use | anajaramillo |
| Policy configuration contract | Enforce allowlist, confidence threshold, approval gating | Missing | Claim | anajaramillo |
| Execution tool adapter layer | Execute only bounded allowlisted actions and persist action results | Missing | Claim | anajaramillo |
| Local runtime/API scaffold (`services/ops_graph`) | Host planning/execution endpoints locally | Available | Use | anajaramillo |

### Shared dependency list
| Task ID | Current status | Owner | Handling decision | Interface contract reference | Foundation Detail File |
|---|---|---|---|---|---|
| FT-OPS-INFRA-01 | [WIP] | anajaramillo | Claim | Extend runtime plumbing for policy + execution boundaries and action adapters | `docs/status/foundation/FT-OPS-INFRA-01.md` |
| FT-OPS-TEST-01 | [WIP] | anajaramillo | Use | Reuse deterministic test harness and coverage gate for new policy/execute tests | `docs/status/foundation/FT-OPS-TEST-01.md` |

### Mandatory dependency prompt requirements for Step 3.4/3.5
| Prompt purpose | Linked dependency | Required ordering/gate |
|---|---|---|
| Add policy contract schema and gate evaluator | Physical: Policy configuration contract | Must run before plan/execution strategy prompts |
| Add bounded action adapter interfaces | Physical: Execution tool adapter layer | Must run before execution logic prompts |
| Extend shared runtime plumbing for policy/execute flow | FT-OPS-INFRA-01 | Must run before strategy implementation prompts |
| Reuse deterministic test harness for policy/execute validations | FT-OPS-TEST-01 | Must run before logic-changing prompts |

### Dependency readiness verdict
- Verdict: `Ready`

### Blockers
- None at Step 3.2. Missing dependencies are explicitly claimed with owner and foundation reference.

## 3.3 Strategy Evaluation + Final Convergence
Pending Step 3.3.

## 3.3.1 Pattern Evaluation + Final Convergence
Pending Step 3.3.1.

## 3.4 Prompt Chain
Pending Step 3.4.

## 3.5 Prompt Execution Reports
Pending Step 3.5.

## 3.6 Slice Review Output
Pending Step 3.6.

## 3.7 Retry/Escalation Log
Pending Step 3.7.

## 3.8 Slice Closure Output
Pending Step 3.8.
