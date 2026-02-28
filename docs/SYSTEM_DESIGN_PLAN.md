# STAGE 1 OUTPUT: SYSTEM ARCHITECTURE

**Sources:** stage_0.5_output.md, walkerops_for_vllm.md, walkerops_for_vllm_system_design.md, jaseci_api.md, vLLM.md
**Product:** Ops Graph — Walker-Native Inference Incident Response

---

## 1.0 PREMISE

**Product name:** Ops Graph (WalkerOps for vLLM)

**Problem:**
Operators of inference-serving infrastructure currently triage and resolve latency incidents manually — bouncing across alerts, deployment state, route state, config state, and policy rules with no structured coordination. Existing tools either alert without acting (PagerDuty) or suggest without executing (LangChain agents). The result: 30–40 minute MTTR, high error risk under pressure, and zero audit trail.

**Who for:**
- Primary: ML platform engineer / inference engineer responsible for serving reliability
- Secondary: Engineering manager who needs lower MTTR and safer rollouts
- Judges: Hackathon judges who need to run, follow, and understand the product in 2–3 minutes

**Desired outcome:**
- Reduce ambiguity during inference incidents
- Produce a safe, bounded remediation path with verification and rollback
- Show measurable time savings: manual baseline vs. automated walker pipeline
- Runnable 2–3 minute demo with visible graph reasoning

**What the product does:**
Ops Graph is a Jac/Jaseci-native agentic system that ingests vLLM-style runtime signals, converts them into typed graph state, and dispatches a sequential walker pipeline (triage → plan → execute → verify → rollback → audit) to resolve the incident autonomously within a policy-governed action boundary — with full auditability.

**Why it matters:**
- Inference incidents are a real, repetitive, multi-tool operational workflow
- Graph state is the natural model for incident context (nodes = operational entities, edges = causal relationships)
- Jac/Jaseci primitives are load-bearing: remove walkers → the pipeline collapses; remove byLLM → typed hypothesis disappears
- It is agentic by definition: goal (resolve incident) + tools (mocked ops primitives) + loop (triage→plan→execute→verify→rollback) + guardrails (policy gate, confidence threshold, allowlist) + product surface (UI with 4 panels + MTTR dashboard)
- It is differentiated: not passive monitoring, not a chatbot, not prompt glue — typed, auditable, governed action

---

## 1.1 FUNCTIONAL REQUIREMENTS

Ordered by workflow. Pattern: {Actor} shall {action} {condition/purpose}.

| ID | Requirement |
|---|---|
| FR-01 | User shall view an active incident with its current severity, affected deployment, and primary signals so the workflow starts from a clear operational state. |
| FR-02 | System shall ingest alert, deployment, route, config, and policy inputs when an incident is triggered so the agent has the minimum operational context required for diagnosis. |
| FR-03 | System shall map the ingested inputs into typed graph nodes and edges so the workflow operates on structured state instead of free-text context. |
| FR-04 | `triage_walker` shall traverse the incident graph starting at the Incident node and visit Alert, Deployment, Config, and Policy nodes to produce a typed incident hypothesis when sufficient context is available. |
| FR-05 | System shall classify the incident into one of a bounded set of supported incident types when triage completes so downstream planning remains safe and testable. |
| FR-06 | `plan_walker` shall generate a typed remediation workflow containing ordered action steps, a verification condition, and a rollback flag when the incident type is supported. |
| FR-07 | System shall evaluate Policy node constraints — action allowlist, confidence threshold, approval requirement — before any operational action is executed so unsafe or disallowed actions are blocked. |
| FR-08 | System shall pause execution and expose an approval endpoint when a Policy node marks the incident as approval-gated so the product can operate in supervised mode. |
| FR-09 | `execute_walker` shall perform only actions present in the hardcoded allowlist when policy and approval checks pass so execution remains bounded. |
| FR-10 | System shall update graph state after each executed action so the current operational state remains traceable and subsequent walkers operate on accurate context. |
| FR-11 | `verify_walker` shall compare post-action metric values against expected recovery conditions after execution so the system can determine whether the incident is actually resolving. |
| FR-12 | `rollback_walker` shall restore the known-good deployment path when verification fails so the system can recover from a bad remediation attempt without operator intervention. |
| FR-13 | `audit_walker` shall emit a machine-readable and human-readable timeline entry for every significant pipeline step — triage, plan, policy check, execute, verify, rollback — so operators and judges can inspect exactly what happened. |
| FR-14 | User shall see typed triage output, typed remediation plan, verification state, and audit log in the product UI so the agent's work is fully visible within 2–3 minutes of demo start. |
| FR-15 | System shall calculate and display time-to-diagnosis, time-to-safe-action, and time-to-recovery against a manual baseline so productivity gains are measurable on screen. |
| FR-16 | System shall ingest mock vLLM Prometheus metrics using real vLLM metric names from the `/metrics` endpoint so the demo signal layer maps to a believable production system. |

