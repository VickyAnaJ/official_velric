from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

ALLOWED_ACTION_TYPES = {"shift_traffic", "set_deployment_status", "rollback_config"}
ALLOWED_ACTION_STATUSES = {"succeeded", "failed", "blocked"}
ALLOWED_EXECUTION_STATUSES = {"executed", "blocked", "approval_required", "failed"}


class MockExecutionContractError(ValueError):
    """Raised when mocked upstream execution payload is invalid."""


@dataclass(frozen=True)
class MockActionResult:
    action_type: str
    target: str
    status: str
    message: str


@dataclass(frozen=True)
class MockExecutionState:
    incident_id: str
    execution_status: str
    action_results: tuple[MockActionResult, ...]


def _parse_action_result(raw: Any, index: int) -> MockActionResult:
    if not isinstance(raw, Mapping):
        raise MockExecutionContractError(f"action_results[{index}] must be an object")

    action_type = raw.get("action_type")
    if not isinstance(action_type, str) or action_type not in ALLOWED_ACTION_TYPES:
        raise MockExecutionContractError(f"action_results[{index}].action_type is unsupported")

    target = raw.get("target")
    if not isinstance(target, str) or not target.strip():
        raise MockExecutionContractError(f"action_results[{index}].target must be a non-empty string")

    status = raw.get("status")
    if not isinstance(status, str) or status not in ALLOWED_ACTION_STATUSES:
        raise MockExecutionContractError(f"action_results[{index}].status is invalid")

    message = raw.get("message", "")
    if not isinstance(message, str):
        raise MockExecutionContractError(f"action_results[{index}].message must be a string")

    return MockActionResult(action_type=action_type, target=target, status=status, message=message)


def parse_mock_execution_state(payload: Mapping[str, Any]) -> MockExecutionState:
    """Validate and normalize mocked execution output from an upstream slice contract."""
    incident_id = payload.get("incident_id")
    if not isinstance(incident_id, str) or not incident_id.strip():
        raise MockExecutionContractError("incident_id must be a non-empty string")

    execution_status = payload.get("execute_status", "executed")
    if not isinstance(execution_status, str) or execution_status not in ALLOWED_EXECUTION_STATUSES:
        raise MockExecutionContractError("execute_status is invalid")

    raw_results = payload.get("action_results")
    if raw_results is None:
        raise MockExecutionContractError("action_results is required")
    if not isinstance(raw_results, list):
        raise MockExecutionContractError("action_results must be an array")
    if not raw_results:
        raise MockExecutionContractError("action_results must not be empty")

    normalized = tuple(_parse_action_result(item, index) for index, item in enumerate(raw_results))
    return MockExecutionState(
        incident_id=incident_id,
        execution_status=execution_status,
        action_results=normalized,
    )
