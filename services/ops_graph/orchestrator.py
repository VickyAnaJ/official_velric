from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from .executor import ActionAdapter, LocalActionAdapter, execute_bounded_actions
from .graph import InMemoryGraphStore, incident_to_response
from .mock_metrics import parse_metrics_payload
from .planner import UnsupportedIncidentTypeError, build_remediation_plan
from .policy import PolicyConfig, default_policy_config, evaluate_policy
from .triage import classify_incident


class MetricsSourceError(RuntimeError):
    """Raised when the metrics source cannot be read safely."""


@dataclass
class OrchestratorResult:
    status_code: int
    payload: dict[str, object]


class IncidentOrchestrator:
    def __init__(
        self,
        store: InMemoryGraphStore,
        metrics_source: "MetricsSource",
        policy_config: PolicyConfig | None = None,
        action_adapter: ActionAdapter | None = None,
    ) -> None:
        self._store = store
        self._metrics_source = metrics_source
        self._policy_config = policy_config if policy_config is not None else default_policy_config()
        self._action_adapter = action_adapter if action_adapter is not None else LocalActionAdapter()

    def trigger_incident(self, incident_key: str | None) -> OrchestratorResult:
        if incident_key and self._store.has_incident_key(incident_key):
            existing_id = self._store.get_incident_id_by_key(incident_key)
            existing = self._store.get_incident(existing_id)
            assert existing is not None
            data = incident_to_response(existing)
            data["idempotent"] = True
            return OrchestratorResult(status_code=200, payload=data)

        try:
            metrics_payload = self._metrics_source.get_payload()
        except Exception as exc:  # pragma: no cover - tested via integration boundary
            raise MetricsSourceError("Unable to read metrics source") from exc

        metrics = parse_metrics_payload(metrics_payload)
        hypothesis = classify_incident(metrics)
        incident_id = str(uuid4())
        record = self._store.save_incident(
            incident_id=incident_id,
            incident_key=incident_key,
            metrics=metrics,
            hypothesis=hypothesis,
        )
        data = incident_to_response(record)
        data["idempotent"] = False
        return OrchestratorResult(status_code=201, payload=data)

    def execute_incident(
        self,
        *,
        incident_id: str,
        approval_token: str | None,
        force_fail: bool = False,
    ) -> OrchestratorResult:
        incident = self._store.get_incident(incident_id)
        if incident is None:
            return OrchestratorResult(status_code=404, payload={"error": "incident_not_found"})

        try:
            plan = build_remediation_plan(incident)
        except UnsupportedIncidentTypeError as exc:
            return OrchestratorResult(
                status_code=422,
                payload={
                    "error": "unsupported_incident_type",
                    "detail": str(exc),
                    "status": "manual_review_required",
                },
            )

        if force_fail and plan.actions:
            first = plan.actions[0]
            plan.actions[0] = first.__class__(
                action_type=first.action_type,
                target=first.target,
                params={**first.params, "force_fail": True},
            )

        policy_decision = evaluate_policy(
            plan=plan,
            confidence=incident.hypothesis.confidence,
            config=self._policy_config,
            approval_token=approval_token,
        )

        if policy_decision.status == "POLICY_BLOCKED":
            updated = self._store.update_execution_state(
                incident_id=incident_id,
                plan=plan,
                policy_decision=policy_decision,
                action_results=[],
            )
            payload = incident_to_response(updated)
            payload["execute_status"] = "blocked"
            return OrchestratorResult(status_code=403, payload=payload)

        if policy_decision.status == "APPROVAL_REQUIRED":
            updated = self._store.update_execution_state(
                incident_id=incident_id,
                plan=plan,
                policy_decision=policy_decision,
                action_results=[],
            )
            payload = incident_to_response(updated)
            payload["execute_status"] = "approval_required"
            return OrchestratorResult(status_code=202, payload=payload)

        action_results = execute_bounded_actions(plan.actions, self._action_adapter)
        updated = self._store.update_execution_state(
            incident_id=incident_id,
            plan=plan,
            policy_decision=policy_decision,
            action_results=action_results,
        )
        payload = incident_to_response(updated)
        payload["execute_status"] = (
            "failed" if any(result.status == "failed" for result in action_results) else "executed"
        )
        return OrchestratorResult(status_code=200, payload=payload)


class MetricsSource:
    def get_payload(self) -> str:
        raise NotImplementedError
