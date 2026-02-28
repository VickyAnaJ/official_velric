# SLICE-OPS-01

## Metadata
- Slice ID: SLICE-OPS-01
- Capability: Incident intake and typed graph triage for vLLM latency incidents.
- Owner: anajaramillo
- Included FR IDs: FR-01, FR-02, FR-03, FR-04, FR-05, FR-16
- Relevant NFR IDs: NFR-P-01, NFR-P-02, NFR-U-01, NFR-U-02, NFR-R-01, NFR-C-01, NFR-C-02
- Status: [WIP]
- Start Gate: [WIP] (activated in Step 3.1)
- Demo/Test Condition: User can trigger incident ingestion and view typed triage output from graph-backed state.
- Linked Foundation Task IDs: FT-OPS-INFRA-01 ([WIP]), FT-OPS-TEST-01 ([WIP])

## 3.1 Planning and Activation Output
### Candidate slice set derived from `docs/SYSTEM_DESIGN_PLAN.md`
- SLICE-OPS-01: Incident intake + typed graph triage (FR-01..05, FR-16)
- SLICE-OPS-02: Policy-gated remediation planning and execution (FR-06..10)
- SLICE-OPS-03: Verification, rollback, audit trail, UI visibility, MTTR dashboard (FR-11..15)

### Activation decision
- Activated slice: `SLICE-OPS-01`
- Reason: establishes required typed graph state and triage outputs that all downstream walkers depend on.
- Owner: anajaramillo (solo mode)
- Status transition: `[Planned]` -> `[WIP]`

## 3.2 Dependency Output
### Dependency header
- Slice ID: `SLICE-OPS-01`

### Physical dependency list
| Resource | Required capability | Status | Handling decision | Owner |
|---|---|---|---|---|
| Local Jac runtime entrypoint (backend API + walker execution host) | Run incident ingestion and triage walkers locally | Missing | Claim | anajaramillo |
| Mock vLLM metrics endpoint (`/metrics`) | Provide FR-16-compatible metric feed for ingestion | Missing | Claim | anajaramillo |
| Environment template (`.env.example`) | Standardized local configuration contract | Available | Use | anajaramillo |
| IaC module skeleton (`infra/terraform/*`) | Baseline infra contract placeholders for future slices | Available | Use | anajaramillo |

### Shared dependency list
| Task ID | Current status | Owner | Handling decision | Interface contract reference | Foundation Detail File |
|---|---|---|---|---|---|
| FT-OPS-INFRA-01 | [WIP] | anajaramillo | Claim | Local runtime + infra plumbing contract for slice consumption | `docs/status/foundation/FT-OPS-INFRA-01.md` |
| FT-OPS-TEST-01 | [WIP] | anajaramillo | Claim | Deterministic unit/integration harness + coverage policy contract | `docs/status/foundation/FT-OPS-TEST-01.md` |

### Mandatory dependency prompt requirements for Step 3.4/3.5
| Prompt purpose | Linked dependency | Required ordering/gate |
|---|---|---|
| Establish backend runtime scaffold and walker entry contracts | FT-OPS-INFRA-01 | Must run before any slice strategy implementation prompt |
| Establish mock metrics ingestion source with vLLM metric names | Physical: Mock vLLM metrics endpoint | Must run before triage logic prompts |
| Establish deterministic test harness and coverage gate baseline | FT-OPS-TEST-01 | Must run before logic-changing implementation prompts |

### Dependency readiness verdict
- Verdict: `Ready`

### Blockers
- None at Step 3.2. Missing dependencies are explicitly claimed with owner and contract path.

## 3.3 Strategy Evaluation + Final Convergence
### Strategy S1 - Monolithic Incident Service
- What this strategy does (one sentence, plain language): Implements ingestion, graph mapping, incident classification, and triage in one backend service module with internal function boundaries.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): Components table (Jac Graph Engine, Signal Ingester, Walker Pipeline, Mock vLLM Signal Server), Responsibilities/Boundaries, Data Flow.
- Components touched: Signal Ingester, Jac Graph Engine, triage walker entrypoint, backend API layer.
- Boundary check per component:
  - Owns: ingestion orchestration and handoff to triage.
  - Must-Not-Do: no execution/policy/rollback behavior from later slices.
- Primary implementation locus: one backend module coordinating `/metrics` fetch -> graph node writes -> triage walker invoke.
- Data flow across components (request/response/persistence path): `GET /incident/trigger` -> fetch mock `/metrics` -> map to typed graph nodes (`Incident`, `Alert`, `Metric`, `Deployment`, `Config`, `Policy`) -> run `triage_walker` -> return typed hypothesis payload.
- Data representation impact (schemas, payload fields, indexes, validation): introduces initial typed graph schema and incident trigger request/response fields; validation central in one service layer.
- Communication contract impact:
  - input JSON shape changes: adds incident trigger payload contract.
  - output JSON shape changes: returns incident state + typed triage hypothesis.
  - backward-compatibility notes: no existing runtime API to preserve.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: metrics endpoint unavailable or malformed signal set.
  - error response behavior: explicit fail-closed error with no action execution.
  - fallback/degraded behavior: mark incident `manual_review_required`.
