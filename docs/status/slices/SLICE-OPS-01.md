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