---

## 1.2 NON-FUNCTIONAL REQUIREMENTS

### Performance
| ID | Requirement |
|---|---|
| NFR-P-01 | System shall render the initial incident view within 2 seconds in the demo environment. |
| NFR-P-02 | System shall complete graph triage and remediation planning within 5 seconds in the demo environment. |
| NFR-P-03 | End-to-end happy-path demo flow shall complete within 3 minutes. |
| NFR-P-04 | Frontend shall poll backend for walker state updates at 1-second intervals so live walker progress is visible without WebSocket infrastructure. |

### Security
| ID | Requirement |
|---|---|
| NFR-S-01 | System shall restrict execution to an explicit hardcoded allowlist of remediation action types: `shift_traffic`, `set_deployment_status`, `rollback_config`. |
| NFR-S-02 | System shall block execution and emit a `POLICY_BLOCKED` audit entry when Policy node denies action or confidence is below threshold (default: 0.80). |
| NFR-S-03 | System shall support an approval-gated mode that pauses at `execute_walker` and exposes a manual approval endpoint before proceeding. |

### Usability
| ID | Requirement |
|---|---|
| NFR-U-01 | Product UI shall make the active incident, current walker stage, chosen action, and final resolution status visible without requiring log inspection. |
| NFR-U-02 | System shall produce typed outputs alongside plain-language summaries that a non-expert judge can understand. |
| NFR-U-03 | Full setup (mock vLLM server + Jac backend + frontend) shall be runnable from a single README with 3 commands. |

### Reliability
| ID | Requirement |
|---|---|
| NFR-R-01 | System shall fail closed on unsupported incident types: no action taken, incident marked `manual_review_required`. |
| NFR-R-02 | System shall preserve a complete audit trail even when verification fails or rollback is triggered. |
| NFR-R-03 | System shall define explicit error responses for: missing signal data, policy denial, low confidence, execution failure, verification failure, and rollback failure. |

### Compatibility
| ID | Requirement |
|---|---|
| NFR-C-01 | Mock vLLM signal server shall serve metrics using real vLLM Prometheus metric names: `vllm:e2e_request_latency_seconds`, `vllm:kv_cache_usage_perc`, `vllm:num_requests_running`, `vllm:request_success_total`. |
| NFR-C-02 | System shall run locally on macOS and Linux from a single virtualenv with no GPU, no Kubernetes, and no external database. |

---

## 1.2.1 FEASIBILITY AUDIT (Against API Docs)

> SOP step: audit premise and FRs against sponsor documentation before writing architecture.

### Jaseci/Jac Audit

| Premise Claim | Doc Evidence | Feasibility |
|---|---|---|
| `node` declarations model operational entities | `node Task { has title: str; }` confirmed in jaseci_api.md; auto-persisted from root | ✅ CONFIRMED |
| `walker` with `visit` traverses typed graph | `walker W {}` + `visit [-->]` syntax confirmed | ✅ CONFIRMED |
| `by llm()` produces typed structured output | Return type is enforced — enum = only valid values, obj = all fields filled. `def triage_ticket(description: str) -> Priority by llm()` confirmed | ✅ CONFIRMED |
| `sem` provides additional LLM context | `sem X.field = "..."` confirmed as compiler directive, not a comment | ✅ CONFIRMED |
| `cl {}` codespace produces React frontend | `jac-client` plugin, `cl {}` block compiles to JavaScript/React, served from `jac start` | ✅ CONFIRMED |
| `jac start main.jac` serves HTTP API + frontend | Confirmed: HTTP server, walkers become REST endpoints, Swagger at /docs | ✅ CONFIRMED |
| Root persistence = no separate DB in hackathon | `root ++> Node(...)` persists automatically, SQLite locally | ✅ CONFIRMED |
| byLLM tool calling for walker actions | `by llm(tools=[fn1, fn2])` — LLM decides which tools to call | ✅ CONFIRMED |

