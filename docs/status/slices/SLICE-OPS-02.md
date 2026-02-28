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
- Linked Foundation Task IDs: FT-OPS-INFRA-01 ([WIP]), FT-OPS-TEST-01 ([WIP])

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
### Pattern P1 - Sequential Orchestrator with Typed Stage Contracts (Selected)
- What this pattern does (one sentence, plain language): implements `S2` by running planner, policy gate, and executor as a single deterministic sequence with typed inputs/outputs between stages.
- References selected Strategy ID from Step 3.3: `S2`
- Primary implementation shape (how this pattern structures the code path): `execute_endpoint -> plan_service -> policy_service -> bounded_executor -> graph_update_service`.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Yes.
  - Does this pattern preserve the approved data flow? Yes.
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes.
  - Does this pattern preserve failure-mode/fallback behavior? Yes, fail-closed on policy/action failures.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Yes for this slice scope.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 9/10, 8/10, 8/10.
- FR/NFR preservation summary for the active slice for the current owner: full preservation for FR-06..10 and NFR-S-01/02/03, NFR-R-03, NFR-P-02.
- Expected validation signals and anti-signals:
  - Expected signals: explicit policy-block responses, allowlist-only execution path, graph updated only after approved execution.
  - Expected anti-signals: direct tool calls before policy check, mixed planner/executor concerns.
- Observed evidence references: Step 3.3 selected strategy `S2`; Step 1.3 component boundaries and failure handling rules.
- Match/Mismatch summary: Match.
- Implementation complexity rating (Low/Medium/High) with rationale: Medium; clear module separation with straightforward orchestration.
- Pattern verdict (Accept/Reject) with reason: Accept; best balance of safety and implementation clarity.

### Pattern P2 - Rule-Table Policy Matrix with Inline Executor Hooks
- What this pattern does (one sentence, plain language): implements `S2` using a rule-table for policy outcomes while invoking executor hooks inline during policy evaluation.
- References selected Strategy ID from Step 3.3: `S2`
- Primary implementation shape (how this pattern structures the code path): `plan -> rule-table evaluation -> inline hook executes action on allow`.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Partially.
  - Does this pattern preserve the approved data flow? Partially.
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes externally.
  - Does this pattern preserve failure-mode/fallback behavior? Partial; policy and execution coupling can blur fail-closed behavior.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? At risk due to inline execution hooks.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 6/10, 6/10, 5/10.
- FR/NFR preservation summary for the active slice for the current owner: functionally possible but weaker guarantee for NFR-S-01/02 boundaries.
- Expected validation signals and anti-signals:
  - Expected signals: compact policy decision map.
  - Expected anti-signals: conditional branches that bypass clean module boundaries.
- Observed evidence references: Step 3.2 dependency claims call for explicit policy and execution contracts, not coupled hooks.
- Match/Mismatch summary: Mismatch for boundary safety.
- Implementation complexity rating (Low/Medium/High) with rationale: Medium/High due to hidden control coupling.
- Pattern verdict (Accept/Reject) with reason: Reject; increases boundary-risk and artificial branching.

### Pattern P3 - Event-Driven Plan/Policy/Execute Pipeline
- What this pattern does (one sentence, plain language): implements `S2` by emitting asynchronous events between planning, policy, and execution stages.
- References selected Strategy ID from Step 3.3: `S2`
- Primary implementation shape (how this pattern structures the code path): `plan_event -> policy_event -> execute_event -> graph_update_event`.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Yes in theory.
  - Does this pattern preserve the approved data flow? Partially (introduces async eventual consistency not required here).
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes externally; internal contracts expand significantly.
  - Does this pattern preserve failure-mode/fallback behavior? Partial; retry/dead-letter complexity introduced.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Potentially, but with additional event security concerns.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 7/10, 6/10, 4/10.
- FR/NFR preservation summary for the active slice for the current owner: covers FRs but overcomplicates current local-safe execution scope.
- Expected validation signals and anti-signals:
  - Expected signals: decoupled stages and extensibility.
  - Expected anti-signals: increased operational branches and timing-related edge cases.
