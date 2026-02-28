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
### Strategy S1 - Inline Endpoint Orchestration
- What this strategy does (one sentence, plain language): implement planning, policy checks, approval pause handling, and bounded execution directly inside one HTTP endpoint path in `main.jac`.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): Walker Pipeline separation (`plan_walker`, Policy Engine, `execute_walker`), component must-not boundaries, communication contracts (`/walker/incident_state` + approval flow), failure-mode table for policy block/low confidence/execution failure.
- External source references used:
  - `docs/SYSTEM_DESIGN_PLAN.md`
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Components touched:
  - `main.jac` endpoint handlers
  - Policy evaluation logic
  - action execution wrappers
- Boundary check per component:
  - Owns: request orchestration and response assembly.
  - Must-Not-Do: bypass allowlist/approval gates; mutate unrelated verification/rollback/audit behavior (owned by `SLICE-OPS-03`).
- Primary implementation locus (where this strategy places core behavior: component/path/state transition): one API orchestration path from incident state fetch -> plan compute -> policy gate -> execute -> graph update.
- Data flow across components (request/response/persistence path): incident request -> inline plan generation -> inline policy decision -> inline allowlisted action calls -> write `ActionResult` + updated deployment/route state -> response payload.
- Data representation impact (schemas, payload fields, indexes, validation): `RemediationPlan` and `ActionResult` schemas introduced but tightly coupled to endpoint payload shape.
- Communication contract impact:
  - input JSON shape changes: single execute call must carry approval token and execution options.
  - output JSON shape changes: mixed planning/policy/execution payload.
  - backward-compatibility notes: high coupling risk if downstream slices need stage-level payload separation.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: policy denial or low confidence.
  - error response behavior: return `POLICY_BLOCKED` / `LOW_CONFIDENCE` and no actions executed.
  - fallback/degraded behavior: pause for manual review/approval.
- FR ownership coverage map:
  - FR-06 -> inline plan creation branch
  - FR-07 -> inline policy branch
  - FR-08 -> inline approval pause branch
  - FR-09 -> inline allowlisted action branch
  - FR-10 -> inline graph-update branch
- Slice coverage completeness check:
  - all included FRs mapped: Yes.
  - relevant NFRs addressed: partially; harder to keep strict S/R boundaries as logic grows.
- Expected evidence map:
  - Positive signals: rapid prototype, minimal files changed.
  - Absent signals: clean stage boundaries and reusable contracts.
  - Trigger behavior: one call attempts full plan->execute flow.
- Observed evidence references: Step `3.2` notes explicit mock contracts for upstream triage schema and shared runtime; design doc expects separated walker responsibilities.
- Match/Mismatch summary: Mismatch with Step 1.3 component separation and maintainability expectations.
- Cloud/Infra feasibility check: feasible locally, but poor fit for collaborative parallel ownership.
- NFR mapping: weak fit for `NFR-S-01/02/03` and `NFR-R-03` clarity as complexity increases.
- Risk and complexity rating (Low/Medium/High) with rationale: Medium implementation effort, High contract/regression risk.
- Strategy verdict (Accept/Reject) with reason: Reject; violates preferred modular boundaries and increases cross-slice collision risk.

### Strategy S2 - Split Plan/Policy/Execute Modules Behind Orchestrator (Selected)
- What this strategy does (one sentence, plain language): implement a staged Jac flow where `plan_walker` produces typed plan output, policy gate evaluates constraints, and `execute_walker` applies only allowlisted actions with explicit state updates.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): component responsibilities for Policy Engine and Action Executor; bounded walker sequence (`plan_walker` -> policy check -> `execute_walker`); failure-mode contracts for policy denial/approval gate/execution failure.
- External source references used:
  - `docs/SYSTEM_DESIGN_PLAN.md`
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Components touched:
  - `main.jac` walker definitions and typed objects
  - policy decision contract module/section
  - bounded action adapter functions