**Cautions:**
- `⚠️` Real-time WebSocket push from walker to UI: NOT confirmed. **Mitigation:** use 1-second HTTP polling from `cl{}` frontend (NFR-P-04). Sufficient for demo cadence.
- `⚠️` byLLM requires LLM provider API key. **Mitigation:** README specifies `export ANTHROPIC_API_KEY=...` as step 1.

### vLLM Audit

| Premise Claim | Doc Evidence | Feasibility |
|---|---|---|
| vLLM exposes `/metrics` HTTP endpoint | `curl http://0.0.0.0:8000/metrics` confirmed, Prometheus-compatible format | ✅ CONFIRMED |
| `vllm:e2e_request_latency_seconds` available | Listed as Histogram in Grafana dashboard key metrics | ✅ CONFIRMED |
| `vllm:kv_cache_usage_perc` available (context pressure) | Listed as Gauge, 0–1 fraction of used KV cache blocks | ✅ CONFIRMED |
| `vllm:num_requests_running/_waiting` available | Listed as Gauges, confirmed in Prometheus example output | ✅ CONFIRMED |
| `vllm:request_success_total` available | Listed as Counter, labelled by `finished_reason` (stop/length/abort) | ✅ CONFIRMED |
| Can mock the `/metrics` endpoint for hackathon | Prometheus text format is simple key-value lines; trivially reproducible with a Python HTTP server | ✅ CONFIRMED |
| Deployment, route, config are real vLLM concepts | vLLM has API server → engine core → GPU worker process hierarchy; canary/baseline deployment patterns are real | ✅ CONFIRMED |

**Finding:** All signal types used in the demo incident scenario (`p95_latency_high`, `kv_cache_pressure`) map to real vLLM Prometheus metrics. Mock server is trivially buildable. No GPU required — mock signals are sufficient for hackathon demo.

---

## 1.3 SYSTEM ARCHITECTURE BLUEPRINT

### Components

| Component | Responsibility | Must NOT |
|---|---|---|
| **Jac Graph Engine** | Declare and persist all typed nodes and edges via OSP. Serve as the single source of truth for operational state throughout the pipeline. | Store free-text blobs. Mutate state outside of walker execution. |
| **Walker Pipeline** | Orchestrate the sequential execution of triage → plan → execute → verify → rollback → audit walkers. Each walker traverses graph state, does bounded work, updates graph, and yields to the next. | Skip policy gate. Execute actions outside allowlist. Proceed if confidence < threshold. |
| **byLLM Integration** | Delegate typed semantic functions (incident classification, hypothesis generation, plan summary) to an LLM via `by llm()`. Type system enforces output correctness. | Call byLLM for graph traversal decisions, policy evaluation, action selection, state mutation, or verification logic. |
| **Mock vLLM Signal Server** | Serve Prometheus-formatted metrics at `GET /metrics` using real vLLM metric names. Simulate a canary rollout incident scenario on demand. | Return non-standard metric names. Require a real GPU or real vLLM instance. |
| **Signal Ingester** | Poll the mock vLLM signal server at incident start. Map metric threshold breaches to `Alert` nodes and current values to `Metric` nodes in the graph. | Interpret signal semantics — that is `triage_walker`'s job. |
| **Policy Engine** | Evaluate `Policy` nodes against the proposed action. Check: action in allowlist, confidence ≥ threshold, approval not required. Block or pass. | Generate actions. Suggest alternatives. |
| **Action Executor** | Call mocked operational tool functions (`shift_traffic`, `set_deployment_status`, `rollback_config`) when policy passes. Update graph state with action result. | Call tools not on the hardcoded allowlist. Execute without a policy pass result. |
| **Jac React Frontend** | Render 4 panels (Incident Feed, Graph View, Typed Decisions, Audit Log) + MTTR metrics dashboard. Poll backend every 1 second for walker stage updates. | Contain business logic. Directly mutate graph state. |
| **Audit Store** | Persist `AuditEntry` nodes on the Jac graph, append-only. One entry per pipeline step. Accessible by frontend. | Overwrite or delete audit entries. |