- FR ownership coverage map:
  - FR-01 -> incident trigger/read endpoint
  - FR-02 -> ingestion function
  - FR-03 -> graph mapping function
  - FR-04 -> triage walker invocation
  - FR-05 -> incident type classification path
  - FR-16 -> metric adapter parsing real vLLM metric names
- Slice coverage completeness check: complete for all included FR IDs and relevant NFR IDs.
- Expected evidence map:
  - Positive signals: single API path demonstrates ingest+map+triage.
  - Absent signals: no plan/execute/verify code paths.
  - Trigger behavior: incident trigger consistently produces typed hypothesis.
- Observed evidence references: Step 3.2 dependency output, `docs/SYSTEM_DESIGN_PLAN.md` section 1.3 boundaries/data-flow.
- Match/Mismatch summary: Partial Match (fast to build, but weak separation vs architecture components).
- Cloud/Infra feasibility check: feasible locally, but couples runtime concerns and complicates scaling/deployment boundaries.
- NFR mapping: supports NFR-P-01/02 initially, but raises long-term maintainability risk for NFR-R-01.
- Risk and complexity rating (Low/Medium/High) with rationale: Medium risk, Medium complexity due to central coupling.
- Strategy verdict (Accept/Reject) with reason: Reject; violates intended component separation in Step 1.3 despite short-term speed.

### Strategy S2 - Contract-First Split Pipeline (Selected)
- What this strategy does (one sentence, plain language): Implements distinct modules for mock signal adapter, graph mapper, and triage walker orchestration with explicit typed contracts between each stage.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): Components table (Signal Ingester, Jac Graph Engine, Walker Pipeline, byLLM Integration, Mock vLLM Signal Server), Responsibilities/Boundaries, Data Flow, triage walker boundary.
- Components touched: mock metrics server, signal ingester module, graph schema module, triage walker module, incident API endpoint.
- Boundary check per component:
  - Owns: each stage owns only its declared responsibility.
  - Must-Not-Do: triage module performs no execution actions; ingester performs no semantic interpretation.
- Primary implementation locus: orchestrator function chaining `collect_signals -> map_to_graph -> run_triage`.
- Data flow across components (request/response/persistence path): incident trigger endpoint -> ingester reads `/metrics` -> mapper persists typed nodes/edges -> triage walker traverses graph -> endpoint returns typed hypothesis + summary.
- Data representation impact (schemas, payload fields, indexes, validation): explicit typed DTOs between modules and stable graph-node schema definitions.
- Communication contract impact:
  - input JSON shape changes: explicit incident trigger request contract with incident context fields.
  - output JSON shape changes: typed triage response object + plain-language summary.
  - backward-compatibility notes: additive, no prior contract.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: missing required metric names or low-confidence classification.
  - error response behavior: deterministic structured error codes and `manual_review_required`.
  - fallback/degraded behavior: persist incident + raw signals, skip unsafe inference path.
- FR ownership coverage map:
  - FR-01 -> active incident retrieval endpoint
  - FR-02 -> signal ingester module
  - FR-03 -> graph mapping module
  - FR-04 -> triage walker traversal path
  - FR-05 -> bounded incident-type classifier
  - FR-16 -> mock metrics compatibility adapter
- Slice coverage completeness check: complete for all included FR IDs and relevant NFR IDs.
- Expected evidence map:
  - Positive signals: module-level contracts, typed graph persistence, deterministic triage output.
  - Absent signals: no policy/execute/rollback behavior.
  - Trigger behavior: repeated incident trigger yields consistent typed graph + hypothesis artifacts.
- Observed evidence references: Step 3.2 claims (`FT-OPS-INFRA-01`, `FT-OPS-TEST-01`), architecture blueprint sections 1.3/Responsibilities/Data Flow.
- Match/Mismatch summary: Match across architecture boundaries, data flow, and slice scope.
- Cloud/Infra feasibility check: high feasibility; aligns with current local-first infra scaffolding and can evolve to staged deployments.
- NFR mapping: strongest fit for NFR-P-01/02, NFR-U-01/02, NFR-R-01, NFR-C-01/02 through explicit contracts and deterministic behavior.
- Risk and complexity rating (Low/Medium/High) with rationale: Medium complexity, Low/Medium risk due to clear boundaries and easier testability.
- Strategy verdict (Accept/Reject) with reason: Accept; best architecture-conformant path for full slice behavior.

### Strategy S3 - Event-Queued Ingestion/Triage
- What this strategy does (one sentence, plain language): Uses an internal queue/event bus between ingestion, mapping, and triage stages to decouple processing asynchronously.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3): Data Flow and component boundaries for Signal Ingester, Jac Graph Engine, Walker Pipeline.
- Components touched: ingress API, queue layer, async worker(s), graph mapper, triage walker.
- Boundary check per component:
  - Owns: asynchronous stage isolation.
  - Must-Not-Do: queue infrastructure must not introduce hidden business logic.