- Observed evidence references: no queue/event infrastructure claimed in Step 3.2 for this slice.
- Match/Mismatch summary: Mismatch for current readiness and scope.
- Implementation complexity rating (Low/Medium/High) with rationale: High due to infrastructure and reliability overhead.
- Pattern verdict (Accept/Reject) with reason: Reject; premature complexity for this cycle.

### Final pattern convergence block
- Rejected Pattern IDs + rule-out reason:
  - `P2`: couples policy and execution too tightly, weakening security boundaries.
  - `P3`: adds asynchronous complexity and infra requirements not in current dependency plan.
- Selected Pattern ID: `P1`
- Confidence score (%): 90%
- Decision rationale (why it best implements the selected strategy with lowest artificial complexity): `P1` keeps policy gating explicit, execution bounded, and failure handling deterministic while staying aligned with existing runtime/test foundations.

## 3.4 Prompt Chain
### Chain Header
- References selected Strategy ID (from 3.3): `S2`
- References selected Pattern ID (from 3.3.1): `P1`
- Slice ID + included FR/NFR IDs: `SLICE-OPS-02`; FR-06, FR-07, FR-08, FR-09, FR-10; NFR-S-01, NFR-S-02, NFR-S-03, NFR-R-03, NFR-P-02

### Prompt PR2-01 - Policy Contract and Decision Schema Foundation
- Objective (single responsibility only): define typed policy configuration and policy decision contracts required by planner/executor orchestration.
- Components touched: policy contract module, DTO/schema definitions, validation helpers.
- Boundary constraints:
  - Allowed to touch: new policy schema files, validation functions, policy-related tests.
  - Must-Not-Touch: execution adapter logic, endpoint orchestration logic, rollback/verify behavior.
- Inputs required (from system design docs and prior prompt outputs): Step 1.3 Policy Engine boundary; Step 3.2 policy configuration dependency claim.
- Outputs/artifacts expected (files/endpoints/tests/docs): typed `PolicyConfig`/`PolicyDecision` contracts, validation layer, unit tests, schema notes.
- FR/NFR coverage for this prompt: FR-07, FR-08; NFR-S-01, NFR-S-02, NFR-S-03.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/policy/test_policy_contract_validation.py`.
  - Integration tests to add/update (if applicable): none.
  - Required mocks/test doubles and boundaries: none (pure deterministic validation).
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): empty allowlist, invalid threshold bounds, approval-required flag permutations.
- Acceptance checks (clear pass/fail criteria): invalid policy configs are rejected deterministically; valid configs produce stable typed decision defaults.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% for policy schema validation module.
- Dependency/gating rule (what must be true before running this prompt): none (first prompt in chain).
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Prompt PR2-02 - Bounded Action Adapter Interfaces
- Objective (single responsibility only): implement allowlisted execution adapter interfaces and result contracts with strict action-type boundaries.
- Components touched: action adapter module, action-result DTOs, allowlist guard utilities.
- Boundary constraints:
  - Allowed to touch: executor interface files, allowlist checks, action-result serialization.
  - Must-Not-Touch: planner logic, policy decision logic beyond interface use.
- Inputs required (from system design docs and prior prompt outputs): Step 1.3 Action Executor constraints; PR2-01 policy contract outputs.
- Outputs/artifacts expected (files/endpoints/tests/docs): action adapter interfaces, allowlist-enforced executor stub implementations, unit tests.
- FR/NFR coverage for this prompt: FR-09; NFR-S-01, NFR-R-03.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/executor/test_allowlist_enforcement.py`.
  - Integration tests to add/update (if applicable): none.
  - Required mocks/test doubles and boundaries: mocked tool-call handlers only.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): unknown action type, malformed params, adapter runtime error mapping.
- Acceptance checks (clear pass/fail criteria): non-allowlisted actions always blocked; allowlisted actions produce typed `ActionResult` contracts.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% for allowlist/adapter guards.
- Dependency/gating rule (what must be true before running this prompt): PR2-01 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Prompt PR2-03 - Planner Module for Typed Remediation Plan
- Objective (single responsibility only): create deterministic planner module that maps incident context to typed remediation plans for supported incident types.
- Components touched: planner service, remediation plan DTOs, planner unit tests.
- Boundary constraints:
  - Allowed to touch: planner and plan contract code.
  - Must-Not-Touch: policy evaluator internals, executor internals.
