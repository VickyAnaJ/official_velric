from __future__ import annotations

from uuid import uuid4

from .contracts import IncidentRecord, PlanAction, RemediationPlan


class UnsupportedIncidentTypeError(ValueError):
    """Raised when planning is requested for an unsupported incident type."""


def build_remediation_plan(incident: IncidentRecord) -> RemediationPlan:
    incident_type = incident.hypothesis.incident_type

    if incident_type == "latency_regression":
        actions = [
            PlanAction(
                action_type="shift_traffic",
                target="route:prod_split",
                params={"canary_percentage": 0},
            ),
            PlanAction(
                action_type="set_deployment_status",
                target="deployment:canary",
                params={"status": "isolated"},
            ),
        ]
    elif incident_type == "capacity_pressure":
        actions = [
            PlanAction(
                action_type="rollback_config",
                target="config:runtime",
                params={"profile": "safe_defaults"},
            )
        ]
    else:
        raise UnsupportedIncidentTypeError(f"Unsupported incident type: {incident_type}")

    return RemediationPlan(
        plan_id=str(uuid4()),
        incident_id=incident.incident_id,
        actions=actions,
        verification_condition="p95 latency decreasing and request success stable",
        rollback_required=True,
    )
