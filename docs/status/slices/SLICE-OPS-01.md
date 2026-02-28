# SLICE-OPS-01

## Metadata
- Slice ID: SLICE-OPS-01
- Capability: Incident intake and typed graph triage for vLLM latency incidents.
- Owner: Shivaganesh
- Included FR IDs: FR-01, FR-02, FR-03, FR-04, FR-05, FR-16
- Relevant NFR IDs: NFR-P-01, NFR-P-02, NFR-U-01, NFR-U-02, NFR-R-01, NFR-C-01, NFR-C-02
- Status: [WIP]
- Start Gate: Active

## 3.1 Planning and Activation Output
### Source mapping from `docs/SYSTEM_DESIGN_PLAN.md`
- Phase alignment: Phase 1 runnable baseline
- Architecture components owned in this slice:
  - Mock vLLM Signal Server
  - Signal Ingester
  - Jac Graph Engine
  - `triage_walker`
  - byLLM typed incident classification and hypothesis generation
  - Initial Jac frontend visibility for active incident state and typed decisions
- Walker/data-flow boundaries owned in this slice:
  - Incident trigger starts with mock vLLM `/metrics` polling
  - Ingested alert/deployment/route/config/policy inputs are mapped into typed graph nodes/edges
  - `triage_walker` traverses `Incident -> Alert -> Deployment -> Config -> Policy`
  - Output stops at typed `IncidentHypothesis`; no plan, execute, verify, rollback, or audit behavior is allowed in this slice
- Communication contracts introduced by this slice:
  - incident trigger path
  - incident state read path sufficient for initial incident and typed triage visibility
  - mock vLLM `/metrics` compatibility using real metric names
- External references that shape this slice:
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`

### FR/NFR mapping for this slice
- Functional requirements:
  - `FR-01`: active incident visible with severity, affected deployment, and primary signals
  - `FR-02`: ingest alert, deployment, route, config, and policy inputs on incident trigger
  - `FR-03`: map ingested inputs into typed graph nodes and edges
  - `FR-04`: run `triage_walker` over graph neighborhood to produce a typed hypothesis
  - `FR-05`: classify incident into a bounded supported incident type
  - `FR-16`: ingest mock vLLM Prometheus metrics using real metric names
- Non-functional requirements:
  - `NFR-P-01`: initial incident view should render within 2 seconds
  - `NFR-P-02`: ingestion plus triage should complete within 5 seconds
  - `NFR-U-01`: active incident and current walker stage become visible without log inspection
  - `NFR-U-02`: typed outputs should also produce understandable summaries
  - `NFR-R-01`: unsupported incident types fail closed with no action
  - `NFR-C-01`: vLLM metrics use real metric names
  - `NFR-C-02`: local single-virtualenv, no GPU, no external DB

### Candidate slice set considered during planning
- `SLICE-OPS-01`: Phase 1 triage baseline
- `SLICE-OPS-02`: planning/policy/execute expansion
- `SLICE-OPS-03`: verification/rollback/audit/UI closure

### Activation decision
- Activated slice: `SLICE-OPS-01`
- Owner: `Shivaganesh`
- Status transition: `[Planned]` -> `[WIP]`
- Start Gate transition: `Not Started` -> `Active`
- Why this slice activates first:
  - It matches the design doc's Phase 1 build order.
  - It establishes the typed graph state and triage contracts required by all downstream walkers.
  - It is the earliest architecture-valid end-to-end user-visible capability in the system.

## 3.2 Dependency Output
### Dependency header
- Slice ID: `SLICE-OPS-01`
- External reference sources used for this dependency check:
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`

### Physical dependency list
| Resource | Required capability | Status | Handling decision | Owner |
|---|---|---|---|---|
| Jac runtime in `.venv` | Run `jac start main.jac`, typed nodes, walkers, `cl {}` frontend, REST endpoints | Available | Use | Shivaganesh |
| `main.jac` bootstrap entrypoint | canonical place for graph schema, walkers, byLLM functions, frontend codespace | Available | Use | Shivaganesh |
| `mock_vllm.py` | local Prometheus `/metrics` feed with real vLLM metric names | Available | Use | Shivaganesh |
| Anthropic/byLLM environment wiring | enable typed `by llm()` functions during local execution | Missing | Claim | Shivaganesh |
| Cloud/infra guide for this slice | physical cloud provisioning decisions | Missing | Use current local-only baseline from system design; no separate cloud artifact required for this slice | Shivaganesh |