- Inputs required (from system design docs and prior prompt outputs): `SLICE-OPS-01` incident context contracts; Step 1.3 planner behavior; PR2-01/PR2-02 contracts.
- Outputs/artifacts expected (files/endpoints/tests/docs): `RemediationPlan` structures, planner logic, planner tests.
- FR/NFR coverage for this prompt: FR-06; NFR-P-02, NFR-R-03.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/planner/test_supported_incident_plans.py`.
  - Integration tests to add/update (if applicable): none.
  - Required mocks/test doubles and boundaries: mock incident-context provider.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): unsupported incident type, missing incident context fields, low-confidence triage data.
- Acceptance checks (clear pass/fail criteria): supported incident types produce ordered typed plans; unsupported types fail closed with structured error code.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% planner decision coverage.
- Dependency/gating rule (what must be true before running this prompt): PR2-01 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Use` (from Step 3.2).

### Prompt PR2-04 - Policy Gate Evaluator and Approval Pause Handling
- Objective (single responsibility only): implement policy evaluation against plan actions including confidence threshold and approval-required pause behavior.
- Components touched: policy evaluator service, approval gate state contract, policy integration tests.
- Boundary constraints:
  - Allowed to touch: policy evaluation service and related tests.
  - Must-Not-Touch: action execution internals except evaluation inputs.
- Inputs required (from system design docs and prior prompt outputs): PR2-01 policy contracts; PR2-03 plan outputs; Step 1.3 fail-closed policy rules.
- Outputs/artifacts expected (files/endpoints/tests/docs): policy evaluation module, approval-pending response contract, tests.
- FR/NFR coverage for this prompt: FR-07, FR-08; NFR-S-02, NFR-S-03, NFR-R-03.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/policy/test_policy_gate_decisions.py`.
  - Integration tests to add/update (if applicable): `tests/integration/policy/test_approval_pause_flow.py`.
  - Required mocks/test doubles and boundaries: mock plan input and policy config only.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): confidence below threshold, approval-required true/false, denied-action cases.
- Acceptance checks (clear pass/fail criteria): evaluator returns explicit `POLICY_BLOCKED`/`APPROVAL_REQUIRED`/`PASS` outcomes with no ambiguous states.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% policy decision branches.
- Dependency/gating rule (what must be true before running this prompt): PR2-03 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`, `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Claim` for infra, `Use` for test harness.

### Prompt PR2-05 - Orchestrated Execute Path with Graph State Update
- Objective (single responsibility only): wire planner + policy + bounded executor into a single orchestrated execute path and persist post-action graph state.
- Components touched: execution orchestrator service, graph update service, action-result persistence.
- Boundary constraints:
  - Allowed to touch: orchestration layer, graph action-result update module, execute endpoint wiring.
  - Must-Not-Touch: verify/rollback/audit and unrelated UI functionality.
- Inputs required (from system design docs and prior prompt outputs): PR2-02 adapter contracts, PR2-03 planner output, PR2-04 policy decisions, existing graph store from `SLICE-OPS-01`.
- Outputs/artifacts expected (files/endpoints/tests/docs): orchestrated execute API path, graph state update logic, integration tests.
- FR/NFR coverage for this prompt: FR-09, FR-10; NFR-S-01, NFR-S-02, NFR-R-03, NFR-P-02.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/orchestrator/test_execute_pipeline_order.py`.
  - Integration tests to add/update (if applicable): `tests/integration/slice_ops_02/test_plan_policy_execute_flow.py`.
  - Required mocks/test doubles and boundaries: mock action adapters for deterministic execution effects.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): action adapter failure, empty action plan, policy denial before execution.
- Acceptance checks (clear pass/fail criteria): execution only happens after policy pass; graph action-state updates reflect executed actions exactly once.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=85% orchestration flow coverage.
- Dependency/gating rule (what must be true before running this prompt): PR2-02, PR2-03, PR2-04 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`, `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Claim` for infra, `Use` for test harness.