- Boundary check per component:
  - Owns: FR-06..10 orchestration, policy enforcement, bounded execution, post-action graph mutation.
  - Must-Not-Do: implement verification/rollback/audit outputs (reserved for `SLICE-OPS-03`); replace shared runtime plumbing owned by `FT-OPS-INFRA-01`.
- Primary implementation locus (where this strategy places core behavior: component/path/state transition): dedicated stage transitions: hypothesis -> `RemediationPlan` -> policy decision -> action results -> incident state mutation.
- Data flow across components (request/response/persistence path): read mocked `IncidentHypothesis` -> create typed `RemediationPlan` -> evaluate policy allowlist/threshold/approval -> execute allowlisted actions -> persist `ActionResult` and deployment/route updates -> expose execution status in incident state contract.
- Data representation impact (schemas, payload fields, indexes, validation): explicit typed contracts for `RemediationPlan`, policy decision state (`PASS`/`POLICY_BLOCKED`/`APPROVAL_REQUIRED`), and `ActionResult`.
- Communication contract impact:
  - input JSON shape changes: explicit execute request with `incident_id` and optional `approval_token`.
  - output JSON shape changes: staged execution response includes plan, policy decision, and action results.
  - backward-compatibility notes: additive to current bootstrap contracts and aligned to Step 1.3.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: action not allowlisted, low confidence, approval missing, adapter failure.
  - error response behavior: deterministic typed status + no unsafe action.
  - fallback/degraded behavior: manual-review/approval-required state with clear error contract.
- FR ownership coverage map:
  - FR-06 -> `plan_walker` typed plan generation path
  - FR-07 -> policy evaluation stage (allowlist/threshold/approval)
  - FR-08 -> approval-gated pause + approval endpoint contract
  - FR-09 -> execute stage restricted to hardcoded allowlist
  - FR-10 -> graph updates after each action result
- Slice coverage completeness check:
  - all included FRs mapped: Yes.
  - all relevant NFRs mapped: Yes (`NFR-S-01/02/03`, `NFR-R-03`, `NFR-P-02`).
- Expected evidence map:
  - Positive signals: clear stage outputs, deterministic policy gate behavior, explicit action/result contracts.
  - Absent signals: out-of-scope verify/rollback logic.
  - Trigger behavior: `execute` transitions only after policy pass or explicit approval.
- Observed evidence references: Step `3.2` dependencies explicitly marked `Mock` for upstream triage contracts and shared infra; this strategy consumes those contracts without competing implementations.
- Match/Mismatch summary: Match with architecture contracts, collaborative ownership model, and non-competing dependency rule.
- Cloud/Infra feasibility check: high; runs in existing Jac runtime and local mock vLLM setup.
- NFR mapping: strongest fit across security and reliability constraints while maintaining performance for demo.
- Risk and complexity rating (Low/Medium/High) with rationale: Medium complexity, Low-to-medium integration risk due to explicit boundaries.
- Strategy verdict (Accept/Reject) with reason: Accept; best aligned with Step 1.3 separation and collaborative slice execution.

### Strategy S3 - Event-Queue Mediated Execution
- What this strategy does (one sentence, plain language): model planning and execution as queued jobs, with policy and execution processed asynchronously by worker handlers.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): sequential walker pipeline assumptions, API polling contract, local runtime stack assumptions.
- External source references used:
  - `docs/SYSTEM_DESIGN_PLAN.md`
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Components touched:
  - queue dispatcher/runtime worker layer
  - async execution tracking state
  - API polling/status contracts
- Boundary check per component:
  - Owns: asynchronous dispatch semantics.
  - Must-Not-Do: break deterministic policy-before-action guarantee or introduce undeclared infra ownership.