### Shared dependency list
| Task ID | Current status | Owner | Handling decision | Interface contract reference | Foundation Detail File |
|---|---|---|---|---|---|
| FT-OPS-INFRA-01 | [WIP] | Shivaganesh | Claim | Jac runtime/bootstrap contract, shared graph/runtime plumbing, shared endpoint skeleton | `docs/status/foundation/FT-OPS-INFRA-01.md` |
| FT-OPS-TEST-01 | [WIP] | Keilly | Mock | deterministic unit/integration harness and coverage contract for slice work | `docs/status/foundation/FT-OPS-TEST-01.md` |

### Mandatory dependency prompt requirements for Step 3.4/3.5
| Prompt purpose | Linked dependency | Required ordering/gate |
|---|---|---|
| Establish shared Jac runtime/bootstrap plumbing | FT-OPS-INFRA-01 | Must run before graph schema, signal ingestion, or triage implementation prompts |
| Provide deterministic test harness contract for slice work | FT-OPS-TEST-01 | Mock/test contract must exist before reviewable implementation prompts |
| Wire byLLM environment and typed function boundary | Anthropic/byLLM environment wiring | Must be handled before executing live typed `by llm()` paths; mock/fallback path required in development |

### Dependency readiness verdict
- Verdict: `Ready`

### Blockers
- None. Missing byLLM environment wiring is explicitly claimed and does not block strategy selection.

## 3.3 Strategy Evaluation + Final Convergence
### Strategy S1 - Single-File Jac Baseline Extension (Selected)
- What this strategy does (one sentence, plain language): implements the full Phase 1 slice directly inside `main.jac`, extending the existing Jac entrypoint with typed graph schema, signal ingestion, triage walker logic, typed REST endpoints, and minimal `cl {}` UI visibility in one load-bearing file.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3):
  - Components: Jac Graph Engine, Walker Pipeline, byLLM Integration, Mock vLLM Signal Server, Signal Ingester, Jac React Frontend
  - Responsibilities and Boundaries: `triage_walker` only, no execute/verify/rollback behavior
  - Data Flow: `/metrics` -> ingester -> graph nodes -> `triage_walker` -> incident state endpoint -> frontend poll
  - Communication and Contracts: `POST /walker/trigger_incident`, `GET /walker/incident_state/{incident_id}`, typed `IncidentHypothesis`
- External source references used:
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Components touched:
  - `main.jac`
  - `mock_vllm.py`
  - shared bootstrap/runtime contract from `FT-OPS-INFRA-01`
  - minimal frontend state in `cl {}` block
- Boundary check per component:
  - Owns:
    - Phase 1 graph entities and typed hypothesis contract
    - incident trigger and incident-state read path
    - signal ingestion from mock vLLM `/metrics`
    - `triage_walker` traversal and typed output persistence
  - Must-Not-Do:
    - no `plan_walker`, policy gate, execution, verification, rollback, or audit implementation
    - no separate non-Jac backend
    - no state mutation outside walker/runtime flow
- Primary implementation locus (where this strategy places core behavior: component/path/state transition):
  - `main.jac` as the canonical locus for node declarations, ingestion orchestration, `triage_walker`, typed REST endpoints, and minimal frontend polling/output.
- Data flow across components (request/response/persistence path):
  - `POST /walker/trigger_incident` -> fetch `mock_vllm.py` `/metrics` -> map to typed `Incident`, `Alert`, `Deployment`, `Route`, `Config`, `Policy` graph nodes -> run `triage_walker` -> persist `IncidentHypothesis` -> `GET /walker/incident_state/{incident_id}` returns typed state for `cl {}` polling.
- Data representation impact (schemas, payload fields, indexes, validation):
  - completes Phase 1 node schema in Jac root persistence
  - adds typed incident-state payload for severity, deployment, primary signals, walker stage, and hypothesis
  - validates bounded `IncidentType` and typed hypothesis fields through Jac/byLLM types
- Communication contract impact:
  - input JSON shape changes:
    - `POST /walker/trigger_incident` must accept `incident_id`, `severity`, `deployment_id`, `signal_source`
  - output JSON shape changes:
    - `GET /walker/incident_state/{incident_id}` must return active incident summary plus `hypothesis`
  - backward-compatibility notes:
    - current bootstrap endpoints are placeholders only; no production compatibility burden exists yet
- Failure-mode and fallback plan for critical path:
  - expected failure condition:
    - mock signal endpoint unavailable
    - missing required vLLM metric names
    - unsupported incident type / low-confidence hypothesis
  - error response behavior:
    - fail closed with explicit incident status and no downstream execution behavior
  - fallback/degraded behavior:
    - persist incident with paused/manual-review-required state and expose plain status to UI
