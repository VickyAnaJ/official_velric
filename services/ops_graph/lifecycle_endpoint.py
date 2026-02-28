from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .audit import build_lifecycle_audit_entries
from .mock_execution_contract import MockExecutionContractError, parse_mock_execution_state
from .rollback import run_rollback
from .verification import VerificationError, evaluate_recovery
from .visibility import build_visibility_payload, compute_mttr


@dataclass(frozen=True)
class LifecycleEndpointResult:
    status_code: int
    payload: dict[str, object]


class LifecycleEndpointError(ValueError):
    """Raised when lifecycle request input is invalid."""


def _to_float(value: object, *, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise LifecycleEndpointError(f"{field_name} must be numeric") from exc


def process_lifecycle_request(body: Mapping[str, Any]) -> LifecycleEndpointResult:
    """Process lifecycle endpoint payload using mocked upstream execution contracts."""
    incident_id = body.get("incident_id")
    if not isinstance(incident_id, str) or not incident_id.strip():
        return LifecycleEndpointResult(status_code=400, payload={"error": "incident_id is required"})

    try:
        execution_state = parse_mock_execution_state(body)
    except MockExecutionContractError as exc:
        return LifecycleEndpointResult(
            status_code=422,
            payload={
                "error": "invalid_execution_contract",
                "detail": str(exc),
                "status": "manual_review_required",
            },
        )

    observed_metrics = body.get("observed_metrics")
    if not isinstance(observed_metrics, Mapping):
        return LifecycleEndpointResult(
            status_code=400,
            payload={"error": "observed_metrics must be an object"},
        )

    try:
        verification = evaluate_recovery(observed_metrics=observed_metrics)
    except VerificationError as exc:
        return LifecycleEndpointResult(
            status_code=422,
            payload={
                "error": "verification_failed",
                "detail": str(exc),
                "status": "manual_review_required",
            },
        )

    fail_on = body.get("rollback_fail_on", [])
    if not isinstance(fail_on, list):
        return LifecycleEndpointResult(
            status_code=400,
            payload={"error": "rollback_fail_on must be an array when provided"},
        )

    rollback = run_rollback(
        action_results=execution_state.action_results,
        verification_status=verification.status,
        fail_on_action_types={str(item) for item in fail_on},
    )
    audit_entries = build_lifecycle_audit_entries(verification=verification, rollback=rollback)

    created_at = _to_float(body.get("created_at", 0.0), field_name="created_at")
    execution_completed_at = body.get("execution_completed_at")
    lifecycle_completed_at = body.get("lifecycle_completed_at")

    execution_completed_at_f = (
        _to_float(execution_completed_at, field_name="execution_completed_at")
        if execution_completed_at is not None
        else None
    )
    lifecycle_completed_at_f = (
        _to_float(lifecycle_completed_at, field_name="lifecycle_completed_at")
        if lifecycle_completed_at is not None
        else None
    )

    mttr = compute_mttr(
        created_at=created_at,
        execution_completed_at=execution_completed_at_f,
        lifecycle_completed_at=lifecycle_completed_at_f,
    )

    if verification.status == "passed":
        lifecycle_status = "resolved"
    elif rollback.status == "completed":
        lifecycle_status = "resolved_with_rollback"
    else:
        lifecycle_status = "manual_review_required"

    payload = build_visibility_payload(
        incident_id=incident_id,
        lifecycle_status=lifecycle_status,
        verification=verification,
        rollback=rollback,
        audit_entries=audit_entries,
        mttr=mttr,
    )

    return LifecycleEndpointResult(status_code=200, payload=payload)
