from __future__ import annotations

from .contracts import ActionResult, PlanAction


class ActionAdapter:
    def run(self, action: PlanAction) -> ActionResult:
        raise NotImplementedError


class LocalActionAdapter(ActionAdapter):
    def run(self, action: PlanAction) -> ActionResult:
        if bool(action.params.get("force_fail", False)):
            return ActionResult(
                action_type=action.action_type,
                target=action.target,
                status="failed",
                message="simulated_action_failure",
            )

        return ActionResult(
            action_type=action.action_type,
            target=action.target,
            status="succeeded",
            message="executed",
        )


def execute_bounded_actions(actions: list[PlanAction], adapter: ActionAdapter) -> list[ActionResult]:
    return [adapter.run(action) for action in actions]