- Primary implementation locus (where this strategy places core behavior: component/path/state transition): async queue between planning and execution stages.
- Data flow across components (request/response/persistence path): request -> enqueue plan job -> worker evaluates policy -> worker executes actions -> async status projection updates.
- Data representation impact (schemas, payload fields, indexes, validation): requires queue job schema, retry metadata, and additional status states.
- Communication contract impact:
  - input JSON shape changes: enqueue-style execute request.
  - output JSON shape changes: job token/status polling instead of immediate stage result.
  - backward-compatibility notes: significant contract shift vs current design baseline.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: queue delay, worker timeout, duplicate job replay.
  - error response behavior: retry/dead-letter style statuses.
  - fallback/degraded behavior: manual intervention and queue replay handling.
- FR ownership coverage map:
  - FR-06..10 can be mapped, but with additional async state complexity not required by current slice scope.
- Slice coverage completeness check:
  - all included FRs mapped: theoretically yes.
  - relevant NFRs addressed: mixed; risks `NFR-P-02` in local demo environment.
- Expected evidence map:
  - Positive signals: decoupled execution scaling.
  - Absent signals: simple deterministic local flow.
  - Trigger behavior: eventual consistency via queue processing.
- Observed evidence references: no queue infra is claimed in Step `3.2`; workflow warns against introducing competing shared infrastructure outside ownership contracts.
- Match/Mismatch summary: Mismatch for current scope and infrastructure assumptions.
- Cloud/Infra feasibility check: low in current repo state (no queue scaffolding in active dependencies).
- NFR mapping: can satisfy security constraints but threatens performance/demo simplicity.
- Risk and complexity rating (Low/Medium/High) with rationale: High complexity and coordination risk.
- Strategy verdict (Accept/Reject) with reason: Reject; over-scoped and misaligned with current dependency/infra baseline.

### Final convergence block
- Rejected Strategy IDs + rule-out reason:
  - `S1`: rejected for boundary coupling and higher regression risk.
  - `S3`: rejected for undeclared async infrastructure complexity and contract drift.
- Selected Strategy ID: `S2`
- Confidence score (%): 92%
- Decision rationale (why it best fits full slice behavior): `S2` cleanly maps FR-06..10 with explicit stage contracts, preserves security/reliability NFRs, and respects collaborative ownership by consuming Step `3.2` mocks/contracts instead of implementing competing dependencies.
- Architecture conformance statement:
  - Selected strategy preserves Step 1.3 component boundaries, ordered data flow, communication contracts, failure handling, and Jac/Jaseci load-bearing runtime choices.

## 3.3.1 Pattern Evaluation + Final Convergence
### Pattern P1 - Sequential Stage Handlers with Typed Contracts (Selected)
- What this pattern does (one sentence, plain language): implement `S2` with explicit stage handlers (`plan`, `policy`, `execute`) that exchange typed records and update state in one deterministic sequence.
- References selected Strategy ID from Step 3.3: `S2`
- External source references used:
  - `docs/SYSTEM_DESIGN_PLAN.md`
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Primary implementation shape (how this pattern structures the code path): `plan_walker` emits `RemediationPlan` -> policy evaluator emits decision (`PASS`/`POLICY_BLOCKED`/`APPROVAL_REQUIRED`) -> `execute_walker` runs allowlisted actions -> graph state updated per action result.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Yes.
  - Does this pattern preserve the approved data flow? Yes.
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes, additive staged response fields.
  - Does this pattern preserve failure-mode/fallback behavior? Yes, explicit typed error states and approval pause behavior.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Yes for slice scope; only allowlisted action exposure.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 9/10, 8/10, 8/10.
- FR/NFR preservation summary for the active slice for the current owner: full FR-06..10 coverage with strong NFR-S-01/02/03, NFR-R-03, NFR-P-02 alignment.
- Expected validation signals and anti-signals:
  - Expected signals: single ordered flow, deterministic policy outcomes, typed action results, explicit pause path.
  - Expected anti-signals: duplicated policy checks in execute stage, hidden action side effects.
