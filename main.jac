enum IncidentType { ROLLOUT_REGRESSION, CONFIG_PRESSURE, CAPACITY_SATURATION, UNKNOWN }

obj IncidentHypothesis {
    has incident_type: IncidentType;
    has root_cause: str;
    has confidence: float;
    has affected_node_ids: list[str];
}
sem IncidentHypothesis.confidence = "Float between 0.0 and 1.0. Only above 0.80 triggers execution.";

obj RemediationPlan {
    has plan_id: str;
    has actions: list[dict];
    has verification_metric: str;
    has expected_direction: str;
    has rollback_on_fail: bool;
}

obj VerificationResult {
    has passed: bool;
    has observed_value: float;
    has expected_direction: str;
    has metric: str;
}

obj AuditEntry {
    has step: str;
    has typed_data: dict;
    has plain_summary: str;
}

node Incident {
    has incident_id: str;
    has severity: str;
    has created_at: str;
    has status: str = "active";
    has deployment_id: str = "deployment:canary";
    has current_stage: str = "bootstrap";
    has signal_source: str = "mock_vllm";
    has primary_signal_names: list[str] = [];
    has hypothesis_type: str = "UNKNOWN";
    has hypothesis_summary: str = "";
    has hypothesis_confidence: float = 0.0;
    has requires_manual_review: bool = False;
    has latest_metrics_payload: str = "";
    has resolved_at: str | None = None;
}

node Alert {
    has alert_id: str;
    has alert_type: str;
    has threshold: float;
    has observed_value: float;
    has fired_at: str;
}

node Metric {
    has metric_name: str;
    has metric_value: float;
    has model_name: str;
}

node Deployment {
    has deployment_id: str;
    has name: str;
    has role: str;
    has status: str;
    has traffic_pct: int;
}

node Route {
    has route_id: str;
    has baseline_pct: int;
    has canary_pct: int;
}

node Config {
    has config_id: str;
    has max_model_len: int;
    has batch_size: int;
    has dtype: str;
}

node Policy {
    has policy_id: str;
    has action_allowlist: list[str];
    has confidence_threshold: float;
    has approval_required: bool;
}

def classify_incident(signals: list[str], graph_context: str) -> IncidentHypothesis
    by llm();
sem classify_incident = "Analyze inference serving signals and graph context to produce a typed hypothesis.";

def generate_plan(hypothesis: IncidentHypothesis, policy: dict) -> RemediationPlan
    by llm();
sem generate_plan = "Generate the minimal safe remediation plan for the identified incident using allowlisted actions only.";

def required_metric_names() -> list[str] {
    return [
        "vllm:e2e_request_latency_seconds",
        "vllm:kv_cache_usage_perc",
        "vllm:num_requests_running",
        "vllm:request_success_total",
    ];
}

def phase_1_metrics_payload(scenario: str = "rollout_regression") -> str {
    if scenario == "healthy" {
        return """
# HELP vllm:e2e_request_latency_seconds End-to-end request latency
# TYPE vllm:e2e_request_latency_seconds histogram
vllm:e2e_request_latency_seconds{model_name="canary"} 0.18
# HELP vllm:kv_cache_usage_perc KV cache utilization
# TYPE vllm:kv_cache_usage_perc gauge
vllm:kv_cache_usage_perc{model_name="canary"} 0.42
# HELP vllm:num_requests_running Number running
# TYPE vllm:num_requests_running gauge
vllm:num_requests_running{model_name="canary"} 6.0
vllm:num_requests_running{model_name="baseline"} 8.0
# HELP vllm:request_success_total Number of successful requests
# TYPE vllm:request_success_total counter
vllm:request_success_total{finished_reason="stop"} 2401.0
""";
    }

    return """
# HELP vllm:e2e_request_latency_seconds End-to-end request latency
# TYPE vllm:e2e_request_latency_seconds histogram
vllm:e2e_request_latency_seconds{model_name="canary"} 1.34
# HELP vllm:kv_cache_usage_perc KV cache utilization
# TYPE vllm:kv_cache_usage_perc gauge
vllm:kv_cache_usage_perc{model_name="canary"} 0.94
# HELP vllm:num_requests_running Number running
# TYPE vllm:num_requests_running gauge
vllm:num_requests_running{model_name="canary"} 47.0
vllm:num_requests_running{model_name="baseline"} 8.0
# HELP vllm:request_success_total Number of successful requests
# TYPE vllm:request_success_total counter
vllm:request_success_total{finished_reason="stop"} 1821.0
""";
}

