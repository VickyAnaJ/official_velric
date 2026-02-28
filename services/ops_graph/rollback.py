from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .mock_execution_contract import MockActionResult


class RollbackError(ValueError):
    """Raised when rollback mapping cannot be completed safely."""


@dataclass(frozen=True)
class RollbackAction:
    action_type: str
    target: str
    params: dict[str, Any]
    status: str
    message: str


@dataclass(frozen=True)
class RollbackResult:
    status: str
    reason: str
    actions: tuple[RollbackAction, ...]


def inverse_action(action: MockActionResult) -> RollbackAction:
    if action.action_type == "shift_traffic":
        return RollbackAction(
            action_type="shift_traffic",
            target=action.target,
            params={"canary_percentage": 0},
            status="pending",
            message="inverse_action_prepared",
        )

    if action.action_type == "set_deployment_status":
        return RollbackAction(
            action_type="set_deployment_status",
            target=action.target,
            params={"status": "active"},
            status="pending",
            message="inverse_action_prepared",
        )

    if action.action_type == "rollback_config":
        return RollbackAction(
            action_type="rollback_config",
            target=action.target,
            params={"profile": "last_known_good"},
            status="pending",
            message="inverse_action_prepared",
        )

    raise RollbackError(f"unsupported_inverse_action:{action.action_type}")


def run_rollback(
    *,
    action_results: Iterable[MockActionResult],
    verification_status: str,
    fail_on_action_types: set[str] | None = None,
) -> RollbackResult:
    """Execute inverse actions when verification fails."""
    if verification_status != "failed":
        return RollbackResult(
            status="not_needed",
            reason="verification_passed",
            actions=(),
        )

    failures = fail_on_action_types if fail_on_action_types is not None else set()
    executed: list[RollbackAction] = []

    for item in action_results:
        if item.status != "succeeded":
            continue

        try:
            inverse = inverse_action(item)
        except RollbackError as exc:
            return RollbackResult(status="failed", reason=str(exc), actions=tuple(executed))

        if inverse.action_type in failures:
            executed.append(
                RollbackAction(
                    action_type=inverse.action_type,
                    target=inverse.target,
                    params=inverse.params,
                    status="failed",
                    message="simulated_rollback_failure",
                )
            )
        else:
            executed.append(
                RollbackAction(
                    action_type=inverse.action_type,
                    target=inverse.target,
                    params=inverse.params,
                    status="succeeded",
                    message="rollback_executed",
                )
            )

    if not executed:
        return RollbackResult(status="not_needed", reason="no_succeeded_actions", actions=())

    if any(action.status == "failed" for action in executed):
        return RollbackResult(status="failed", reason="rollback_failed", actions=tuple(executed))

    return RollbackResult(status="completed", reason="rollback_completed", actions=tuple(executed))