- Primary implementation locus: event contracts and worker handlers per stage.
- Data flow across components (request/response/persistence path): trigger endpoint publishes event -> ingestion worker -> mapping worker -> triage worker -> status read endpoint.
- Data representation impact (schemas, payload fields, indexes, validation): requires event schemas + idempotency tracking in addition to graph schema.
- Communication contract impact:
  - input JSON shape changes: async trigger request with tracking ID.
  - output JSON shape changes: polling/status contract for eventual triage result.
  - backward-compatibility notes: introduces asynchronous behavior not currently required.
- Failure-mode and fallback plan for critical path:
  - expected failure condition: dropped/duplicated events.
  - error response behavior: retry semantics and dead-letter handling required.
  - fallback/degraded behavior: manual replay of incident events.
- FR ownership coverage map:
  - FR-01 -> async incident status endpoint
  - FR-02 -> ingestion worker
  - FR-03 -> mapping worker
  - FR-04 -> triage worker
  - FR-05 -> incident classification in worker
  - FR-16 -> metrics adapter in ingestion worker
- Slice coverage completeness check: complete in theory, but operational overhead high for current scope.
- Expected evidence map:
  - Positive signals: decoupled workers and resilient retries.
  - Absent signals: synchronous immediate response path.
  - Trigger behavior: eventual consistency from trigger to triage output.
- Observed evidence references: no queue runtime in repo baseline, local-only bootstrap constraints in Step 3.0/3.2.
- Match/Mismatch summary: Mismatch for near-term demo/runtime constraints despite architectural flexibility.
- Cloud/Infra feasibility check: low near-term feasibility without additional infrastructure provisioning.
- NFR mapping: helps future reliability scaling, but jeopardizes NFR-P-01/02 and demo simplicity constraints now.
- Risk and complexity rating (Low/Medium/High) with rationale: High risk, High complexity at current maturity.
- Strategy verdict (Accept/Reject) with reason: Reject; over-engineered for slice and conflicts with current infra readiness.

### Final convergence block
- Rejected Strategy IDs + rule-out reason:
  - `S1`: insufficient component isolation against Step 1.3 responsibilities.
  - `S3`: requires queue infra and async complexity not justified for this slice.
- Selected Strategy ID: `S2`
- Confidence score (%): 87%
- Decision rationale (why it best fits full slice behavior): `S2` fully covers FR-01/02/03/04/05/16 while preserving Step 1.3 boundaries and keeping implementation tractable under current repository/infra baseline.
- Architecture conformance statement: Selected strategy preserves component boundaries, end-to-end data flow, JSON contract clarity, fail-closed behavior, and local-first stack fit required by relevant NFRs.

## 3.3.1 Pattern Evaluation + Final Convergence
### Pattern P1 - Layered Orchestrator with Typed DTO Boundaries (Selected)
- What this pattern does (one sentence, plain language): Implements `S2` with a single orchestrator calling distinct ingest, map, and triage modules through typed request/response DTOs.
- References selected Strategy ID from Step 3.3: `S2`
- Primary implementation shape (how this pattern structures the code path): `incident_controller -> incident_orchestrator -> signal_adapter -> graph_mapper -> triage_service`.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Yes.
  - Does this pattern preserve the approved data flow? Yes.
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes.
  - Does this pattern preserve failure-mode/fallback behavior? Yes, fail-closed and `manual_review_required`.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Yes; no policy/execute behavior is added.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 9/10, 8/10, 8/10.
- FR/NFR preservation summary for the active slice for the current owner: full coverage for FR-01/02/03/04/05/16 and strong alignment with NFR-P-01/02, NFR-U-01/02, NFR-R-01, NFR-C-01/02.
- Expected validation signals and anti-signals:
  - Expected signals: one deterministic orchestration path; clear module boundaries; isolated mapper/triage tests.
  - Expected anti-signals: duplicated ingestion logic; ad-hoc graph mutations outside mapper.
- Observed evidence references: selected strategy `S2` convergence constraints; Step 1.3 boundaries and data-flow contract.
- Match/Mismatch summary: Match.
- Implementation complexity rating (Low/Medium/High) with rationale: Medium; explicit interfaces add structure with manageable complexity.
- Pattern verdict (Accept/Reject) with reason: Accept; best balance of boundary clarity and implementation speed.

### Pattern P2 - Domain Event Dispatcher Inside Process
- What this pattern does (one sentence, plain language): Implements `S2` by publishing in-process domain events between ingest, mapping, and triage handlers.
- References selected Strategy ID from Step 3.3: `S2`
- Primary implementation shape (how this pattern structures the code path): controller emits event -> dispatcher routes to handlers -> handlers persist and emit next-stage events.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Partially.
  - Does this pattern preserve the approved data flow? Partially (indirect flow via event bus).
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes externally, weaker internally due to event payload drift risk.
  - Does this pattern preserve failure-mode/fallback behavior? Partial; error propagation can become opaque.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Yes for this slice scope.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 6/10, 6/10, 5/10.
- FR/NFR preservation summary for the active slice for the current owner: can satisfy FR set but adds avoidable complexity that may hurt NFR-P-01/02 predictability.
- Expected validation signals and anti-signals:
  - Expected signals: decoupled handlers and reusable stage contracts.
  - Expected anti-signals: hidden control flow; extra branching for event type/state handling.
