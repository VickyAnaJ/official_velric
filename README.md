# Ops Graph

**Walker-Native Inference Incident Response for vLLM**

Ops Graph is a Jac/Jaseci-native agentic system that ingests vLLM-style runtime signals, converts them into typed graph state, and dispatches a sequential walker pipeline to resolve inference incidents autonomously — with full auditability.

## Problem

Operators of inference-serving infrastructure triage and resolve latency incidents manually — bouncing across alerts, deployment state, route state, config state, and policy rules with no structured coordination. The result: 30-40 minute MTTR, high error risk under pressure, and zero audit trail.

## What Ops Graph Does

1. **Ingests** mock vLLM Prometheus metrics (real metric names)
2. **Builds** typed graph state (Incident, Alert, Deployment, Route, Config, Policy nodes)
3. **Runs** a 6-walker pipeline: `triage` > `plan` > `execute` > `verify` > `rollback` > `audit`
4. **Enforces** policy-gated execution with allowlist, confidence threshold, and approval controls
5. **Verifies** post-action metrics and triggers automatic rollback on failure
6. **Produces** an append-only audit trail with MTTR metrics

## Architecture

```
Mock vLLM /metrics ──> Signal Ingester ──> Jac Graph Engine (OSP)
                                                   │
                                          triage_walker (byLLM)
                                                   │
                                          plan_walker (byLLM)
                                                   │
                                          Policy Engine (allowlist + confidence gate)
                                                   │
                                     ┌─────────────┴─────────────┐
                                   PASS                        BLOCK
                                     │                           │
                              execute_walker              POLICY_BLOCKED
                                     │                     (no action)
                              verify_walker
                                     │
                              ┌──────┴──────┐
                            pass          fail
                              │             │
                        audit_walker   rollback_walker
                        (resolved)          │
                                      audit_walker
                                      (rolled back)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Language / Runtime | Jac/Jaseci (jaclang 0.11.2, byllm, jac-client) |
| LLM Provider | Anthropic Claude via byllm (with deterministic fallback) |
| Graph Persistence | Jac root (SQLite, auto-managed) |
| Frontend | React via Jac `cl {}` codespace |
| Mock Signal Server | Python `http.server` (Prometheus text format) |
| HTTP Server | FastAPI (auto-provisioned by `jac start`) |

## Project Structure

```
├── main.jac              # Full Jac entrypoint (walkers, graph, endpoints, UI)
├── mock_vllm.py          # Mock vLLM Prometheus metrics server
├── jac.toml              # Jac project config
├── requirements.txt      # Python dependencies (jaseci>=2.3.1)
├── Makefile              # Build/test targets
├── scripts/              # Test runners
│   ├── test_unit.sh
│   ├── test_integration.sh
│   └── test_coverage.sh
├── tests/
│   ├── unit/             # 24 unit tests
│   └── integration/      # 14 integration tests
├── tools/
│   ├── bootstrap_check.py
│   └── check_coverage.py
└── docs/
    ├── SYSTEM_DESIGN_PLAN.md
    └── external_apis.md/
        ├── jaseci_api.md
        └── vLLM.md
```

## One-Time Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional — enables LLM-backed triage, planning, and audit summaries:

```bash
export ANTHROPIC_API_KEY=your-key
```

Without `ANTHROPIC_API_KEY`, the system still runs fully using deterministic fallback logic.

## Start the System

**Terminal 1** — Mock vLLM metrics server:

```bash
source .venv/bin/activate
python3 mock_vllm.py
```

**Terminal 2** — Jac application:

```bash
source .venv/bin/activate
jac start main.jac
```

Services:

| Service | URL |
|---|---|
| Mock vLLM metrics | http://127.0.0.1:9000/metrics |
| Jac app | http://127.0.0.1:8000 |
| Swagger API docs | http://127.0.0.1:8000/docs |

## API Endpoints

All endpoints use `POST` with JSON body at `/function/<name>`.

### Trigger an Incident

```bash
curl -X POST http://127.0.0.1:8000/function/trigger_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "inc_001", "severity": "high", "deployment_id": "deployment:canary", "signal_source": "mock_vllm"}'
```

Ingests metrics, builds the graph, runs `triage_walker`, and returns the typed hypothesis.

### Execute Full Pipeline

```bash
curl -X POST http://127.0.0.1:8000/function/execute_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "inc_001"}'
```

Runs `plan` > `execute` > `verify` > `rollback` > `audit` and returns the full lifecycle state including MTTR metrics.

Optional parameters:

| Param | Type | Default | Purpose |
|---|---|---|---|
| `confidence` | float | 0.92 | Policy confidence threshold override |
| `require_approval` | bool | false | Enable approval-gated mode |
| `approval_token` | string | "" | Token for approval (must start with `apr_`) |
| `force_verification_failure` | bool | false | Force rollback path (demo) |
| `force_fail` | bool | false | Force action execution failure |

### Get Incident State

```bash
curl -X POST http://127.0.0.1:8000/function/get_incident_state \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "inc_001"}'
```

Returns: hypothesis, plan, policy decision, action results, verification, rollback, audit trail, and MTTR metrics.

## Demo Scenarios

### Happy path (incident resolved)

```bash
# 1. Trigger incident
curl -X POST http://127.0.0.1:8000/function/trigger_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "demo_001", "severity": "high"}'

# 2. Execute pipeline — resolves automatically
curl -X POST http://127.0.0.1:8000/function/execute_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "demo_001"}'
```

### Rollback path (verification fails)

```bash
curl -X POST http://127.0.0.1:8000/function/trigger_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "demo_rollback", "severity": "critical"}'

curl -X POST http://127.0.0.1:8000/function/execute_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "demo_rollback", "force_verification_failure": true}'
```

### Policy blocked (low confidence)

```bash
curl -X POST http://127.0.0.1:8000/function/trigger_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "demo_blocked"}'

curl -X POST http://127.0.0.1:8000/function/execute_incident \
  -H "Content-Type: application/json" \
  -d '{"incident_id": "demo_blocked", "confidence": 0.5}'
```

## Testing

```bash
make build                    # Verify bootstrap artifacts
./scripts/test_unit.sh        # 24 unit tests
./scripts/test_integration.sh # 14 integration tests
./scripts/test_coverage.sh    # Coverage gate (threshold: 25%)
```

## Walker Pipeline Details

| Walker | Responsibility | byLLM | Output |
|---|---|---|---|
| `triage_walker` | Traverse graph, classify incident type | `classify_incident()` | IncidentHypothesis |
| `plan_walker` | Generate typed remediation plan | `generate_plan()` | RemediationPlan |
| `execute_walker` | Policy gate + run allowlisted actions | - | ActionResult nodes |
| `verify_walker` | Compare post-action metrics | - | VerificationResult |
| `rollback_walker` | Inverse actions on verification failure | - | RollbackResult |
| `audit_walker` | Emit timeline + MTTR metrics | `summarize_audit_step()` | AuditEntry nodes |

### Policy Controls

- **Action allowlist:** `shift_traffic`, `set_deployment_status`, `rollback_config`
- **Confidence threshold:** 0.80 (below = POLICY_BLOCKED)
- **Approval gate:** optional manual approval with `apr_` prefixed token

## Notes

- The system uses real vLLM Prometheus metric names against a mock server — no GPU required
- Generated runtime artifacts (`.jac/`, `__pycache__/`) are gitignored
- All walkers have deterministic fallback paths when no LLM API key is configured