FR IDs covered: FR-01 through FR-16
NFR IDs covered: NFR-P-01, NFR-P-02, NFR-P-04, NFR-S-01 through NFR-S-03, NFR-U-01, NFR-R-01 through NFR-R-03, NFR-C-01, NFR-C-02

---

### Responsibilities and Boundaries

**Walker Pipeline — detailed breakdown:**

```
triage_walker
  entry: Incident node
  visits: Alert → Deployment → Config → Policy
  byLLM call: classify_incident_type(signals) -> IncidentType (enum)
  byLLM call: generate_hypothesis(graph_neighborhood) -> IncidentHypothesis (obj)
  output: typed IncidentHypothesis written to Incident node
  boundary: no actions, no metric polling, no state mutation beyond hypothesis

plan_walker
  entry: Incident node (after triage completes)
  reads: IncidentHypothesis from Incident node
  byLLM call: generate_remediation_plan(hypothesis, policy) -> RemediationPlan (obj)
  output: typed RemediationPlan written to Incident node
  boundary: no actions, no metric polling

execute_walker
  entry: Incident node (after plan_walker completes)
  reads: RemediationPlan
  step 1: policy gate (Policy node evaluation, confidence check, approval check)
  step 2: for each action in plan.actions → call allowlisted tool function
  step 3: update graph state (Deployment node status, Route node traffic split)
  output: ActionResult nodes written to graph
  boundary: only calls allowlisted functions, fails closed on any gate failure

verify_walker
  entry: Incident node (after execute_walker completes)
  re-polls: mock vLLM /metrics for post-action metric values
  compares: observed p95_latency vs. expected_direction (down)
  output: VerificationResult node (pass | fail)
  boundary: no actions, read-only metric polling

rollback_walker
  entry: Incident node (only when verification fails)
  reads: ActionResult nodes to determine what was changed
  calls: inverse action (shift_traffic back to 0% canary, restore deployment status)
  output: RollbackResult node
  boundary: only inverts previously executed allowlisted actions

audit_walker
  entry: Incident node (runs on every path — success and failure)
  reads: all pipeline step nodes (Hypothesis, Plan, ActionResult, VerificationResult, RollbackResult)
  byLLM call: generate_summary(timeline) -> str (plain language for judges)
  output: AuditEntry nodes (typed machine-readable + plain string summary)
  boundary: read-only except for AuditEntry writes
```

FR IDs covered: FR-04, FR-06, FR-07, FR-08, FR-09, FR-10, FR-11, FR-12, FR-13
NFR IDs covered: NFR-S-01, NFR-S-02, NFR-S-03, NFR-R-01, NFR-R-02

---

### Data Flow

```
[Mock vLLM /metrics] ──GET /metrics──► [Signal Ingester]
                                              │
                                    maps threshold breaches
                                              │
                                              ▼
                                    [Jac Graph: Alert nodes,
                                     Metric nodes, Deployment
                                     nodes, Route nodes, Config
                                     nodes, Policy nodes]
                                              │
                                    incident_triggered()
                                              │
                                              ▼
                                    [triage_walker]
                                     └─ visits graph neighborhood
                                     └─ byLLM: IncidentHypothesis
                                              │
                                              ▼
                                    [plan_walker]
                                     └─ byLLM: RemediationPlan
                                              │
                                              ▼
                                    [Policy Engine]
                                     └─ allowlist check
                                     └─ confidence check
                                     └─ approval check
                                              │
                                  ┌───────────┴───────────┐
                                pass                     block
                                  │                        │
                                  ▼                        ▼
                          [execute_walker]         POLICY_BLOCKED
                           └─ tool calls            audit entry
                           └─ graph update         no action taken
                                  │
                                  ▼
                          [verify_walker]
                           └─ re-poll /metrics
                           └─ compare recovery
                                  │
                          ┌───────┴───────┐
                         pass           fail
                          │               │
                          ▼               ▼
                   [audit_walker]  [rollback_walker]
                   (success path)   └─ inverse actions
                                         │
                                         ▼
                                  [audit_walker]
                                  (failure path)
                                         │
                          ┌──────────────┘
                          ▼
                  AuditEntry nodes
                  written to graph
                          │
                          ▼
                  [Jac Frontend cl{}]
                  polls GET /incident_state/{id}
                  every 1 second
                          │
                   renders 4 panels +
                   MTTR dashboard
```

