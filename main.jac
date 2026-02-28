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

obj PolicyDecision {
    has status: str;
    has reason: str;
    has confidence: float;
    has requires_approval: bool;
}

obj ActionResult {
    has action_type: str;
    has target: str;
    has status: str;
    has message: str;
}

obj VerificationResult {
    has passed: bool;
    has observed_value: float;
    has expected_direction: str;
    has metric: str;
}

obj RollbackResult {
    has triggered: bool;
    has status: str;
    has restored_targets: list[str];
    has action_types: list[str];
    has message: str;
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

def summarize_audit_step(step: str, typed_data: dict) -> str
    by llm();
sem summarize_audit_step = "Write a short plain-language explanation of an incident response timeline step for non-expert judges.";

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

def hypothesis_payload(hypothesis: IncidentHypothesis) -> dict {
    if hypothesis == None {
        return {
            "incident_type": "UNKNOWN",
            "root_cause": "",
            "confidence": 0.0,
            "affected_node_ids": [],
        };
    }
    return {
        "incident_type": str(hypothesis.incident_type).split(".")[-1],
        "root_cause": hypothesis.root_cause,
        "confidence": hypothesis.confidence,
        "affected_node_ids": hypothesis.affected_node_ids,
    };
}

def plan_payload(plan: RemediationPlan) -> dict {
    if plan == None {
        return {
            "plan_id": "",
            "actions": [],
            "verification": {},
            "rollback_on_fail": False,
        };
    }
    return {
        "plan_id": plan.plan_id,
        "actions": plan.actions,
        "verification": {
            "metric": plan.verification_metric,
            "expected_direction": plan.expected_direction,
        },
        "rollback_on_fail": plan.rollback_on_fail,
    };
}

def policy_payload(policy: PolicyDecision) -> dict {
    if policy == None {
        return {
            "status": "NOT_EVALUATED",
            "reason": "",
            "confidence": 0.0,
            "requires_approval": False,
        };
    }
    return {
        "status": policy.status,
        "reason": policy.reason,
        "confidence": policy.confidence,
        "requires_approval": policy.requires_approval,
    };
}

def action_results_payload(action_results: list[ActionResult]) -> list[dict] {
    payload = [];
    for result in action_results {
        payload.append(
            {
                "action_type": result.action_type,
                "target": result.target,
                "status": result.status,
                "message": result.message,
            }
        );
    }
    return payload;
}

def verification_payload(verification: VerificationResult) -> dict {
    if verification == None {
        return {
            "passed": False,
            "observed_value": 0.0,
            "expected_direction": "",
            "metric": "",
            "status": "not_run",
        };
    }
    return {
        "passed": verification.passed,
        "observed_value": verification.observed_value,
        "expected_direction": verification.expected_direction,
        "metric": verification.metric,
        "status": "passed" if verification.passed else "failed",
    };
}

def rollback_payload(rollback: RollbackResult) -> dict {
    if rollback == None {
        return {
            "triggered": False,
            "status": "not_run",
            "restored_targets": [],
            "action_types": [],
            "message": "",
        };
    }
    return {
        "triggered": rollback.triggered,
        "status": rollback.status,
        "restored_targets": rollback.restored_targets,
        "action_types": rollback.action_types,
        "message": rollback.message,
    };
}

def audit_payload(entries: list[AuditEntry]) -> list[dict] {
    payload = [];
    for entry in entries {
        payload.append(
            {
                "step": entry.step,
                "typed_data": entry.typed_data,
                "plain_summary": entry.plain_summary,
            }
        );
    }
    return payload;
}

def verification_threshold(metric: str) -> float {
    if metric == "vllm:e2e_request_latency_seconds" {
        return 0.80;
    }
    return 1.0;
}

def post_action_metrics_payload(execute_status: str, force_failure: bool = False) -> str {
    if force_failure or execute_status != "executed" {
        return phase_1_metrics_payload("rollout_regression");
    }
    return phase_1_metrics_payload("healthy");
}

def build_verification_result(
    plan: RemediationPlan,
    execute_status: str,
    force_failure: bool = False,
) -> VerificationResult {
    payload = post_action_metrics_payload(execute_status, force_failure=force_failure);
    metrics = parse_prometheus_metrics(payload);
    observed = metrics.get(plan.verification_metric, 0.0);
    threshold = verification_threshold(plan.verification_metric);
    passed = observed <= threshold;
    if plan.expected_direction != "down" {
        passed = observed >= threshold;
    }
    return VerificationResult(
        passed=passed,
        observed_value=observed,
        expected_direction=plan.expected_direction,
        metric=plan.verification_metric,
    );
}

def build_rollback_result(action_results: list[ActionResult], verification: VerificationResult) -> RollbackResult {
    if verification == None or verification.passed {
        return RollbackResult(
            triggered=False,
            status="not_needed",
            restored_targets=[],
            action_types=[],
            message="verification_passed",
        );
    }
    restored_targets = [];
    rollback_actions = [];
    for result in action_results {
        if result.target not in restored_targets {
            restored_targets.append(result.target);
        }
        if result.action_type == "set_deployment_status" {
            rollback_actions.append("rollback_config");
        } else {
            if result.action_type == "shift_traffic" {
                rollback_actions.append("shift_traffic");
            }
        }
    }
    if "rollback_config" not in rollback_actions {
        rollback_actions.append("rollback_config");
    }
    return RollbackResult(
        triggered=True,
        status="rolled_back",
        restored_targets=restored_targets,
        action_types=rollback_actions,
        message="known_good_path_restored",
    );
}

def rollback_state_updates() -> dict {
    return {
        "deployment": {
            "deployment_id": "deployment:canary",
            "status": "rolled_back",
            "role": "canary",
        },
        "route": {
            "route_id": "route:prod_split",
            "baseline_pct": 100,
            "canary_pct": 0,
        },
    };
}

def build_mttr_metrics(verification: VerificationResult, rollback: RollbackResult) -> dict {
    diagnosis_seconds = 35;
    safe_action_seconds = 80;
    recovery_seconds = 110;
    resolved_state = "verified_recovery";
    if verification != None and not verification.passed {
        recovery_seconds = 165;
        resolved_state = "rollback_recovery";
    }
    if rollback != None and rollback.status not in ["rolled_back", "not_needed"] {
        recovery_seconds = 300;
        resolved_state = "manual_followup_required";
    }
    manual_baseline_seconds = 1800;
    return {
        "time_to_diagnosis_seconds": diagnosis_seconds,
        "time_to_safe_action_seconds": safe_action_seconds,
        "time_to_recovery_seconds": recovery_seconds,
        "manual_baseline_seconds": manual_baseline_seconds,
        "seconds_saved_vs_manual": manual_baseline_seconds - recovery_seconds,
        "resolution_mode": resolved_state,
    };
}

def build_audit_entries(incident: Incident, execution_state: dict) -> list[AuditEntry] {
    entries = [];
    hypothesis = execution_state.get("hypothesis", hypothesis_from_incident(incident));
    plan = execution_state.get("plan", None);
    policy = execution_state.get("policy_decision", None);
    action_results = execution_state.get("action_results", []);
    verification = execution_state.get("verification", None);
    rollback = execution_state.get("rollback", None);

    triage_summary = "Triage identified " + hypothesis_payload(hypothesis)["incident_type"] + " with bounded confidence.";
    try {
        triage_summary = summarize_audit_step("triage", hypothesis_payload(hypothesis));
    } except Exception as e {}
    entries.append(
        AuditEntry(
            step="triage",
            typed_data=hypothesis_payload(hypothesis),
            plain_summary=triage_summary,
        )
    );
    plan_summary = "Plan prepared with " + str(len(plan.actions) if plan != None else 0) + " allowlisted actions.";
    try {
        plan_summary = summarize_audit_step("plan", plan_payload(plan));
    } except Exception as e {}
    entries.append(
        AuditEntry(
            step="plan",
            typed_data=plan_payload(plan),
            plain_summary=plan_summary,
        )
    );
    policy_summary = "Policy decision returned " + policy_payload(policy)["status"] + ".";
    try {
        policy_summary = summarize_audit_step("policy_check", policy_payload(policy));
    } except Exception as e {}
    entries.append(
        AuditEntry(
            step="policy_check",
            typed_data=policy_payload(policy),
            plain_summary=policy_summary,
        )
    );
    execute_summary = "Execution completed with status " + execution_state.get("execute_status", "not_started") + ".";
    try {
        execute_summary = summarize_audit_step(
            "execute",
            {
                "execute_status": execution_state.get("execute_status", "not_started"),
                "action_results": action_results_payload(action_results),
            },
        );
    } except Exception as e {}
    entries.append(
        AuditEntry(
            step="execute",
            typed_data={
                "execute_status": execution_state.get("execute_status", "not_started"),
                "action_results": action_results_payload(action_results),
            },
            plain_summary=execute_summary,
        )
    );
    verify_summary = "Verification " + ("passed" if verification != None and verification.passed else "failed") + " against post-action metrics.";
    try {
        verify_summary = summarize_audit_step("verify", verification_payload(verification));
    } except Exception as e {}
    entries.append(
        AuditEntry(
            step="verify",
            typed_data=verification_payload(verification),
            plain_summary=verify_summary,
        )
    );
    if rollback != None and rollback.triggered {
        rollback_summary = "Rollback restored the known-good route after failed verification.";
        try {
            rollback_summary = summarize_audit_step("rollback", rollback_payload(rollback));
        } except Exception as e {}
        entries.append(
            AuditEntry(
                step="rollback",
                typed_data=rollback_payload(rollback),
                plain_summary=rollback_summary,
            )
        );
    }
    audit_summary = "Audit timeline preserved the full incident workflow for operator review.";
    try {
        audit_summary = summarize_audit_step(
            "audit",
            {
                "entry_count": len(entries) + 1,
                "resolved_status": incident.status,
            },
        );
    } except Exception as e {}
    entries.append(
        AuditEntry(
            step="audit",
            typed_data={
                "entry_count": len(entries) + 1,
                "resolved_status": incident.status,
            },
            plain_summary=audit_summary,
        )
    );
    return entries;
}

def lifecycle_state_payload(incident: Incident, execution_state: dict) -> dict {
    hypothesis = execution_state.get("hypothesis", hypothesis_from_incident(incident));
    return {
        "incident_id": incident.incident_id,
        "severity": incident.severity,
        "status": incident.status,
        "phase": "phase_2_target_product",
        "current_stage": execution_state.get("current_stage", incident.current_stage),
        "deployment_id": incident.deployment_id,
        "signal_source": incident.signal_source,
        "primary_signals": incident.primary_signal_names,
        "hypothesis": hypothesis_payload(hypothesis),
        "plan": plan_payload(execution_state.get("plan", None)),
        "policy_decision": policy_payload(execution_state.get("policy_decision", None)),
        "action_results": action_results_payload(execution_state.get("action_results", [])),
        "state_updates": execution_state.get("state_updates", {}),
        "verification": verification_payload(execution_state.get("verification", None)),
        "rollback": rollback_payload(execution_state.get("rollback", None)),
        "audit": audit_payload(execution_state.get("audit", [])),
        "mttr": execution_state.get("mttr", build_mttr_metrics(None, None)),
        "requires_manual_review": incident.requires_manual_review,
    };
}

def incident_type_from_string(raw_type: str) -> IncidentType {
    if raw_type == "ROLLOUT_REGRESSION" {
        return IncidentType.ROLLOUT_REGRESSION;
    }
    if raw_type == "CONFIG_PRESSURE" {
        return IncidentType.CONFIG_PRESSURE;
    }
    if raw_type == "CAPACITY_SATURATION" {
        return IncidentType.CAPACITY_SATURATION;
    }
    return IncidentType.UNKNOWN;
}

def hypothesis_from_incident(incident: Incident) -> IncidentHypothesis {
    return IncidentHypothesis(
        incident_type=incident_type_from_string(incident.hypothesis_type),
        root_cause=incident.hypothesis_summary,
        confidence=incident.hypothesis_confidence,
        affected_node_ids=[
            incident.deployment_id,
            "route:prod_split",
            "alert:p95_latency_high",
        ],
    );
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

walker verify_walker {
    has incident_id: str;
    has force_failure: bool = False;
    has verification: VerificationResult = None;

    can start with Root entry {
        visit [-->(?:Incident)];
    }

    can verify_incident with Incident entry {
        if here.incident_id == self.incident_id and self.incident_id in INCIDENT_EXECUTION_STATE {
            execution_state = INCIDENT_EXECUTION_STATE[self.incident_id];
            plan = execution_state.get("plan", None);
            if plan != None {
                self.verification = build_verification_result(
                    plan,
                    execution_state.get("execute_status", "not_started"),
                    force_failure=self.force_failure,
                );
                execution_state["verification"] = self.verification;
                execution_state["current_stage"] = "verify_walker";
                here.current_stage = "verify_walker";
                if self.verification.passed {
                    here.status = "resolved";
                    here.current_stage = "verify_complete";
                    here.resolved_at = "2026-02-28T00:01:50Z";
                } else {
                    here.status = "rollback_pending";
                    here.current_stage = "verify_failed";
                }
                report verification_payload(self.verification);
            }
        }
    }
}

walker rollback_walker {
    has incident_id: str;
    has rollback: RollbackResult = None;

    can start with Root entry {
        visit [-->(?:Incident)];
    }

    can rollback_incident with Incident entry {
        if here.incident_id == self.incident_id and self.incident_id in INCIDENT_EXECUTION_STATE {
            execution_state = INCIDENT_EXECUTION_STATE[self.incident_id];
            self.rollback = build_rollback_result(
                execution_state.get("action_results", []),
                execution_state.get("verification", None),
            );
            execution_state["rollback"] = self.rollback;
            execution_state["current_stage"] = "rollback_walker";
            here.current_stage = "rollback_walker";
            if self.rollback.triggered {
                execution_state["state_updates"] = {
                    **execution_state.get("state_updates", {}),
                    "rollback": rollback_state_updates(),
                };
                here.status = "resolved";
                here.current_stage = "rollback_complete";
                here.resolved_at = "2026-02-28T00:02:45Z";
            }
            report rollback_payload(self.rollback);
        }
    }
}

walker audit_walker {
    has incident_id: str;
    has entries: list[AuditEntry] = [];

    can start with Root entry {
        visit [-->(?:Incident)];
    }

    can finalize_audit with Incident entry {
        if here.incident_id == self.incident_id and self.incident_id in INCIDENT_EXECUTION_STATE {
            execution_state = INCIDENT_EXECUTION_STATE[self.incident_id];
            self.entries = build_audit_entries(here, execution_state);
            execution_state["audit"] = self.entries;
            execution_state["mttr"] = build_mttr_metrics(
                execution_state.get("verification", None),
                execution_state.get("rollback", None),
            );
            execution_state["current_stage"] = "resolved";
            here.current_stage = "resolved";
            if here.resolved_at == None {
                here.resolved_at = "2026-02-28T00:01:50Z";
                here.status = "resolved";
            }
            report audit_payload(self.entries);
        }
    }
}

glob POLICY_ALLOWLIST: list[str] = ["shift_traffic", "set_deployment_status", "rollback_config"];
glob INCIDENT_EXECUTION_STATE: dict = {};

def build_mock_hypothesis(incident_id: str) -> IncidentHypothesis {
    return IncidentHypothesis(
        incident_type=IncidentType.ROLLOUT_REGRESSION,
        root_cause="canary deployment introduced latency regression under current load",
        confidence=0.92,
        affected_node_ids=[
            "incident:" + incident_id,
            "deployment:canary",
            "route:prod_split",
            "policy:default",
        ],
    );
}

def build_plan_from_hypothesis(hypothesis: IncidentHypothesis, incident_id: str) -> RemediationPlan {
    if hypothesis.incident_type == IncidentType.UNKNOWN {
        return RemediationPlan(
            plan_id="plan_" + incident_id,
            actions=[],
            verification_metric="vllm:e2e_request_latency_seconds",
            expected_direction="down",
            rollback_on_fail=True,
        );
    }
    return RemediationPlan(
        plan_id="plan_" + incident_id,
        actions=[
            {
                "step": 1,
                "type": "shift_traffic",
                "target": "route:prod_split",
                "params": {"canary_percentage": 0},
            },
            {
                "step": 2,
                "type": "set_deployment_status",
                "target": "deployment:canary",
                "params": {"status": "isolated"},
            },
        ],
        verification_metric="vllm:e2e_request_latency_seconds",
        expected_direction="down",
        rollback_on_fail=True,
    );
}

def evaluate_policy(
    plan: RemediationPlan,
    confidence: float,
    require_approval: bool,
    approval_token: str,
) -> PolicyDecision {
    if confidence < 0.80 {
        return PolicyDecision(
            status="POLICY_BLOCKED",
            reason="LOW_CONFIDENCE",
            confidence=confidence,
            requires_approval=False,
        );
    }
    for action in plan.actions {
        if action["type"] not in POLICY_ALLOWLIST {
            return PolicyDecision(
                status="POLICY_BLOCKED",
                reason="ACTION_NOT_ALLOWLISTED",
                confidence=confidence,
                requires_approval=False,
            );
        }
    }
    if require_approval and approval_token == "" {
        return PolicyDecision(
            status="APPROVAL_REQUIRED",
            reason="MANUAL_APPROVAL_REQUIRED",
            confidence=confidence,
            requires_approval=True,
        );
    }
    return PolicyDecision(
        status="PASS",
        reason="POLICY_PASSED",
        confidence=confidence,
        requires_approval=require_approval,
    );
}

def run_allowlisted_actions(plan: RemediationPlan, force_fail: bool = False) -> list[ActionResult] {
    results = [];
    for action in plan.actions {
        if force_fail and action["type"] == "set_deployment_status" {
            results.append(
                ActionResult(
                    action_type=action["type"],
                    target=action["target"],
                    status="failed",
                    message="mock_execution_failure",
                )
            );
        } else {
            results.append(
                ActionResult(
                    action_type=action["type"],
                    target=action["target"],
                    status="succeeded",
                    message="executed",
                )
            );
        }
    }
    return results;
}

def project_graph_updates(action_results: list[ActionResult]) -> dict {
    deployment_status = "active";
    canary_pct = 100;
    baseline_pct = 0;
    for result in action_results {
        if result.status != "succeeded" {
            continue;
        }
        if result.action_type == "shift_traffic" {
            canary_pct = 0;
            baseline_pct = 100;
        }
        if result.action_type == "set_deployment_status" {
            deployment_status = "isolated";
        }
    }
    return {
        "deployment": {
            "deployment_id": "deployment:canary",
            "status": deployment_status,
            "role": "canary",
        },
        "route": {
            "route_id": "route:prod_split",
            "baseline_pct": baseline_pct,
            "canary_pct": canary_pct,
        },
    };
}

def runtime_contract_metadata() -> dict {
    return {
        "phase": "phase_2_target_product",
        "strategy_id": "S1",
        "pattern_id": "P1",
        "runtime": "jac",
        "entrypoint": "main.jac",
        "frontend_codespace": "cl app",
        "signal_source": "mock_vllm.py",
        "published_endpoints": [
            "bootstrap_status",
            "trigger_incident",
            "execute_incident",
            "get_incident_state",
        ],
        "active_slice": "SLICE-OPS-03",
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
        "status": "phase_2_ready",
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
    INCIDENT_EXECUTION_STATE[incident_id] = {
        "incident_id": incident_id,
        "current_stage": "triage_complete",
        "execute_status": "not_started",
    };
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

def:pub execute_incident(
    incident_id: str,
    approval_token: str = "",
    force_fail: bool = False,
    confidence: float = 0.92,
    require_approval: bool = False,
    force_verification_failure: bool = False,
) -> dict {
    incidents = [node for node in [root-->](?:Incident) if node.incident_id == incident_id];
    if incident_id == "" {
        return {
            "incident_id": incident_id,
            "current_stage": "input_validation",
            "execute_status": "invalid_input",
            "error": "INCIDENT_ID_REQUIRED",
        };
    }
    if require_approval and approval_token != "" and approval_token[0:4] != "apr_" {
        return {
            "incident_id": incident_id,
            "current_stage": "input_validation",
            "execute_status": "invalid_input",
            "error": "INVALID_APPROVAL_TOKEN",
        };
    }
    if confidence < 0.0 or confidence > 1.0 {
        return {
            "incident_id": incident_id,
            "current_stage": "input_validation",
            "execute_status": "invalid_input",
            "error": "INVALID_CONFIDENCE_RANGE",
        };
    }
    if not incidents {
        return {
            "incident_id": incident_id,
            "current_stage": "input_validation",
            "execute_status": "invalid_input",
            "error": "INCIDENT_NOT_FOUND",
        };
    }

    incident = incidents[0];
    hypothesis = hypothesis_from_incident(incident);
    plan = build_plan_from_hypothesis(hypothesis, incident_id);
    policy = evaluate_policy(plan, confidence, require_approval, approval_token);

    if policy.status != "PASS" {
        INCIDENT_EXECUTION_STATE[incident_id] = {
            "incident_id": incident_id,
            "current_stage": "policy_check",
            "execute_status": "blocked" if policy.status == "POLICY_BLOCKED" else "approval_required",
            "hypothesis": hypothesis,
            "plan": plan,
            "policy_decision": policy,
            "action_results": [],
            "state_updates": {},
        };
        return INCIDENT_EXECUTION_STATE[incident_id];
    }

    action_results = run_allowlisted_actions(plan, force_fail=force_fail);
    state_updates = project_graph_updates(action_results);
    execute_status = "executed";
    for result in action_results {
        if result.status != "succeeded" {
            execute_status = "partial_execution";
        }
    }

    INCIDENT_EXECUTION_STATE[incident_id] = {
        "incident_id": incident_id,
        "current_stage": "execute_walker",
        "execute_status": execute_status,
        "hypothesis": hypothesis,
        "plan": plan,
        "policy_decision": policy,
        "action_results": action_results,
        "state_updates": state_updates,
    };
    root spawn verify_walker(
        incident_id=incident_id,
        force_failure=force_verification_failure,
    );
    root spawn rollback_walker(
        incident_id=incident_id,
    );
    root spawn audit_walker(
        incident_id=incident_id,
    );
    return get_incident_state(incident_id);
}

def:pub get_incident_state(incident_id: str) -> dict {
    incidents = [node for node in [root-->](?:Incident) if node.incident_id == incident_id];
    if incident_id in INCIDENT_EXECUTION_STATE and incidents {
        execution_state = INCIDENT_EXECUTION_STATE[incident_id];
        if execution_state.get("execute_status", "not_started") != "not_started" {
            return lifecycle_state_payload(incidents[0], execution_state);
        }
    }

    if not incidents {
        if incident_id in INCIDENT_EXECUTION_STATE {
            return INCIDENT_EXECUTION_STATE[incident_id];
        }
        return {
            "incident_id": incident_id,
            "phase": "phase_2_target_product",
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
        "phase": "phase_2_target_product",
        "current_stage": incident.current_stage,
        "deployment_id": incident.deployment_id,
        "signal_source": incident.signal_source,
        "primary_signals": incident.primary_signal_names,
        "hypothesis": hypothesis_payload(hypothesis_from_incident(incident)),
        "plan": plan_payload(None),
        "policy_decision": policy_payload(None),
        "action_results": [],
        "state_updates": {},
        "verification": verification_payload(None),
        "rollback": rollback_payload(None),
        "audit": [],
        "mttr": build_mttr_metrics(None, None),
        "requires_manual_review": incident.requires_manual_review,
    };
}

cl import from react { useEffect }

cl def:pub app() -> JsxElement {
    has incident_id: str = "";
    has incident: dict = {};

    async def refresh_incident() -> None {
        if incident_id != "" {
            incident = await get_incident_state(incident_id);
        }
    }

    async can with entry {
        seed = await trigger_incident();
        incident_id = seed["incident_id"];
        incident = await execute_incident(seed["incident_id"]);
    }

    useEffect(lambda -> None {
        if incident_id == "" {
            return lambda -> None {};
        }
        interval = setInterval(lambda -> None { refresh_incident(); }, 1000);
        return lambda -> None { clearInterval(interval); };
    }, [incident_id]);

    return (
        <div>
            <h1>Ops Graph</h1>
            <p>Walker-native inference incident response with verification, rollback, audit, and MTTR visibility.</p>
            <section>
                <h2>Incident Feed</h2>
                <p>Incident: {incident["incident_id"] if incident else "loading"}</p>
                <p>Severity: {incident["severity"] if incident else "loading"}</p>
                <p>Primary signals: {", ".join(incident["primary_signals"]) if incident and incident["primary_signals"] else "loading"}</p>
            </section>
            <section>
                <h2>Graph View</h2>
                <p>Deployment: {incident["deployment_id"] if incident else "loading"}</p>
                <p>Current stage: {incident["current_stage"] if incident else "loading"}</p>
                <p>Typed Incident, Alert, Metric, Deployment, Route, Config, and Policy nodes back the walker pipeline.</p>
            </section>
            <section>
                <h2>Typed Decisions</h2>
                <p>Incident type: {incident["hypothesis"]["incident_type"] if incident else "loading"}</p>
                <p>Root cause: {incident["hypothesis"]["root_cause"] if incident else "loading"}</p>
                <p>Verification: {incident["verification"]["status"] if incident else "loading"}</p>
                <p>`triage_walker`, policy evaluation, and lifecycle closeout remain visible as typed state.</p>
            </section>
            <section>
                <h2>Audit Log + MTTR</h2>
                <p>Audit entries: {str(len(incident["audit"])) if incident else "loading"}</p>
                <p>Recovery seconds: {str(incident["mttr"]["time_to_recovery_seconds"]) if incident else "loading"}</p>
                <p>Manual baseline: {str(incident["mttr"]["manual_baseline_seconds"]) if incident else "loading"}</p>
            </section>
        </div>
    );
}