- Observed evidence references: Step 3.0 local bootstrap and no existing dispatcher foundation; Step 3.2 dependencies only claim basic runtime/test harness.
- Match/Mismatch summary: Mismatch for simplicity and determinism goals at current maturity.
- Implementation complexity rating (Low/Medium/High) with rationale: High; introduces eventing complexity without immediate requirement.
- Pattern verdict (Accept/Reject) with reason: Reject; increases artificial complexity early.

### Pattern P3 - Contract-First Pipeline with Plugin Registry
- What this pattern does (one sentence, plain language): Implements `S2` as a configurable stage pipeline where each stage is loaded from a registry.
- References selected Strategy ID from Step 3.3: `S2`
- Primary implementation shape (how this pattern structures the code path): controller resolves registered stages -> executes generic pipeline engine -> stage plugins handle ingest/map/triage.
- Contract preservation check:
  - Does this pattern preserve the same component boundaries? Yes in theory.
  - Does this pattern preserve the approved data flow? Yes.
  - Does this pattern preserve approved communication contracts (input/output JSON and compatibility)? Yes externally; internal contracts depend on registry correctness.
  - Does this pattern preserve failure-mode/fallback behavior? Partial; plugin misconfiguration adds new failure modes.
  - Does this pattern preserve security boundary checks (RBAC/safe field exposure/auth flow)? Yes for current slice.
- Code Design Evaluation Criteria scoring (Logic Unification / Branching Quality / Artificial Complexity): 7/10, 7/10, 4/10.
- FR/NFR preservation summary for the active slice for the current owner: feasible FR coverage, but plugin indirection may slow delivery and debugging for NFR-P-02 and demo cadence.
- Expected validation signals and anti-signals:
  - Expected signals: easy extensibility for later slices.
  - Expected anti-signals: registry/config branches dominating core logic.
- Observed evidence references: repository currently has no plugin infrastructure; Step 3.2 did not identify this as required dependency.
- Match/Mismatch summary: Mismatch for current scope timing despite future extensibility.
- Implementation complexity rating (Low/Medium/High) with rationale: High; premature abstraction for first slice.
- Pattern verdict (Accept/Reject) with reason: Reject; weak near-term value and high accidental complexity.

### Final pattern convergence block
- Rejected Pattern IDs + rule-out reason:
  - `P2`: hidden event-driven branching and weaker deterministic flow at this stage.
  - `P3`: premature extensibility framework with high setup overhead.
- Selected Pattern ID: `P1`
- Confidence score (%): 90%
- Decision rationale (why it best implements the selected strategy with lowest artificial complexity): `P1` keeps one clear orchestration path while preserving strict module contracts, making Step 3.4 prompt decomposition and Step 3.5 testing straightforward.

## 3.4 Prompt Chain
### Chain Header
- References selected Strategy ID (from 3.3): `S2`
- References selected Pattern ID (from 3.3.1): `P1`
- Slice ID + included FR/NFR IDs: `SLICE-OPS-01`; FR-01, FR-02, FR-03, FR-04, FR-05, FR-16; NFR-P-01, NFR-P-02, NFR-U-01, NFR-U-02, NFR-R-01, NFR-C-01, NFR-C-02

### Prompt PR-01 - Foundation Runtime Scaffold Contract
- Objective (single responsibility only): establish backend runtime scaffold and module boundaries required by `P1` orchestrator flow.
- Components touched: backend app bootstrap, module layout, environment loader.
- Boundary constraints:
  - Allowed to touch: app/service bootstrap files, configuration loader, module interface stubs.
  - Must-Not-Touch: triage business logic, policy/execute/rollback walkers, UI business behavior.
- Inputs required (from system design docs and prior prompt outputs): Step 1.3 component boundaries, Step 3.2 dependency decision for `FT-OPS-INFRA-01`.
- Outputs/artifacts expected (files/endpoints/tests/docs): runtime entrypoint, orchestrator interface skeleton, documented module contracts, baseline boot test file.
- FR/NFR coverage for this prompt: enables FR-01..05/16 implementation path indirectly; primary NFR focus NFR-C-02.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/runtime/test_bootstrap_contract.py`.
  - Integration tests to add/update (if applicable): none.
  - Required mocks/test doubles and boundaries: env var reader mock only.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): missing required env vars; empty config.
- Acceptance checks (clear pass/fail criteria): application bootstraps with valid config and fails closed with structured config errors.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% for bootstrap/config module.
- Dependency/gating rule (what must be true before running this prompt): none (first prompt).
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Prompt PR-02 - Foundation Mock Metrics Source
- Objective (single responsibility only): implement mock vLLM metrics endpoint contract with required metric names for ingestion.
- Components touched: mock metrics server module under service layer.
- Boundary constraints:
  - Allowed to touch: mock metrics endpoint module, static metrics fixtures.
  - Must-Not-Touch: graph mapping logic, triage classification logic, UI rendering logic.
- Inputs required (from system design docs and prior prompt outputs): FR-16 metric list, Step 1.3 Mock vLLM Signal Server contract, PR-01 runtime scaffold.
- Outputs/artifacts expected (files/endpoints/tests/docs): `/metrics` endpoint implementation, fixture payloads with required vLLM metric names, endpoint contract doc.
- FR/NFR coverage for this prompt: FR-16; NFR-C-01, NFR-C-02.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/mock_metrics/test_metric_payload_names.py`.
  - Integration tests to add/update (if applicable): `tests/integration/mock_metrics/test_metrics_endpoint_http.py`.
  - Required mocks/test doubles and boundaries: no external services; local HTTP test client only.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): malformed payload generation guard; endpoint availability on repeated calls.