def parse_prometheus_metrics(payload: str) -> dict {
    metrics = {};
    for raw_line in payload.split("\n") {
        line = raw_line.strip();
        if line == "" or line.startswith("#") {
            continue;
        }
        metric_key = line.split(" ")[0];
        metric_name = metric_key.split("{")[0];
        metric_value = float(line.split(" ")[-1]);
        metrics[metric_name] = metric_value;
    }
    return metrics;
}

def primary_signal_names(metrics: dict) -> list[str] {
    signals = [];
    if metrics.get("vllm:e2e_request_latency_seconds", 0.0) > 1.0 {
        signals.append("p95_latency_high");
    }
    if metrics.get("vllm:kv_cache_usage_perc", 0.0) > 0.90 {
        signals.append("kv_cache_pressure");
    }
    if metrics.get("vllm:num_requests_running", 0.0) > 40.0 {
        signals.append("request_queue_growth");
    }
    return signals;
}

def fallback_incident_hypothesis(metrics: dict, signals: list[str]) -> IncidentHypothesis {
    if "p95_latency_high" in signals and "kv_cache_pressure" in signals {
        return IncidentHypothesis(
            incident_type=IncidentType.ROLLOUT_REGRESSION,
            root_cause="Canary deployment is serving elevated latency under high KV cache pressure.",
            confidence=0.92,
            affected_node_ids=[
                "deployment:canary",
                "route:prod_split",
                "alert:p95_latency_high",
            ],
        );
    }
    if "kv_cache_pressure" in signals {
        return IncidentHypothesis(
            incident_type=IncidentType.CONFIG_PRESSURE,
            root_cause="Serving configuration is exhausting KV cache blocks for the active deployment.",
            confidence=0.85,
            affected_node_ids=[
                "deployment:canary",
                "config:deployment_canary",
            ],
        );
    }
    return IncidentHypothesis(
        incident_type=IncidentType.UNKNOWN,
        root_cause="Signal pattern is not in the bounded Phase 1 incident set.",
        confidence=0.40,
        affected_node_ids=["deployment:canary"],
    );
}

def metric_nodes_from_snapshot(metrics: dict) -> list[Metric] {
    return [
        Metric(metric_name="vllm:e2e_request_latency_seconds", metric_value=metrics.get("vllm:e2e_request_latency_seconds", 0.0), model_name="canary"),
        Metric(metric_name="vllm:kv_cache_usage_perc", metric_value=metrics.get("vllm:kv_cache_usage_perc", 0.0), model_name="canary"),
        Metric(metric_name="vllm:num_requests_running", metric_value=metrics.get("vllm:num_requests_running", 0.0), model_name="canary"),
        Metric(metric_name="vllm:request_success_total", metric_value=metrics.get("vllm:request_success_total", 0.0), model_name="canary"),
    ];
}

def build_incident_view(incident: Incident, hypothesis: IncidentHypothesis) -> dict {
    return {
        "incident_id": incident.incident_id,
        "severity": incident.severity,
        "status": incident.status,
        "deployment_id": incident.deployment_id,
        "signal_source": incident.signal_source,
        "current_stage": incident.current_stage,
        "primary_signals": incident.primary_signal_names,
        "hypothesis": {
            "incident_type": str(hypothesis.incident_type).split(".")[-1],
            "root_cause": hypothesis.root_cause,
            "confidence": hypothesis.confidence,
            "affected_node_ids": hypothesis.affected_node_ids,
        },
        "requires_manual_review": incident.requires_manual_review,
    };
}