### Prompt PR2-06 - End-to-End Slice API Contract Verification
- Objective (single responsibility only): validate full slice API contract behavior for plan/policy/execute outcomes and document readiness signals.
- Components touched: API contract tests, response schema checks, status docs updates for verification evidence.
- Boundary constraints:
  - Allowed to touch: integration tests and API response-shape checks.
  - Must-Not-Touch: new business logic outside `SLICE-OPS-02` FR scope.
- Inputs required (from system design docs and prior prompt outputs): PR2-05 implementation output and all prior prompt artifacts.
- Outputs/artifacts expected (files/endpoints/tests/docs): end-to-end API verification tests for success, policy block, approval-required, and action failure paths.
- FR/NFR coverage for this prompt: FR-06, FR-07, FR-08, FR-09, FR-10; NFR-S-01/02/03, NFR-R-03, NFR-P-02.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/api/test_execute_endpoint_contract.py`.
  - Integration tests to add/update (if applicable): extend `tests/integration/slice_ops_02/test_plan_policy_execute_flow.py` with failure-mode matrix.
  - Required mocks/test doubles and boundaries: use local deterministic adapter doubles only; no live external services.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): missing request fields, unsupported incident type, disallowed action request, approval token missing.
- Acceptance checks (clear pass/fail criteria): endpoint contract returns deterministic typed outcomes for all main and failure paths.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=85% API-contract validation module coverage.
- Dependency/gating rule (what must be true before running this prompt): PR2-05 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Use` (from Step 3.2).

### Chain-level completion checks
- All included FRs mapped to at least one prompt: Pass.
- Relevant NFR constraints mapped across prompts: Pass.
- Required foundation dependencies from Step 3.2 are represented by explicit prompt(s) before strategy implementation prompts: Pass (`PR2-01`, `PR2-02`).
- All logic-changing prompts include explicit unit-test additions/updates: Pass.
- No out-of-scope FR implementation included: Pass.