- FR ownership coverage map:
  - `FR-01` -> incident-state endpoint + minimal frontend incident feed
  - `FR-02` -> signal ingestion path on trigger
  - `FR-03` -> typed Jac graph nodes and edges
  - `FR-04` -> `triage_walker`
  - `FR-05` -> byLLM-backed bounded `IncidentType`
  - `FR-16` -> `mock_vllm.py` `/metrics` parsing using real metric names
- Slice coverage completeness check:
  - covers every included FR (`FR-01`, `FR-02`, `FR-03`, `FR-04`, `FR-05`, `FR-16`)
  - covers relevant NFRs (`NFR-P-01`, `NFR-P-02`, `NFR-U-01`, `NFR-U-02`, `NFR-R-01`, `NFR-C-01`, `NFR-C-02`)
- Expected evidence map:
  - Positive signals:
    - Jac nodes persist from root
    - `triage_walker` is the only walker with real Phase 1 behavior
    - typed incident state is accessible through Jac-published endpoints
    - frontend uses Jac `cl {}` instead of a separate app
  - Absent signals:
    - no separate Python incident orchestration service
    - no plan/execute/verify/rollback/audit code paths
  - Trigger behavior:
    - a trigger causes local signal ingestion, graph persistence, triage, and typed incident-state visibility
- Observed evidence references:
  - existing bootstrap in `main.jac`
  - Jac one-file full-stack model in `docs/external_apis.md/jaseci_api.md`
  - vLLM metrics contract in `docs/external_apis.md/vLLM.md`
- Match/Mismatch summary:
  - Match. This strategy matches the system design doc's Phase 1 handoff and Jac-native architecture most directly.
- Cloud/Infra feasibility check:
  - high feasibility; works within current local-only bootstrap and does not require extra provisioning
- NFR mapping:
  - strongest fit for startup speed, local compatibility, and 3-command Jac demo flow
- Risk and complexity rating (Low/Medium/High) with rationale:
  - Low/Medium risk, Low complexity. The file can grow, but the Phase 1 scope is still small and this preserves the sponsor architecture exactly.
- Strategy verdict (Accept/Reject) with reason:
  - Accept. Best architecture-conformant path for the active slice.

### Strategy S2 - Multi-Module Jac Runtime with Imported Slice Files
- What this strategy does (one sentence, plain language): keeps the full implementation Jac-native but splits Phase 1 behavior across multiple Jac modules imported from `main.jac` for schema, ingestion, walkers, and UI helpers.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3):
  - same Jac Graph Engine, Walker Pipeline, byLLM, Signal Ingester, and Jac frontend contracts as Phase 1
- External source references used:
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Components touched:
  - `main.jac`
  - new Jac module files for schema/ingestion/walker helpers
  - `mock_vllm.py`
  - shared bootstrap/runtime contract from `FT-OPS-INFRA-01`
- Boundary check per component:
  - Owns:
    - same Phase 1 responsibilities as S1
  - Must-Not-Do:
    - no non-Jac backend
    - no later-slice behaviors
- Primary implementation locus (where this strategy places core behavior: component/path/state transition):
  - `main.jac` as entrypoint plus imported Jac modules that divide schema, ingestion, endpoint logic, and UI helpers.
- Data flow across components (request/response/persistence path):
  - same as S1, but split across several Jac modules and import boundaries.
- Data representation impact (schemas, payload fields, indexes, validation):
  - same Phase 1 data model as S1, spread across multiple files
- Communication contract impact:
  - input JSON shape changes:
    - same as S1
  - output JSON shape changes:
    - same as S1
  - backward-compatibility notes:
    - still additive over bootstrap placeholders
- Failure-mode and fallback plan for critical path:
  - same failure handling as S1
- FR ownership coverage map:
  - `FR-01` -> frontend + incident-state module
  - `FR-02` -> ingestion module
  - `FR-03` -> schema module
  - `FR-04` -> triage module
  - `FR-05` -> byLLM typed classification module
  - `FR-16` -> mock metrics adapter module
- Slice coverage completeness check:
  - complete for all included FR/NFR IDs
- Expected evidence map:
  - Positive signals:
    - Jac-native modules with clear separations
    - no second backend
  - Absent signals:
    - no Python orchestration layer
  - Trigger behavior:
    - same as S1
- Observed evidence references:
  - current repo has only a single `main.jac` and no Jac module structure yet
