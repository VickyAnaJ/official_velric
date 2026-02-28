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

obj AuditEntry {
    has step: str;
    has typed_data: dict;
    has plain_summary: str;
}

node Incident {
    has incident_id: str;
    has severity: str;
    has status: str = "active";
    has created_at: str;
    has resolved_at: str | None = None;
}

node Alert {
    has alert_id: str;
    has alert_type: str;
    has observed_value: float;
}

node Deployment {
    has deployment_id: str;
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

walker triage_walker {}
walker plan_walker {}
walker execute_walker {}
walker verify_walker {}
walker rollback_walker {}
walker audit_walker {}

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
    has results: list[ActionResult] = [];
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
    has deployment_status: str = "active";
    has canary_pct: int = 100;
    has baseline_pct: int = 0;
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

def:pub bootstrap_status() -> dict {
    return {
        "runtime": "jac",
        "entrypoint": "main.jac",
        "frontend": "cl app",
        "signal_source": "mock_vllm.py",
        "walkers": [
            "triage_walker",
            "plan_walker",
            "execute_walker",
            "verify_walker",
            "rollback_walker",
            "audit_walker",
        ],
    };
}

def:pub trigger_incident(incident_id: str = "inc_bootstrap") -> dict {
    INCIDENT_EXECUTION_STATE[incident_id] = {
        "incident_id": incident_id,
        "current_stage": "triage_walker",
        "execute_status": "not_started",
    };
    return {
        "status": "pipeline_bootstrap_ready",
        "incident_id": incident_id,
        "poll_url": "/walker/incident_state/" + incident_id,
    };
}

def:pub execute_incident(
    incident_id: str,
    approval_token: str = "",
    force_fail: bool = False,
    confidence: float = 0.92,
    require_approval: bool = False,
) -> dict {
    has hypothesis = build_mock_hypothesis(incident_id);
    has plan = build_plan_from_hypothesis(hypothesis, incident_id);
    has policy = evaluate_policy(plan, confidence, require_approval, approval_token);

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

    has action_results = run_allowlisted_actions(plan, force_fail=force_fail);
    has state_updates = project_graph_updates(action_results);
    has execute_status: str = "executed";
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
    return INCIDENT_EXECUTION_STATE[incident_id];
}

def:pub get_incident_state(incident_id: str) -> dict {
    if incident_id in INCIDENT_EXECUTION_STATE {
        return INCIDENT_EXECUTION_STATE[incident_id];
    }
    return {
        "incident_id": incident_id,
        "current_stage": "bootstrap",
        "message": "Jac runtime scaffolded; slice implementation starts after bootstrap verification.",
    };
}

cl def:pub app() -> JsxElement {
    return (
        <div>
            <h1>Ops Graph</h1>
            <p>Walker-native inference incident response bootstrap.</p>
            <section>
                <h2>Incident Feed</h2>
                <p>Pending Step 3.1 capability activation.</p>
            </section>
            <section>
                <h2>Graph View</h2>
                <p>Jac node graph will render here after slice implementation.</p>
            </section>
            <section>
                <h2>Typed Decisions</h2>
                <p>Triage, plan, execute, verify, rollback, and audit outputs surface here.</p>
            </section>
            <section>
                <h2>Audit Log + MTTR</h2>
                <p>Append-only audit entries and MTTR metrics appear here.</p>
            </section>
        </div>
    );
}