**Core Entities (Graph Schema):**

| Node Type | Key Fields | Relationships |
|---|---|---|
| `Incident` | `id`, `severity`, `status`, `created_at`, `resolved_at` | → Alert (1:N), → Deployment (1:1), → AuditEntry (1:N) |
| `Alert` | `id`, `type`, `threshold`, `observed_value`, `fired_at` | → Incident (N:1) |
| `Deployment` | `id`, `name`, `role` (baseline\|canary), `status`, `traffic_pct` | → Route (N:1), → Config (1:1) |
| `Route` | `id`, `name`, `baseline_pct`, `canary_pct` | → Deployment (1:N) |
| `Config` | `id`, `max_model_len`, `batch_size`, `dtype` | → Deployment (1:1) |
| `Policy` | `id`, `action_allowlist`, `confidence_threshold`, `approval_required` | → Incident (1:N) |
| `IncidentHypothesis` | `incident_type`, `root_cause`, `confidence`, `affected_node_ids` | → Incident (1:1) |
| `RemediationPlan` | `plan_id`, `actions[]`, `verification_metric`, `expected_direction`, `rollback_on_fail` | → Incident (1:1) |
| `ActionResult` | `action_type`, `target`, `params`, `status`, `executed_at` | → Incident (1:N) |
| `VerificationResult` | `metric`, `observed_value`, `expected_direction`, `passed`, `checked_at` | → Incident (1:1) |
| `RollbackResult` | `actions_reversed[]`, `status`, `completed_at` | → Incident (1:1) |
| `AuditEntry` | `step`, `timestamp`, `typed_data`, `plain_summary` | → Incident (1:N), append-only |

FR IDs covered: FR-02, FR-03, FR-10, FR-13, FR-15
NFR IDs covered: NFR-R-02, NFR-C-02

---

### Communication and Contracts

**Critical API flows:**

**1. Trigger incident**
```
POST /walker/trigger_incident
Body: {
  "incident_id": "inc_001",
  "severity": "high",
  "deployment_id": "deployment:canary",
  "signal_source": "mock_vllm"
}
Response: {
  "status": "pipeline_started",
  "incident_id": "inc_001",
  "poll_url": "/walker/incident_state/inc_001"
}
```

**2. Poll incident state (frontend polling every 1s)**
```
GET /walker/incident_state/{incident_id}
Response: {
  "incident_id": "inc_001",
  "current_stage": "execute_walker",  // triage | plan | policy_check | execute | verify | rollback | audit | resolved
  "hypothesis": {
    "incident_type": "rollout_regression",
    "root_cause": "canary deployment introduced latency regression under current context/config load",
    "confidence": 0.92,
    "affected_nodes": ["deployment:canary", "route:prod_split", "alert:p95_latency_high"]
  },
  "plan": {
    "plan_id": "plan_001",
    "actions": [
      {"step": 1, "type": "shift_traffic", "target": "route:prod_split", "params": {"canary_percentage": 0}},
      {"step": 2, "type": "set_deployment_status", "target": "deployment:canary", "params": {"status": "isolated"}}
    ],
    "verification": {"metric": "vllm:e2e_request_latency_seconds", "expected_direction": "down"},
    "rollback_on_fail": true
  },
  "verification": {"passed": true, "observed_p95_ms": 210, "threshold_ms": 800},
  "audit": [
    {"step": "triage", "timestamp": "...", "summary": "Identified canary rollout regression with 0.92 confidence."},
    {"step": "execute", "timestamp": "...", "summary": "Shifted 100% traffic to baseline. Canary isolated."},
    {"step": "verify", "timestamp": "...", "summary": "p95 latency recovered to 210ms (threshold: 800ms). Resolved."}
  ],
  "mttr_ms": 118000,
  "manual_baseline_ms": 2400000
}
```