walker triage_walker {
    has incident_id: str;
    has signal_names: list[str] = [];
    has graph_context: list[str] = [];
    has hypothesis: IncidentHypothesis = None;

    can start with Root entry {
        visit [-->(?:Incident)];
    }

    can inspect_incident with Incident entry {
        if here.incident_id == self.incident_id {
            self.graph_context.append("incident:" + here.incident_id + ":" + here.severity);
            visit [-->];
        }
    }

    can inspect_alert with Alert entry {
        self.signal_names.append(here.alert_type);
        self.graph_context.append("alert:" + here.alert_id + ":" + here.alert_type);
    }

    can inspect_metric with Metric entry {
        self.graph_context.append("metric:" + here.metric_name + ":" + str(here.metric_value));
    }

    can inspect_deployment with Deployment entry {
        self.graph_context.append("deployment:" + here.deployment_id + ":" + here.status);
        visit [-->];
    }

    can inspect_route with Route entry {
        self.graph_context.append("route:" + here.route_id + ":" + str(here.canary_pct));
    }

    can inspect_config with Config entry {
        self.graph_context.append("config:" + here.config_id + ":" + str(here.batch_size));
    }

    can inspect_policy with Policy entry {
        self.graph_context.append("policy:" + here.policy_id + ":" + str(here.confidence_threshold));
    }

    can finalize with Incident exit {
        if here.incident_id == self.incident_id {
            try {
                self.hypothesis = classify_incident(
                    self.signal_names,
                    "\n".join(self.graph_context),
                );
            } except Exception as e {
                self.hypothesis = fallback_incident_hypothesis(
                    parse_prometheus_metrics(here.latest_metrics_payload),
                    self.signal_names,
                );
            }
            here.current_stage = "triage_complete";
            here.primary_signal_names = self.signal_names;
            here.hypothesis_type = str(self.hypothesis.incident_type).split(".")[-1];
            here.hypothesis_summary = self.hypothesis.root_cause;
            here.hypothesis_confidence = self.hypothesis.confidence;
            here.requires_manual_review = self.hypothesis.incident_type == IncidentType.UNKNOWN;
            report build_incident_view(here, self.hypothesis);
        }
    }
}

walker plan_walker {}
walker execute_walker {}
walker verify_walker {}
walker rollback_walker {}
walker audit_walker {}

def runtime_contract_metadata() -> dict {
    return {
        "phase": "phase_1_baseline",
        "strategy_id": "S1",
        "pattern_id": "P1",
        "runtime": "jac",
        "entrypoint": "main.jac",
        "frontend_codespace": "cl app",
        "signal_source": "mock_vllm.py",
        "published_endpoints": [
            "bootstrap_status",
            "trigger_incident",
            "get_incident_state",
        ],
        "active_slice": "SLICE-OPS-01",
        "foundation_contracts": [
            "FT-OPS-INFRA-01",
            "FT-OPS-TEST-01",
        ],
    };
}

def:pub bootstrap_status() -> dict {
    return {
        **runtime_contract_metadata(),
        "walkers": [
            "triage_walker",
            "plan_walker",
            "execute_walker",
            "verify_walker",
            "rollback_walker",
            "audit_walker",
        ],
        "status": "phase_1_ready",
    };
}

def persist_phase_1_incident(incident_id: str, severity: str, deployment_id: str, signal_source: str, metrics_payload: str) -> Incident {
    metrics = parse_prometheus_metrics(metrics_payload);
    incident = (root ++> Incident(
        incident_id=incident_id,
        severity=severity,
        deployment_id=deployment_id,
        signal_source=signal_source,
        current_stage="signal_ingested",
        latest_metrics_payload=metrics_payload,
        created_at="2026-02-28T00:00:00Z",
    ))[0];
    incident ++> Alert(
        alert_id="alert:p95_latency_high",
        alert_type="p95_latency_high",
        threshold=1.0,
        observed_value=metrics.get("vllm:e2e_request_latency_seconds", 0.0),
        fired_at="2026-02-28T00:00:00Z",
    );
    for metric_node in metric_nodes_from_snapshot(metrics) {
        incident ++> metric_node;
    }
    deployment = (incident ++> Deployment(
        deployment_id=deployment_id,
        name="canary",
        role="canary",
        status="degraded",
        traffic_pct=10,
    ))[0];
    deployment ++> Route(
        route_id="route:prod_split",
        baseline_pct=90,
        canary_pct=10,
    );
    deployment ++> Config(
        config_id="config:deployment_canary",
        max_model_len=8192,
        batch_size=128,
        dtype="bfloat16",
    );
    incident ++> Policy(
        policy_id="policy:phase_1_read_only",
        action_allowlist=[],
        confidence_threshold=0.80,
        approval_required=True,
    );
    return incident;
}