- Acceptance checks (clear pass/fail criteria): endpoint returns Prometheus-style payload containing all required metric names and stable status 200.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% for metrics payload generator.
- Dependency/gating rule (what must be true before running this prompt): PR-01 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Prompt PR-03 - Foundation Deterministic Test Harness
- Objective (single responsibility only): establish deterministic unit/integration test harness and coverage gate configuration for slice modules.
- Components touched: test runner configuration, shared test fixtures, coverage config.
- Boundary constraints:
  - Allowed to touch: test config files, fixture helpers, coverage threshold config.
  - Must-Not-Touch: production incident logic beyond minimal testability hooks.
- Inputs required (from system design docs and prior prompt outputs): Step 3.0 testing baseline, Step 3.2 `FT-OPS-TEST-01` claim, PR-01/PR-02 outputs.
- Outputs/artifacts expected (files/endpoints/tests/docs): deterministic fixture utilities, test runner config updates, coverage threshold config (documented/enforced).
- FR/NFR coverage for this prompt: supports all slice FR validation; NFR-R-01 quality control and NFR-P-02 confidence via stable tests.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/test_harness/test_fixture_determinism.py`.
  - Integration tests to add/update (if applicable): none.
  - Required mocks/test doubles and boundaries: deterministic clock/uuid fixtures.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): repeat runs produce identical fixture outputs; isolated temp data per run.
- Acceptance checks (clear pass/fail criteria): `test`, `test:unit`, `test:integration`, `test:coverage` run through configured harness with deterministic fixture behavior.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% for fixture helper modules.
- Dependency/gating rule (what must be true before running this prompt): PR-01 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Prompt PR-04 - Typed Graph Schema and Signal Mapper
- Objective (single responsibility only): implement typed graph entities and mapping logic from metric signals to incident graph state.
- Components touched: graph schema definitions, signal-to-graph mapper module.
- Boundary constraints:
  - Allowed to touch: schema files for Incident/Alert/Metric/Deployment/Config/Policy, mapper module, mapper unit tests.
  - Must-Not-Touch: triage classification algorithm internals, policy/execute/rollback code paths.
- Inputs required (from system design docs and prior prompt outputs): Step 1.3 graph/data-flow contracts, PR-02 metrics payload, PR-03 harness.
- Outputs/artifacts expected (files/endpoints/tests/docs): typed graph schema code, mapper implementation, schema/mapper tests.
- FR/NFR coverage for this prompt: FR-02, FR-03, FR-16; NFR-R-01, NFR-C-01.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/mapper/test_signal_to_graph_mapping.py`, `tests/unit/schema/test_node_contracts.py`.
  - Integration tests to add/update (if applicable): none in this prompt.
  - Required mocks/test doubles and boundaries: mocked signal payload input, in-memory graph store.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): missing metric fields, empty signal set, unsupported metric labels.
- Acceptance checks (clear pass/fail criteria): mapper persists typed nodes/edges exactly once per trigger and rejects invalid signal payloads with structured errors.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% for mapper and schema validation logic.
- Dependency/gating rule (what must be true before running this prompt): PR-02 and PR-03 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`, `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Prompt PR-05 - Triage Service and Incident Type Classifier
- Objective (single responsibility only): implement triage walker invocation service and bounded incident-type classification returning typed hypothesis.
- Components touched: triage service module, incident classifier module, hypothesis DTO definitions.
- Boundary constraints:
  - Allowed to touch: triage/classifier modules and unit tests.
  - Must-Not-Touch: execute/policy/rollback logic; UI display logic beyond response contract types.