**3. Mock vLLM incident signal**
```
GET http://localhost:9000/metrics
Response (Prometheus text format, simulated breach):
# HELP vllm:e2e_request_latency_seconds End-to-end request latency
# TYPE vllm:e2e_request_latency_seconds histogram
vllm:e2e_request_latency_seconds_bucket{le="0.5",model_name="canary"} 12.0
vllm:e2e_request_latency_seconds_bucket{le="1.0",model_name="canary"} 12.0
vllm:e2e_request_latency_seconds_bucket{le="2.0",model_name="canary"} 89.0
# HELP vllm:kv_cache_usage_perc KV cache utilization
# TYPE vllm:kv_cache_usage_perc gauge
vllm:kv_cache_usage_perc{model_name="canary"} 0.94
# HELP vllm:num_requests_running Number running
# TYPE vllm:num_requests_running gauge
vllm:num_requests_running{model_name="canary"} 47.0
vllm:num_requests_running{model_name="baseline"} 8.0
```

**4. byLLM typed function signatures (Jac):**
```jac
enum IncidentType { ROLLOUT_REGRESSION, CONFIG_PRESSURE, CAPACITY_SATURATION, UNKNOWN }

obj IncidentHypothesis {
    has incident_type: IncidentType;
    has root_cause: str;
    has confidence: float;
    has affected_node_ids: list[str];
}
sem IncidentHypothesis.confidence = "Float between 0.0 and 1.0. Only above 0.80 triggers execution.";

def classify_incident(signals: list[str], graph_context: str) -> IncidentHypothesis
    by llm();
sem classify_incident = "Analyze inference serving signals to identify the most likely root cause and incident type.";

obj RemediationPlan {
    has plan_id: str;
    has actions: list[dict];
    has verification_metric: str;
    has expected_direction: str;
    has rollback_on_fail: bool;
}

def generate_plan(hypothesis: IncidentHypothesis, policy: dict) -> RemediationPlan
    by llm();
sem generate_plan = "Generate the minimal safe remediation plan for the identified incident. Only include allowlisted actions.";
```

FR IDs covered: FR-04, FR-05, FR-06, FR-14, FR-15, FR-16
NFR IDs covered: NFR-P-04, NFR-U-02, NFR-C-01

---

### Failure Modes

| Failure | Trigger | Error Response | Fallback |
|---|---|---|---|
| Unsupported incident type | `classify_incident()` returns `IncidentType.UNKNOWN` | `{error: "UNSUPPORTED_INCIDENT_TYPE", action: "none", status: "manual_review_required"}` | Audit entry written, pipeline halts, incident flagged for operator |
| Policy blocks action | Policy node `action_allowlist` does not contain planned action type | `{error: "POLICY_BLOCKED", blocked_action: "...", status: "requires_approval"}` | Audit entry written, pipeline pauses at execute_walker, awaits manual approval |
| Low confidence | `hypothesis.confidence < 0.80` | `{error: "LOW_CONFIDENCE", confidence: X, status: "human_in_loop"}` | Audit entry written, no action taken, hypothesis shown to operator |
| Signal data unavailable | Mock vLLM server not responding | `{error: "SIGNAL_UNAVAILABLE", status: "paused"}` | triage_walker marks incident `STALE_DATA`, pipeline halts until signal refreshes |
| Execution tool fails | Mocked tool function throws exception | `{error: "EXECUTION_FAILED", action: "...", status: "partial_execution"}` | Partial actions rolled back if possible, audit entry written, incident escalated |
| Verification fails | `verify_walker` observes metric not recovering | `{error: "VERIFICATION_FAILED", rollback_triggered: true}` | `rollback_walker` automatically activated |
| Rollback fails | Inverse action call fails | `{error: "ROLLBACK_FAILED", status: "CRITICAL_MANUAL_INTERVENTION_REQUIRED"}` | Audit entry written with CRITICAL flag, pipeline halts, incident marked for immediate human action |

FR IDs covered: FR-07, FR-08, FR-11, FR-12, FR-13
NFR IDs covered: NFR-R-01, NFR-R-02, NFR-R-03, NFR-S-01, NFR-S-02

---

### Technology Stack