- Observed evidence references: Step `3.2` mock dependencies and Step `3.3` strategy `S2` selected for boundary-safe staged orchestration.
- Match/Mismatch summary: Match.
- Implementation complexity rating (Low/Medium/High) with rationale: Medium; straightforward staged composition with explicit contracts.
- Pattern verdict (Accept/Reject) with reason: Accept; best fit with lowest artificial complexity and strongest boundary preservation.

### Pattern P2 - Rule Matrix Controller
- What this pattern does (one sentence, plain language): implement `S2` using one central rule matrix that maps incident/policy states to action and graph update decisions.
- References selected Strategy ID from Step 3.3: `S2`
- External source references used:
  - `docs/SYSTEM_DESIGN_PLAN.md`
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Primary implementation shape (how this pattern structures the code path): a controller table evaluates all policy/execution conditions and dispatches action handlers based on matrix entries.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Partially.
  - Does this pattern preserve the approved data flow? Partially; policy and execution concerns are merged in controller logic.
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes externally, but internal mapping is less explicit.
  - Does this pattern preserve failure-mode/fallback behavior? Partial; harder to trace which rule emitted a fallback state.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Partial; allowlist logic is embedded in matrix entries.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 6/10, 5/10, 4/10.
- FR/NFR preservation summary for the active slice for the current owner: functional FR coverage possible, but weaker NFR-S and NFR-R clarity due to matrix complexity.
- Expected validation signals and anti-signals:
  - Expected signals: centralized decision table.
  - Expected anti-signals: opaque branching and increased debugging overhead.
- Observed evidence references: workflow and architecture emphasize explicit stage ownership and deterministic contracts, not large rule matrices.
- Match/Mismatch summary: Mismatch due to artificial complexity.
- Implementation complexity rating (Low/Medium/High) with rationale: High; branching and test matrix grow quickly.
- Pattern verdict (Accept/Reject) with reason: Reject; increases artificial complexity without clear architectural benefit.

### Pattern P3 - Split Async Stage Queue
- What this pattern does (one sentence, plain language): implement `S2` with asynchronous stage queues where plan, policy, and execute stages run as separate queued workers.
- References selected Strategy ID from Step 3.3: `S2`
- External source references used:
  - `docs/SYSTEM_DESIGN_PLAN.md`
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Primary implementation shape (how this pattern structures the code path): enqueue stage jobs and process them asynchronously with projected incident state updates.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Yes in theory.
  - Does this pattern preserve the approved data flow? Partially; introduces eventual-consistency timing not required by current design phase.
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? No, requires job-token and polling contract changes.
  - Does this pattern preserve failure-mode/fallback behavior? Partial; queue timeout/retry states add new failure classes.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Potentially, but requires extra queue authorization controls.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 7/10, 6/10, 3/10.
- FR/NFR preservation summary for the active slice for the current owner: can cover FRs, but weakens NFR-P-02 and operational simplicity goals.
- Expected validation signals and anti-signals:
  - Expected signals: decoupled worker scalability.
  - Expected anti-signals: additional infra contracts and harder deterministic testing.
- Observed evidence references: Step `3.2` has no queue dependency claimed and local Jac bootstrap favors direct staged flow.
- Match/Mismatch summary: Mismatch for current dependency and phase constraints.
- Implementation complexity rating (Low/Medium/High) with rationale: High; introduces out-of-scope infrastructure and contract churn.
- Pattern verdict (Accept/Reject) with reason: Reject; not justified for current slice objectives and collaboration constraints.

### Final pattern convergence block
- Rejected Pattern IDs + rule-out reason:
  - `P2`: rejected due to high artificial branching complexity and weaker policy/audit traceability.
  - `P3`: rejected due to async/infra overhead and communication contract drift.
- Selected Pattern ID: `P1`
- Confidence score (%): 93%
- Decision rationale (why it best implements the selected strategy with lowest artificial complexity): `P1` keeps strategy `S2` explicit, deterministic, and collaboration-safe while preserving clear security gates and failure contracts.

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