def:pub trigger_incident(
    incident_id: str = "inc_bootstrap",
    severity: str = "high",
    deployment_id: str = "deployment:canary",
    signal_source: str = "mock_vllm",
) -> dict {
    metrics_payload = phase_1_metrics_payload();
    incident = persist_phase_1_incident(
        incident_id=incident_id,
        severity=severity,
        deployment_id=deployment_id,
        signal_source=signal_source,
        metrics_payload=metrics_payload,
    );
    triage_result = root spawn triage_walker(incident_id=incident_id);
    return {
        "status": "pipeline_started",
        "phase": "phase_1_baseline",
        "current_stage": incident.current_stage,
        "incident_id": incident_id,
        "signal_source": signal_source,
        "poll_url": "/walker/get_incident_state/" + incident_id,
        "primary_signals": incident.primary_signal_names,
        "hypothesis": triage_result[0] if triage_result else {
            "incident_type": incident.hypothesis_type,
            "root_cause": incident.hypothesis_summary,
            "confidence": incident.hypothesis_confidence,
            "affected_node_ids": [],
        },
    };
}

def:pub get_incident_state(incident_id: str) -> dict {
    incidents = [node for node in [root-->](?:Incident) if node.incident_id == incident_id];
    if not incidents {
        return {
            "incident_id": incident_id,
            "phase": "phase_1_baseline",
            "current_stage": "not_found",
            "error": "INCIDENT_NOT_FOUND",
            "message": "No incident state exists for the requested incident id.",
        };
    }
    incident = incidents[0];
    return {
        "incident_id": incident.incident_id,
        "severity": incident.severity,
        "status": incident.status,
        "phase": "phase_1_baseline",
        "current_stage": incident.current_stage,
        "deployment_id": incident.deployment_id,
        "signal_source": incident.signal_source,
        "primary_signals": incident.primary_signal_names,
        "hypothesis": {
            "incident_type": incident.hypothesis_type,
            "root_cause": incident.hypothesis_summary,
            "confidence": incident.hypothesis_confidence,
            "affected_node_ids": [
                "deployment:canary",
                "route:prod_split",
                "alert:p95_latency_high",
            ],
        },
        "requires_manual_review": incident.requires_manual_review,
    };
}

cl def:pub app() -> JsxElement {
    has incident: dict = {};

    async can with entry {
        seed = await trigger_incident();
        incident = await get_incident_state(seed["incident_id"]);
    }

    return (
        <div>
            <h1>Ops Graph</h1>
            <p>Walker-native inference incident response Phase 1 baseline.</p>
            <section>
                <h2>Incident Feed</h2>
                <p>Incident: {incident["incident_id"] if incident else "loading"}</p>
                <p>Severity: {incident["severity"] if incident else "loading"}</p>
                <p>Primary signals: {", ".join(incident["primary_signals"]) if incident and incident["primary_signals"] else "loading"}</p>
            </section>
            <section>
                <h2>Graph View</h2>
                <p>Deployment: {incident["deployment_id"] if incident else "loading"}</p>
                <p>Typed Incident, Alert, Metric, Deployment, Route, Config, and Policy nodes back the Phase 1 flow.</p>
            </section>
            <section>
                <h2>Typed Decisions</h2>
                <p>Incident type: {incident["hypothesis"]["incident_type"] if incident else "loading"}</p>
                <p>Root cause: {incident["hypothesis"]["root_cause"] if incident else "loading"}</p>
                <p>`triage_walker` produces a bounded incident hypothesis and fail-closed manual review status when unsupported.</p>
            </section>
            <section>
                <h2>Audit Log + MTTR</h2>
                <p>Current stage: {incident["current_stage"] if incident else "loading"}</p>
                <p>Later-slice lifecycle visibility remains intentionally out of scope.</p>
            </section>
        </div>
    );
}