| Layer | Technology | Why Chosen | Alternatives Considered | Key Tradeoff |
|---|---|---|---|---|
| Language / Runtime | Jac/Jaseci (jaclang, byllm, jac-client) | Required by hackathon; load-bearing walkers, OSP, byLLM, React frontend all in one tool | Python + LangChain (rejected: prompt glue, no typed graph) | Jac is newer — smaller community, fewer Stack Overflow answers |
| LLM Provider | Anthropic Claude Haiku (via byllm) | Fast inference for demo latency (< 2s), low cost, team likely has API key | OpenAI GPT-4o-mini (also viable, same integration path via byllm) | Haiku is cheaper/faster; Sonnet is more accurate — Haiku sufficient for typed enum returns |
| Graph Persistence | Jac root (SQLite local) | Zero config, no external DB process, confirmed in jaseci_api.md | PostgreSQL (rejected: overkill for hackathon, adds setup friction) | SQLite not production-scale but perfectly sufficient for demo |
| Frontend | React via Jac `cl {}` codespace | Same file as backend — no separate frontend project, confirmed in jaseci_api.md | Separate React app (rejected: adds complexity, slower to build) | Jac client codespace is less flexible than raw React — acceptable for 4-panel demo layout |
| Mock Signal Server | Python `http.server` or FastAPI | Trivial to write, serves Prometheus text format, no dependencies | Real vLLM instance (rejected: requires GPU, not available at hackathon) | Mock cannot simulate dynamic metric evolution — use a scripted scenario sequence instead |
| Frontend-Backend Sync | HTTP polling (1s interval) | Confirmed feasible via `jac start` REST endpoints; no WebSocket complexity | WebSocket push (not confirmed available in Jac client codespace — NFR-P-04 mitigation) | 1s polling adds 0–1s display lag — acceptable for demo pacing |
| HTTP Server | FastAPI (via `jac start`) | Automatically provisioned when `jac start main.jac` is run | None — Jac handles this | No configuration needed |