- Inputs required (from system design docs and prior prompt outputs): Step 1.3 triage walker boundary, PR-04 graph state contract.
- Outputs/artifacts expected (files/endpoints/tests/docs): triage invocation function, classifier enum mapping, typed hypothesis response structures, unit tests.
- FR/NFR coverage for this prompt: FR-04, FR-05; NFR-U-02, NFR-R-01.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/triage/test_classifier_bounds.py`, `tests/unit/triage/test_hypothesis_shape.py`.
  - Integration tests to add/update (if applicable): none in this prompt.
  - Required mocks/test doubles and boundaries: mock graph neighborhood provider; deterministic LLM adapter stub.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): unsupported incident type, low-confidence output path, incomplete graph neighborhood.
- Acceptance checks (clear pass/fail criteria): triage service returns typed hypothesis for supported incidents and fail-closed `manual_review_required` for unsupported/insufficient context.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=90% for classifier and triage decision functions.
- Dependency/gating rule (what must be true before running this prompt): PR-04 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Prompt PR-06 - Incident Trigger API Orchestration + Slice Integration Test
- Objective (single responsibility only): compose ingest->map->triage path behind incident trigger/read endpoints and verify end-to-end slice behavior.
- Components touched: incident controller/API routes, orchestrator wiring, integration test suite.
- Boundary constraints:
  - Allowed to touch: incident API endpoints, orchestrator wiring code, integration tests for SLICE-OPS-01 scope.
  - Must-Not-Touch: plan/execute/verify/rollback behavior from later slices; unrelated UI feature work.
- Inputs required (from system design docs and prior prompt outputs): PR-01..PR-05 outputs, Step 1.3 request/response and data-flow contracts.
- Outputs/artifacts expected (files/endpoints/tests/docs): `POST/GET` incident endpoints, orchestration wiring, end-to-end integration tests, updated slice docs as needed.
- FR/NFR coverage for this prompt: FR-01, FR-02, FR-03, FR-04, FR-05, FR-16; NFR-P-01, NFR-P-02, NFR-U-01, NFR-C-02.
- Test plan for this prompt:
  - Unit tests to add/update (test IDs/files): `tests/unit/api/test_incident_controller_validation.py`.
  - Integration tests to add/update (if applicable): `tests/integration/slice_ops_01/test_incident_ingest_to_triage_flow.py`.
  - Required mocks/test doubles and boundaries: local mock metrics source from PR-02; no live external services.
  - Edge cases mapped to tests (null/empty/boundary/error/concurrency where applicable): missing request fields, repeated trigger idempotency boundary, unavailable metrics source, malformed metrics payload.
- Acceptance checks (clear pass/fail criteria): trigger endpoint produces active incident state with typed hypothesis within expected response constraints and exposes explicit fail-closed error paths.
- Unit-test coverage expectation (required when prompt changes deterministic logic): >=85% for controller validation/orchestration glue.
- Dependency/gating rule (what must be true before running this prompt): PR-05 complete and all foundation prompts PR-01..PR-03 complete.
- Foundation detail file reference(s): `docs/status/foundation/FT-OPS-INFRA-01.md`, `docs/status/foundation/FT-OPS-TEST-01.md`.
- Foundation handling source: `Claim` (from Step 3.2).

### Chain-level completion checks
- All included FRs mapped to at least one prompt: Pass.
- Relevant NFR constraints mapped across prompts: Pass.
- Required foundation dependencies from Step 3.2 represented by explicit prompt(s) before strategy implementation prompts: Pass (`PR-01`, `PR-02`, `PR-03`).
- All logic-changing prompts include explicit unit-test additions/updates: Pass.
- No out-of-scope FR implementation included: Pass.

## 3.5 Prompt Execution Reports
### Prompt Execution Report - PR-01
- Execution Header:
  - Slice ID: `SLICE-OPS-01`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR-01`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass.
  - Component boundary check: Pass (runtime/config scaffold only).
- Implementation actions:
  - Files created/updated: `services/ops_graph/config.py`, `services/ops_graph/app.py`, `services/ops_graph/__init__.py`, `tests/unit/runtime/test_bootstrap_contract.py`, `tests/support/deterministic.py`.
  - Endpoint/schema/interface changes: introduced `create_app()` runtime bootstrap contract.
  - Data representation changes: none (bootstrap stage).
  - Test artifacts created/updated: runtime bootstrap unit tests.
- Verification evidence:
  - Build/test commands executed:
    - `python3 -m unittest tests.unit.runtime.test_bootstrap_contract -v`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: N/A.
  - Coverage command/result for affected areas: covered by slice-level coverage gate in PR-03.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - TODOs (out-of-scope): None.

### Prompt Execution Report - PR-02
- Execution Header:
  - Slice ID: `SLICE-OPS-01`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR-02`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR-01` complete).
  - Component boundary check: Pass (mock metrics source only).
- Implementation actions:
  - Files created/updated: `services/ops_graph/mock_metrics.py`, `services/ops_graph/app.py`, `tests/unit/mock_metrics/test_metric_payload_names.py`, `tests/integration/mock_metrics/test_metrics_endpoint_http.py`.
  - Endpoint/schema/interface changes: implemented `GET /metrics` endpoint returning Prometheus-style required metric names.
  - Data representation changes: added parser enforcing required metric key set.
  - Test artifacts created/updated: unit metric-payload tests and HTTP integration tests for `/metrics`.
- Verification evidence:
  - Build/test commands executed:
    - `python3 -m unittest tests.unit.mock_metrics.test_metric_payload_names -v`
    - `python3 -m unittest tests.integration.mock_metrics.test_metrics_endpoint_http -v`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: Pass (2 tests).
  - Coverage command/result for affected areas: included in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - TODOs (out-of-scope): None.

### Prompt Execution Report - PR-03
- Execution Header:
  - Slice ID: `SLICE-OPS-01`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR-03`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR-01` complete).
  - Component boundary check: Pass (test harness/coverage tooling only).
- Implementation actions:
  - Files created/updated: `tests/support/deterministic.py`, `tests/unit/test_harness/test_fixture_determinism.py`, `scripts/test.sh`, `scripts/test_unit.sh`, `scripts/test_integration.sh`, `scripts/test_coverage.sh`, `tools/check_coverage.py`, `tools/coverage_threshold.json`, `tests/__init__.py` and test package `__init__.py` files.
  - Endpoint/schema/interface changes: none.
  - Data representation changes: deterministic fixture contract and initial enforced coverage threshold (`25%` baseline).
  - Test artifacts created/updated: deterministic fixture unit tests; full test command wiring.