- Match/Mismatch summary:
  - Partial Match. Architecture is valid, but it introduces file-structure complexity earlier than the design doc requires.
- Cloud/Infra feasibility check:
  - feasible locally
- NFR mapping:
  - satisfies the same NFR set as S1, but with slightly more setup overhead
- Risk and complexity rating (Low/Medium/High) with rationale:
  - Medium risk, Medium complexity because Jac module boundaries and imports would need to be introduced before the first slice proves the base path
- Strategy verdict (Accept/Reject) with reason:
  - Reject. Valid architecture, but premature structure for the current Phase 1 scope.

### Strategy S3 - Jac Frontend with Separate Python Ingestion/Triage Helper
- What this strategy does (one sentence, plain language): keeps the Jac frontend and some graph types in `main.jac` but moves signal ingestion and triage processing into a separate Python helper service that Jac calls.
- Architecture contract references (from `docs/SYSTEM_DESIGN_PLAN.md` Step 1.3):
  - Jac Graph Engine
  - Walker Pipeline
  - byLLM Integration
  - Signal Ingester
- External source references used:
  - `docs/external_apis.md/jaseci_api.md`
  - `docs/external_apis.md/vLLM.md`
- Components touched:
  - `main.jac`
  - new Python helper service
  - `mock_vllm.py`
- Boundary check per component:
  - Owns:
    - attempts to offload parsing and triage orchestration into Python
  - Must-Not-Do:
    - violates the chosen Jac-native runtime boundary by reintroducing a second backend locus
- Primary implementation locus (where this strategy places core behavior: component/path/state transition):
  - external Python helper plus Jac wrapper endpoints
- Data flow across components (request/response/persistence path):
  - trigger endpoint in Jac -> Python service fetches `/metrics` and computes hypothesis -> Jac stores results -> frontend polls state
- Data representation impact (schemas, payload fields, indexes, validation):
  - duplicates graph/hypothesis contract logic across Jac and Python
- Communication contract impact:
  - input JSON shape changes:
    - adds an internal Jac-to-Python helper contract
  - output JSON shape changes:
    - adds translation layers between helper and Jac
  - backward-compatibility notes:
    - creates unnecessary dual-runtime coupling
- Failure-mode and fallback plan for critical path:
  - expected failure condition:
    - helper service drift, contract mismatch, additional local-process failure
  - error response behavior:
    - more complex dual-runtime error surface
  - fallback/degraded behavior:
    - none that is better than a pure Jac implementation
- FR ownership coverage map:
  - could theoretically map all FRs, but ownership becomes split across runtimes
- Slice coverage completeness check:
  - incomplete in architecture terms because it breaks the Step 1.3 load-bearing runtime choice
- Expected evidence map:
  - Positive signals:
    - some reuse of prior Python patterns
  - Absent signals:
    - no pure Jac end-to-end Phase 1 path
  - Trigger behavior:
    - depends on a second backend process
- Observed evidence references:
  - the previously removed Python service already demonstrated why this diverges from the design
- Match/Mismatch summary:
  - Mismatch. Violates the load-bearing Jac/Jaseci architecture and reintroduces the exact drift the reset removed.
- Cloud/Infra feasibility check:
  - technically feasible, but structurally wrong for this repo
- NFR mapping:
  - weakens `NFR-C-02`, `NFR-U-03`, and the architecture constraints behind the demo stack
- Risk and complexity rating (Low/Medium/High) with rationale:
  - High risk, High complexity because it recreates the rejected split-stack design
- Strategy verdict (Accept/Reject) with reason:
  - Reject. Not architecture-conformant.

### Final convergence block
- Rejected Strategy IDs + rule-out reason:
  - `S2`: valid but too much structural overhead for the first Jac-native slice
  - `S3`: violates the selected Jac/Jaseci runtime architecture and reintroduces split-stack drift
- Selected Strategy ID: `S1`
- Confidence score (%): 92%
- Decision rationale (why it best fits full slice behavior):
  - `S1` implements the full Phase 1 capability directly on the chosen Jac/Jaseci architecture, matches the one-file full-stack model supported by the external Jac docs, preserves the system design’s component boundaries, and minimizes accidental complexity while the repo is still establishing the first real slice.
- Architecture conformance statement:
  - Selected strategy preserves Step 1.3 component boundaries, Phase 1 data flow, typed communication contracts, fail-closed triage behavior, Jac-native runtime choice, mock vLLM compatibility, and local single-virtualenv constraints.

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