Decision rationale — Jaseci as the entire backend:
- **Why chosen:** Walkers ARE the pipeline. Removing Jac → pipeline becomes Python if/else → loses typed graph traversal, byLLM, and OSP. This is the load-bearing argument.
- **Key assumption:** byllm integration works reliably with Anthropic API key. Confirmed by jaseci_api.md examples.
- **Key tradeoff:** Jac is less mature than Python ecosystem. Mitigated by: team has Jac expertise (it's the hackathon sponsor language), docs are clear, examples run.

---

## 1.3 ARCHITECTURE COVERAGE GATE

### FR Coverage Matrix

| FR_ID | Mapped | 1.3 Section | Owning Component / Path |
|---|---|---|---|
| FR-01 | Y | Frontend | Jac React Frontend → Panel 1 (Incident Feed) |
| FR-02 | Y | Data Flow | Signal Ingester → Mock vLLM poll → Alert/Deployment/Config/Route nodes |
| FR-03 | Y | Data Flow + Entities | Jac Graph Engine (OSP) → typed node/edge schema |
| FR-04 | Y | Walker Pipeline | `triage_walker` → graph traversal → byLLM hypothesis |
| FR-05 | Y | Contracts | byLLM `IncidentType` enum — type system enforces bounded values |
| FR-06 | Y | Walker Pipeline | `plan_walker` → byLLM `RemediationPlan` obj |
| FR-07 | Y | Walker Pipeline + Failure Modes | Policy Engine → allowlist + confidence + approval checks |
| FR-08 | Y | Failure Modes | Policy Engine → approval_gated pause + manual approval endpoint |
| FR-09 | Y | Walker Pipeline | Action Executor → hardcoded allowlist check before tool call |
| FR-10 | Y | Data Flow | Action Executor → graph state update (Deployment, Route node mutation) |
| FR-11 | Y | Walker Pipeline | `verify_walker` → re-poll mock vLLM → compare recovery condition |
| FR-12 | Y | Walker Pipeline | `rollback_walker` → inverse actions on verification fail |
| FR-13 | Y | Walker Pipeline + Entities | `audit_walker` → AuditEntry nodes, both paths (success + failure) |
| FR-14 | Y | Frontend + Contracts | Jac React Frontend → 4 panels; polled via GET /incident_state |
| FR-15 | Y | Frontend + Contracts | MTTR panel → `resolved_at - created_at` vs. manual baseline constant |
| FR-16 | Y | Components + Contracts | Mock vLLM Signal Server → real metric names confirmed against vLLM.md |

**All 16 FRs mapped. Gate: PASS ✅**

---

### NFR Coverage Matrix

| NFR_ID | Mapped | 1.3 Section | Enforcing Layer / Mechanism |
|---|---|---|---|
| NFR-P-01 | Y | Technology Stack | Jac start serves pre-bundled React; SQLite graph read for initial incident node < 2s |
| NFR-P-02 | Y | Walker Pipeline + Technology Stack | Haiku inference < 2s per byLLM call; 2 byLLM calls in triage+plan ≤ 5s total |
| NFR-P-03 | Y | Walker Pipeline | Scripted demo scenario; sequential walker pipeline estimated 60–90s end-to-end |
| NFR-P-04 | Y | Communication and Contracts | Frontend polls `GET /incident_state` every 1s; no WebSocket required |
| NFR-S-01 | Y | Components + Failure Modes | Action Executor allowlist: hardcoded `["shift_traffic", "set_deployment_status", "rollback_config"]` |
| NFR-S-02 | Y | Components + Failure Modes | Policy Engine gate blocks on confidence < 0.80 or policy denial; POLICY_BLOCKED audit entry |
| NFR-S-03 | Y | Components + Failure Modes | `approval_required: true` on Policy node → execute_walker pauses, exposes approval endpoint |
| NFR-U-01 | Y | Frontend | Panel 2 (Graph View) shows active walker stage via 1s poll; Panel 3 shows current decision |
| NFR-U-02 | Y | Contracts + Walker Pipeline | `audit_walker` byLLM call produces plain-language summary alongside typed output |
| NFR-U-03 | Y | Technology Stack | README: (1) `export ANTHROPIC_API_KEY=...` (2) `python mock_vllm.py` (3) `jac start main.jac` |
| NFR-R-01 | Y | Failure Modes | `triage_walker` fails closed on `IncidentType.UNKNOWN` — no execute_walker activation |
| NFR-R-02 | Y | Components + Failure Modes | `audit_walker` runs on both success and failure paths; AuditEntry written before pipeline exit |
| NFR-R-03 | Y | Failure Modes | Explicit error enum defined for 7 failure modes with specific response shapes and fallbacks |
| NFR-C-01 | Y | Contracts | Mock vLLM server uses `vllm:e2e_request_latency_seconds`, `vllm:kv_cache_usage_perc`, `vllm:num_requests_running`, `vllm:request_success_total` — all confirmed in vLLM.md |
| NFR-C-02 | Y | Technology Stack | SQLite (zero config), Jac (pip install), mock server (Python stdlib) — no GPU, no K8s, no external DB |

**All 15 NFRs mapped. Gate: PASS ✅**

---

## STAGE HANDOFF

**Stage 1 status: COMPLETE ✅**

This architecture feeds into Stage 2 (build). The build order follows the execution hedge from Stage 0.5:

```
PHASE 1 — Runnable baseline (triage_walker + graph schema + mock vLLM + minimal UI):
  main.jac: node declarations, triage_walker, byLLM classify_incident
  mock_vllm.py: serves /metrics with incident scenario
  UI: Panel 1 (incident feed) + Panel 3 (hypothesis output)

PHASE 2 — Full walker pipeline (plan → execute → verify → rollback → audit):
  main.jac: plan_walker, execute_walker (with policy gate), verify_walker, rollback_walker, audit_walker
  UI: Panel 2 (graph view with walker stage) + Panel 4 (audit log)

PHASE 3 — Polish (MTTR dashboard + demo script):
  UI: MTTR panel (manual baseline vs. automated)
  Demo script: trigger → watch pipeline → show audit trail
  README: 3-command setup
```

**At the end of Phase 1:** submittable product (matches IDEA A v2.0 — READY, 91.1% avg)
**At the end of Phase 2:** target product (matches IDEA B v3.0 — READY, 93.4% avg)
**At the end of Phase 3:** polished demo for judges