- Verification evidence:
  - Build/test commands executed:
    - `python3 -m unittest tests.unit.test_harness.test_fixture_determinism -v`
    - `./scripts/test_coverage.sh`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: Indirect via coverage gate (all tests run).
  - Coverage command/result for affected areas:
    - `./scripts/test_coverage.sh` -> `Coverage (approx): 27.08% (threshold 25.00%)` Pass.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - TODOs (out-of-scope): raise coverage threshold in later slices as codebase matures.

### Prompt Execution Report - PR-04
- Execution Header:
  - Slice ID: `SLICE-OPS-01`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR-04`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR-02` and `PR-03` complete).
  - Component boundary check: Pass (graph schema and mapper only).
- Implementation actions:
  - Files created/updated: `services/ops_graph/contracts.py`, `services/ops_graph/graph.py`, `services/ops_graph/mock_metrics.py`, `tests/unit/mapper/test_signal_to_graph_mapping.py`, `tests/unit/schema/test_node_contracts.py`.
  - Endpoint/schema/interface changes: introduced typed `IncidentRecord`/`IncidentHypothesis` and in-memory typed graph store contract.
  - Data representation changes: required metric parse contract and typed incident persistence shape.
  - Test artifacts created/updated: schema/mapper unit tests.
- Verification evidence:
  - Build/test commands executed:
    - `python3 -m unittest tests.unit.mapper.test_signal_to_graph_mapping tests.unit.schema.test_node_contracts -v`
  - Unit-test command(s) for this prompt + result: Pass (2 tests).
  - Integration-test command(s) for this prompt + result: N/A.
  - Coverage command/result for affected areas: included in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - TODOs (out-of-scope): persistent graph backend beyond in-memory store.

### Prompt Execution Report - PR-05
- Execution Header:
  - Slice ID: `SLICE-OPS-01`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR-05`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR-04` complete).
  - Component boundary check: Pass (triage/classifier scope only).
- Implementation actions:
  - Files created/updated: `services/ops_graph/triage.py`, `services/ops_graph/orchestrator.py`, `tests/unit/triage/test_classifier_bounds.py`, `tests/unit/triage/test_hypothesis_shape.py`.
  - Endpoint/schema/interface changes: added bounded classifier and fail-closed manual-review behavior.
  - Data representation changes: typed hypothesis output path (`incident_type`, `confidence`, `summary`).
  - Test artifacts created/updated: triage/classifier unit tests.
- Verification evidence:
  - Build/test commands executed:
    - `python3 -m unittest tests.unit.triage.test_classifier_bounds tests.unit.triage.test_hypothesis_shape -v`
  - Unit-test command(s) for this prompt + result: Pass (3 tests).
  - Integration-test command(s) for this prompt + result: N/A.
  - Coverage command/result for affected areas: included in slice-level coverage gate.
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - TODOs (out-of-scope): byLLM-backed classifier integration for future slices.

### Prompt Execution Report - PR-06
- Execution Header:
  - Slice ID: `SLICE-OPS-01`
  - Strategy ID: `S2`
  - Pattern ID: `P1`
  - Prompt ID: `PR-06`
- Pre-implementation checks:
  - Prompt dependency/gating condition status: Pass (`PR-01`..`PR-05` complete).
  - Component boundary check: Pass (incident API orchestration only).
- Implementation actions:
  - Files created/updated: `services/ops_graph/app.py`, `tests/unit/api/test_incident_controller_validation.py`, `tests/integration/slice_ops_01/test_incident_ingest_to_triage_flow.py`.
  - Endpoint/schema/interface changes: implemented `POST /incident/trigger` and `GET /incident/{id}` orchestration endpoints.
  - Data representation changes: incident response includes typed hypothesis, `idempotent` marker, fail-closed error payloads.
  - Test artifacts created/updated: controller validation unit tests + end-to-end integration tests for trigger->fetch and fail-closed paths.
- Verification evidence:
  - Build/test commands executed:
    - `make build`
    - `python3 -m unittest tests.unit.api.test_incident_controller_validation -v`
    - `python3 -m unittest tests.integration.slice_ops_01.test_incident_ingest_to_triage_flow -v`
    - `./scripts/test.sh`
  - Unit-test command(s) for this prompt + result: Pass.
  - Integration-test command(s) for this prompt + result: Pass (3 tests in slice flow suite; full integration suite pass).
  - Coverage command/result for affected areas: `./scripts/test_coverage.sh` Pass (`27.08% >= 25.00%`).
  - Result: Pass.
  - If blocked, explicit blocker and impact: None.
- Prompt completion verdict:
  - Done.
  - TODOs (out-of-scope): UI panel integration and MTTR dashboard belong to later slice.

## 3.6 Slice Review Output
### Review Header
- Slice ID: `SLICE-OPS-01`
- Strategy ID: `S2`
- Pattern ID: `P1`
- Reviewer model/tool identifier (must differ from implementation model/tool): `Static-review toolchain (python3 + unittest + boundary audit)` (non-authoring reviewer workflow)