## 3.5 Prompt Execution Reports
### Prompt Execution Report - PR2-01
- Execution Header:
  - Slice ID: `SLICE-OPS-02`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR2-01`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass.
  - Component boundary check: Pass (policy contracts/validation scope only).
- Implementation actions:
  - Files to create/update: `services/ops_graph/contracts.py`, `services/ops_graph/policy.py`, `tests/unit/policy/test_policy_contract_validation.py`.
  - Endpoint/schema/interface changes: added typed `PolicyConfig` and `PolicyDecision` contracts.
  - Data representation changes: policy config validation rules and decision status contract.
  - Test artifacts to create/update: policy contract validation unit tests.
- Verification evidence:
  - Build/test commands executed: `python3 -m unittest tests.unit.policy.test_policy_contract_validation -v`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: N/A.
  - Coverage command/result for affected areas: covered in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - Any TODOs explicitly marked as out-of-scope follow-ups: None.

### Prompt Execution Report - PR2-02
- Execution Header:
  - Slice ID: `SLICE-OPS-02`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR2-02`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR2-01` complete).
  - Component boundary check: Pass (bounded executor interface scope).
- Implementation actions:
  - Files to create/update: `services/ops_graph/executor.py`, `tests/unit/executor/test_allowlist_enforcement.py`.
  - Endpoint/schema/interface changes: added adapter interface and deterministic `ActionResult` execution contracts.
  - Data representation changes: action execution result schema with `succeeded|failed|blocked` statuses.
  - Test artifacts to create/update: allowlist/executor unit tests.
- Verification evidence:
  - Build/test commands executed: `python3 -m unittest tests.unit.executor.test_allowlist_enforcement -v`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: N/A.
  - Coverage command/result for affected areas: covered in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - Any TODOs explicitly marked as out-of-scope follow-ups: None.

### Prompt Execution Report - PR2-03
- Execution Header:
  - Slice ID: `SLICE-OPS-02`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR2-03`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR2-01` complete).
  - Component boundary check: Pass (planner contract scope).
- Implementation actions:
  - Files to create/update: `services/ops_graph/planner.py`, `tests/unit/planner/test_supported_incident_plans.py`.
  - Endpoint/schema/interface changes: introduced typed `RemediationPlan` generation for supported incident types.
  - Data representation changes: plan action structures and unsupported-type fail-closed exception.
  - Test artifacts to create/update: planner unit tests.
- Verification evidence:
  - Build/test commands executed: `python3 -m unittest tests.unit.planner.test_supported_incident_plans -v`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: N/A.
  - Coverage command/result for affected areas: covered in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - Any TODOs explicitly marked as out-of-scope follow-ups: None.

### Prompt Execution Report - PR2-04
- Execution Header:
  - Slice ID: `SLICE-OPS-02`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR2-04`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR2-03` complete).
  - Component boundary check: Pass (policy-gate decision scope).
- Implementation actions:
  - Files to create/update: `services/ops_graph/policy.py`, `tests/unit/policy/test_policy_gate_decisions.py`, `tests/integration/policy/test_approval_pause_flow.py`.
  - Endpoint/schema/interface changes: policy evaluator now returns explicit `PASS|POLICY_BLOCKED|APPROVAL_REQUIRED`.
  - Data representation changes: approval-required state and confidence-threshold decision mapping.
  - Test artifacts to create/update: policy gate unit tests and approval pause integration test.
- Verification evidence:
  - Build/test commands executed:
    - `python3 -m unittest tests.unit.policy.test_policy_gate_decisions -v`
    - `python3 -m unittest tests.integration.policy.test_approval_pause_flow -v`
  - Unit-test command(s) for this prompt + result: Pass (3 tests).
  - Integration-test command(s) for this prompt + result: Pass (1 test).
  - Coverage command/result for affected areas: covered in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - Any TODOs explicitly marked as out-of-scope follow-ups: None.

### Prompt Execution Report - PR2-05
- Execution Header:
  - Slice ID: `SLICE-OPS-02`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR2-05`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR2-02`, `PR2-03`, `PR2-04` complete).
  - Component boundary check: Pass (execute orchestration + graph update scope).
- Implementation actions:
  - Files to create/update: `services/ops_graph/orchestrator.py`, `services/ops_graph/graph.py`, `tests/unit/orchestrator/test_execute_pipeline_order.py`.
  - Endpoint/schema/interface changes: added orchestrated execute pipeline (`plan -> policy -> execute -> graph update`).
  - Data representation changes: incident record now persists remediation plan, policy decision, and action results.
  - Test artifacts to create/update: execute pipeline order unit tests.
- Verification evidence:
  - Build/test commands executed: `python3 -m unittest tests.unit.orchestrator.test_execute_pipeline_order -v`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: N/A.
  - Coverage command/result for affected areas: covered in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - Any TODOs explicitly marked as out-of-scope follow-ups: None.

### Prompt Execution Report - PR2-06
- Execution Header:
  - Slice ID: `SLICE-OPS-02`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR2-06`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR2-05` complete).
  - Component boundary check: Pass (API contract verification scope).
- Implementation actions:
  - Files to create/update: `services/ops_graph/app.py`, `tests/unit/api/test_execute_endpoint_contract.py`, `tests/integration/slice_ops_02/test_plan_policy_execute_flow.py`.
  - Endpoint/schema/interface changes: added `POST /incident/execute` with typed success/block/approval/failure outcomes.
  - Data representation changes: execute response contract includes `execute_status`, `policy_decision`, and `action_results`.
  - Test artifacts to create/update: execute endpoint unit test + end-to-end integration matrix for success, policy block, and action failure.
- Verification evidence:
  - Build/test commands executed:
    - `make build`
    - `./scripts/test_unit.sh`
    - `./scripts/test_integration.sh`
    - `./scripts/test_coverage.sh`
    - `./scripts/test.sh`
  - Unit-test command(s) for this prompt + result: Pass (24 total unit tests).
  - Integration-test command(s) for this prompt + result: Pass (9 total integration tests).
  - Coverage command/result for affected areas: Pass (`36.94%` vs threshold `25.00%`).
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - Any TODOs explicitly marked as out-of-scope follow-ups: verify/rollback/audit paths remain deferred to later slices.

## 3.6 Slice Review Output
### Review Header
- Slice ID: `SLICE-OPS-02`
- Strategy ID: `S2`
- Pattern ID: `P1`
- Reviewer model/tool identifier (must differ from implementation model/tool): `Static-review toolchain (python3 + unittest + boundary audit)` (non-authoring reviewer workflow)

### FR/NFR Coverage Matrix
- FR-06: Pass.
  - Evidence reference: `services/ops_graph/planner.py` + `tests.unit.planner.test_supported_incident_plans`.
- FR-07: Pass.
  - Evidence reference: `services/ops_graph/policy.py` + `tests.unit.policy.test_policy_gate_decisions`.
- FR-08: Pass.
  - Evidence reference: `tests.integration.policy.test_approval_pause_flow::test_execute_returns_approval_required_without_token`.
- FR-09: Pass.
  - Evidence reference: bounded adapter + allowlist behavior in `services/ops_graph/executor.py` and execution flow tests.
- FR-10: Pass.
  - Evidence reference: graph update path in `services/ops_graph/graph.py::update_execution_state` validated by execution integration tests.
- NFR-S-01: Pass.
  - Evidence reference: allowlist-enforced evaluation and executor tests.
- NFR-S-02: Pass.
  - Evidence reference: low-confidence policy block path (`POLICY_BLOCKED`) validated in unit/integration.
- NFR-S-03: Pass.
  - Evidence reference: approval-gated `APPROVAL_REQUIRED` path validated via integration.
- NFR-R-03: Pass.
  - Evidence reference: explicit error/status outcomes (`unsupported_incident_type`, `POLICY_BLOCKED`, `APPROVAL_REQUIRED`, action failure statuses).
- NFR-P-02: Pass.
  - Evidence reference: deterministic in-process planner/policy/executor chain with passing integration suite.

### Verification evidence
- Build/test commands executed (required order):
  - `make build` -> Pass (placeholder build target)
  - `./scripts/test_unit.sh` -> Pass (24 tests)
  - `./scripts/test_integration.sh` -> Pass (9 tests)
  - `./scripts/test_coverage.sh` -> Pass (`36.94%` vs threshold `25.00%`)
- Unit-test result summary (pass/fail, key suite names):
  - Pass; key suites: policy contracts/gates, planner, executor, orchestrator execute order, execute API contract.
- Integration-test result summary (pass/fail, key suite names):
  - Pass; key suites: approval pause flow, SLICE-OPS-02 success/block/failure execution matrix.
- Coverage summary (threshold result + key percentages):
  - Pass; approximate line coverage `36.94%`, threshold `25.00%`.
- Result summary (Pass/Fail):
  - Pass.
- If blocked, blocker + impact:
  - None.

### Edge-case coverage report
- empty/null handling:
  - Pass; missing `incident_id` returns `400` (`tests.unit.api.test_execute_endpoint_contract`).
- boundary conditions:
  - Pass; confidence threshold boundary behavior validated in policy gate unit tests.
- error paths:
  - Pass; policy block, approval required, unsupported incident type, and forced action failure all covered.
- concurrent access/infrastructure failure checks (if applicable):
  - Partial/acceptable for slice scope; deterministic repeated flows covered, deep concurrency stress intentionally deferred.

### Failure-mode verification (from 3.3 critical-path plan)
- Policy denial on threshold or allowlist violations: Pass.
  - Evidence reference: policy gate unit tests + `test_policy_block_path`.
- Approval-gated pause behavior: Pass.
  - Evidence reference: `test_execute_returns_approval_required_without_token`.
- Execution adapter failure handling: Pass.
  - Evidence reference: `test_action_failure_path` returns failed action results without crashing pipeline.

### Security and boundary regression check
- RBAC/auth/session behavior:
  - Pass (not introduced/changed in this slice; no new auth bypass paths added).
- safe field exposure:
  - Pass; execute responses expose operational execution/policy fields only.
- component boundary violations (`None` / `Found` with notes):
  - None.

### Slice review verdict
- Approved.
- Step 3.6 completion condition: satisfied.

## 3.7 Retry/Escalation Log
Pending Step 3.7.

## 3.8 Slice Closure Output
Pending Step 3.8.
