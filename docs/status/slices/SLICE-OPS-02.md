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
### Strategy S1 - Inline Policy+Execution in Endpoint
- What this strategy does (one sentence, plain language): puts remediation planning, policy checks, and allowlisted action execution directly inside one API endpoint handler.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): Walker Pipeline boundaries, Policy Engine responsibilities, Action Executor responsibilities, data-flow path.
- Components touched: incident API controller, policy checks, action executor calls, graph updates.
- Boundary check per component:
  - Owns: endpoint orchestration only.
  - Must-Not-Do: endpoint should not absorb policy/action domain logic permanently.
- Primary implementation locus: `POST /incident/execute` endpoint function body.
- Data flow across components (request/response/persistence path): request -> inline plan creation -> inline policy gate -> inline action execution -> graph write -> response.
- Data representation impact (schemas, payload fields, indexes, validation): introduces mixed request/plan/action payload schema with tight coupling.
- Communication contract impact:
  - input JSON shape changes: adds remediation request body with policy hints.
  - output JSON shape changes: returns plan + policy + action results in one payload.
  - backward-compatibility notes: additive, but unstable contract boundaries.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: policy denial / low confidence / disallowed action.
  - error response behavior: deny execution and return explicit policy block.
  - fallback/degraded behavior: no action, incident remains active.
- FR ownership coverage map:
  - FR-06, FR-07, FR-08, FR-09, FR-10 mapped but tightly co-located.
- Slice coverage completeness check: complete but with poor separation.
- Expected evidence map:
  - Positive signals: fast delivery with single code path.
  - Absent signals: modular policy engine boundaries.
  - Trigger behavior: immediate response for plan+execute requests.
- Observed evidence references: existing single-service baseline from `SLICE-OPS-01`.
- Match/Mismatch summary: Mismatch with Step 1.3 component boundaries.
- Cloud/Infra feasibility check: feasible locally but high long-term maintenance risk.
- NFR mapping: risks NFR-R-03 error-contract clarity and NFR-S controls maintainability.
- Risk and complexity rating (Low/Medium/High) with rationale: Medium complexity, High boundary risk.
- Strategy verdict (Accept/Reject) with reason: Reject; violates clean policy/action separation.

### Strategy S2 - Split Plan/Policy/Execute Modules Behind Orchestrator (Selected)
- What this strategy does (one sentence, plain language): adds a dedicated orchestration path that composes distinct planner, policy-gate, and bounded action-executor modules.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): Policy Engine, Action Executor, Walker Pipeline, fail-closed boundaries.
- Components touched: plan module, policy module, execute module, incident orchestration API, graph state updater.
- Boundary check per component:
  - Owns: each module owns only its single responsibility.
  - Must-Not-Do: policy module does not generate actions; executor does not bypass allowlist.
- Primary implementation locus: orchestration pipeline `plan -> policy_gate -> execute_if_allowed -> persist_results`.
- Data flow across components (request/response/persistence path): incident context -> typed remediation plan -> policy evaluation -> conditional action execution -> graph updates + action result response.
- Data representation impact (schemas, payload fields, indexes, validation): typed `RemediationPlan`, `PolicyDecision`, and `ActionResult` contracts.
- Communication contract impact:
  - input JSON shape changes: execute-trigger request references incident and optional approval token.
  - output JSON shape changes: structured plan, policy decision, and execution results.
  - backward-compatibility notes: additive, preserves SLICE-OPS-01 contracts.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: policy blocked / approval required / action failure.
  - error response behavior: explicit policy/error codes with no unauthorized action.
  - fallback/degraded behavior: retain incident as active, require supervised continuation.
- FR ownership coverage map:
  - FR-06 -> planner module
  - FR-07 -> policy evaluator
  - FR-08 -> approval-gate handling
  - FR-09 -> bounded executor
  - FR-10 -> post-action graph state update module
- Slice coverage completeness check: complete across all included FRs and NFRs.
- Expected evidence map:
  - Positive signals: clear policy-block responses, allowlist-only execution, action results persisted.
  - Absent signals: direct tool calls from non-executor modules.
  - Trigger behavior: execution proceeds only when policy gate passes.
- Observed evidence references: `SLICE-OPS-01` typed graph/orchestration baseline and `FT-OPS-INFRA-01` dependency claims.
- Match/Mismatch summary: Match with architecture boundaries and safety constraints.
- Cloud/Infra feasibility check: high feasibility in current local runtime with existing foundation tasks.
- NFR mapping: strongest fit for NFR-S-01/02/03, NFR-R-03, and NFR-P-02.
- Risk and complexity rating (Low/Medium/High) with rationale: Medium complexity, Low/Medium risk with strong modularity.
- Strategy verdict (Accept/Reject) with reason: Accept; best architecture-conformant and safety-aligned option.

### Strategy S3 - External Policy Service First
- What this strategy does (one sentence, plain language): offloads policy evaluation and approval handling to a separate external service before local execution.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): Policy Engine responsibilities and execution gating.
- Components touched: external policy adapter, local planner/executor, remote-policy client.
- Boundary check per component:
  - Owns: external policy checks.
  - Must-Not-Do: executor cannot run on remote errors/unknown decisions.
- Primary implementation locus: remote call gateway before action execution.
- Data flow across components (request/response/persistence path): local plan -> remote policy decision -> local execute -> graph update.
- Data representation impact (schemas, payload fields, indexes, validation): adds remote policy request/response schema and error handling.
- Communication contract impact:
  - input JSON shape changes: additional remote policy context fields.
  - output JSON shape changes: includes remote decision metadata.
  - backward-compatibility notes: introduces external dependency contracts not currently present.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: remote policy timeout/unavailable.
  - error response behavior: fail closed, no execution.
  - fallback/degraded behavior: manual approval path only.
- FR ownership coverage map:
  - FR-06..10 all covered but operationally dependent on external service.
- Slice coverage completeness check: functionally complete, operationally heavy for current stage.
- Expected evidence map:
  - Positive signals: central policy governance.
  - Absent signals: local-only resilience.
  - Trigger behavior: execution blocked on any remote policy failure.
- Observed evidence references: no external policy service in current bootstrap/foundation state.
- Match/Mismatch summary: Mismatch for current infra readiness and timeline.
- Cloud/Infra feasibility check: low near-term feasibility.
- NFR mapping: improves future governance but threatens NFR-P-02 responsiveness in local demo environment.
- Risk and complexity rating (Low/Medium/High) with rationale: High risk and integration complexity.
- Strategy verdict (Accept/Reject) with reason: Reject; premature external dependency.

### Final convergence block
- Rejected Strategy IDs + rule-out reason:
  - `S1`: insufficient component separation and policy/execution coupling.
  - `S3`: requires external policy infrastructure unavailable in current cycle.
- Selected Strategy ID: `S2`
- Confidence score (%): 89%
- Decision rationale (why it best fits full slice behavior): `S2` preserves policy safety boundaries, supports explicit approval gating, and cleanly maps FR-06..10 with current foundation readiness.
- Architecture conformance statement: selected strategy preserves Step 1.3 boundaries, fail-closed behavior, typed contracts, and allowlist-only execution constraints.

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