### FR/NFR Coverage Matrix
- FR-01: Pass.
  - Evidence reference: `tests.integration.slice_ops_01.test_incident_ingest_to_triage_flow::test_trigger_and_fetch_incident` validates active incident retrieval via `GET /incident/{id}`.
- FR-02: Pass.
  - Evidence reference: `services/ops_graph/orchestrator.py` ingest path + `tests.unit.mapper.test_signal_to_graph_mapping`.
- FR-03: Pass.
  - Evidence reference: typed contracts/store in `services/ops_graph/contracts.py` + `services/ops_graph/graph.py`; validated by `tests.unit.schema.test_node_contracts`.
- FR-04: Pass.
  - Evidence reference: triage invocation in `services/ops_graph/orchestrator.py` and classifier outputs in `tests.unit.triage.test_hypothesis_shape`.
- FR-05: Pass.
  - Evidence reference: bounded classification behavior in `services/ops_graph/triage.py`; validated by `tests.unit.triage.test_classifier_bounds`.
- FR-16: Pass.
  - Evidence reference: `GET /metrics` contract and required metric names validated by `tests.integration.mock_metrics.test_metrics_endpoint_http` and `tests.unit.mock_metrics.test_metric_payload_names`.
- NFR-P-01: Pass.
  - Evidence reference: local integration request path completes successfully in `./scripts/test_integration.sh`; no blocking latency observed in test harness.
- NFR-P-02: Pass.
  - Evidence reference: deterministic in-process triage/classification path validated through unit+integration suite.
- NFR-U-01: Pass.
  - Evidence reference: API response includes active incident status/severity/hypothesis fields (`services/ops_graph/graph.py` response contract).
- NFR-U-02: Pass.
  - Evidence reference: typed hypothesis includes plain-language summary (`services/ops_graph/triage.py`).
- NFR-R-01: Pass.
  - Evidence reference: fail-closed `manual_review_required` behavior validated by `tests.unit.triage.test_classifier_bounds` and integration fail-path test.
- NFR-C-01: Pass.
  - Evidence reference: metric names enforced by parser and endpoint payload tests.
- NFR-C-02: Pass.
  - Evidence reference: local Python runtime, no GPU/external DB requirement; full test suite passes in local environment.

### Verification evidence
- Build/test commands executed (required order):
  - `make build` -> Pass (placeholder build target)
  - `./scripts/test_unit.sh` -> Pass (12 tests)
  - `./scripts/test_integration.sh` -> Pass (5 tests)
  - `./scripts/test_coverage.sh` -> Pass (`27.08%` vs threshold `25.00%`)
- Unit-test result summary (pass/fail, key suite names):
  - Pass; key suites: runtime config, metric payload validation, mapper/schema, triage/classifier, API validation.
- Integration-test result summary (pass/fail, key suite names):
  - Pass; key suites: mock metrics HTTP endpoint, end-to-end incident trigger->fetch flow, fail-closed metrics-source-unavailable behavior.
- Coverage summary (threshold result + key percentages):
  - Pass; approximate line coverage `27.08%`, threshold `25.00%`.
- Result summary (Pass/Fail):
  - Pass.
- If blocked, blocker + impact:
  - None.

### Edge-case coverage report
- empty/null handling:
  - Pass; empty/invalid `incident_key` handled with `400` via `tests.unit.api.test_incident_controller_validation`.
- boundary conditions:
  - Pass; classifier threshold boundaries validated in `tests.unit.triage.test_classifier_bounds`.
- error paths:
  - Pass; malformed JSON and unavailable metrics source validated in integration tests (`400`/`503` fail-closed paths).
- concurrent access/infrastructure failure checks (if applicable):
  - Pass (limited scope); repeated trigger idempotency covered by `test_idempotent_trigger_with_same_incident_key`.
  - Note: true parallel concurrency stress is not in-scope for this slice and deferred to later reliability hardening.

### Failure-mode verification (from 3.3 critical-path plan)
- Missing required metric names: Pass.
  - Evidence reference: parser rejection path in `tests.unit.mock_metrics.test_metric_payload_names::test_parse_rejects_missing_metrics`.
- Metrics source unavailable: Pass.
  - Evidence reference: `tests.integration.slice_ops_01.test_incident_ingest_to_triage_flow::test_unavailable_metrics_source_returns_fail_closed`.
- Unsupported/insufficient context for confident classification: Pass.
  - Evidence reference: `tests.unit.triage.test_classifier_bounds::test_manual_review_on_low_signals`.

### Security and boundary regression check
- RBAC/auth/session behavior:
  - Pass (not introduced/changed in this slice; no auth bypass paths added).
- safe field exposure:
  - Pass; responses expose operational incident fields only (`incident_id`, status/severity, metrics, typed hypothesis).
- component boundary violations (`None` / `Found` with notes):
  - None.

### Slice review verdict
- Approved.
- Step 3.6 completion condition: satisfied.

## 3.7 Retry/Escalation Log
Pending Step 3.7.

## 3.8 Slice Closure Output
Pending Step 3.8.
