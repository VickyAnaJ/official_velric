from __future__ import annotations

from .contracts import ActionResult, PlanAction, RollbackResult
from .executor import ActionAdapter, LocalActionAdapter


class UnsupportedRollbackAction(ValueError):
    """Raised when inverse mapping for an action does not exist."""


def inverse_action(action: ActionResult) -> PlanAction:
    if action.action_type == "shift_traffic":
        return PlanAction(
            action_type="shift_traffic",
            target=action.target,
            params={"canary_percentage": 0},
        )
    if action.action_type == "set_deployment_status":
        return PlanAction(
            action_type="set_deployment_status",
            target=action.target,
            params={"status": "active"},
        )
    if action.action_type == "rollback_config":
        return PlanAction(
            action_type="rollback_config",
            target=action.target,
            params={"profile": "last_known_good"},
        )
    raise UnsupportedRollbackAction(action.action_type)


def run_rollback(
    action_results: list[ActionResult],
    adapter: ActionAdapter | None = None,
) -> RollbackResult:
    if not action_results:
        return RollbackResult(status="not_needed", actions=[], reason="no_actions_to_rollback")

    active_adapter = adapter if adapter is not None else LocalActionAdapter()
    rollback_results: list[ActionResult] = []
    try:
        for action_result in action_results:
            if action_result.status != "succeeded":
                continue
            rollback_action = inverse_action(action_result)
            rollback_results.append(active_adapter.run(rollback_action))
    except UnsupportedRollbackAction as exc:
        return RollbackResult(status="failed", actions=rollback_results, reason=f"unsupported:{exc}")

    failed = any(item.status == "failed" for item in rollback_results)
    return RollbackResult(
        status="failed" if failed else "completed",
        actions=rollback_results,
        reason="rollback_failed" if failed else "rollback_completed",
    )
