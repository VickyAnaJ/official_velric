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
    return {
        "status": "pipeline_bootstrap_ready",
        "incident_id": incident_id,
        "poll_url": "/walker/incident_state/" + incident_id,
    };
}

def:pub get_incident_state(incident_id: str) -> dict {
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
