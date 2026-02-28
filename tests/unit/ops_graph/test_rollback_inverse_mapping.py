from __future__ import annotations

import unittest

from services.ops_graph.mock_execution_contract import MockActionResult
from services.ops_graph.rollback import RollbackResult, run_rollback


class TestRollbackInverseMapping(unittest.TestCase):
    def test_returns_not_needed_when_verification_passes(self) -> None:
        result = run_rollback(action_results=(), verification_status="passed")

        self.assertEqual(result.status, "not_needed")
        self.assertEqual(result.reason, "verification_passed")
        self.assertEqual(result.actions, ())

    def test_builds_inverse_actions_for_succeeded_inputs(self) -> None:
        actions = (
            MockActionResult(
                action_type="shift_traffic",
                target="route:prod_split",
                status="succeeded",
                message="executed",
            ),
            MockActionResult(
                action_type="set_deployment_status",
                target="deployment:canary",
                status="succeeded",
                message="executed",
            ),
        )

        result = run_rollback(action_results=actions, verification_status="failed")

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.reason, "rollback_completed")
        self.assertEqual(len(result.actions), 2)
        self.assertEqual(result.actions[0].params["canary_percentage"], 0)
        self.assertEqual(result.actions[1].params["status"], "active")

    def test_skips_non_succeeded_action_results(self) -> None:
        actions = (
            MockActionResult(
                action_type="rollback_config",
                target="config:runtime",
                status="failed",
                message="already_failed",
            ),
        )

        result = run_rollback(action_results=actions, verification_status="failed")

        self.assertEqual(result.status, "not_needed")
        self.assertEqual(result.reason, "no_succeeded_actions")

    def test_fails_on_unsupported_inverse_action(self) -> None:
        actions = (
            MockActionResult(
                action_type="delete_cluster",
                target="cluster:prod",
                status="succeeded",
                message="executed",
            ),
        )

        result = run_rollback(action_results=actions, verification_status="failed")

        self.assertEqual(result.status, "failed")
        self.assertTrue(result.reason.startswith("unsupported_inverse_action:"))

    def test_handles_simulated_rollback_failure(self) -> None:
        actions = (
            MockActionResult(
                action_type="shift_traffic",
                target="route:prod_split",
                status="succeeded",
                message="executed",
            ),
        )

        result: RollbackResult = run_rollback(
            action_results=actions,
            verification_status="failed",
            fail_on_action_types={"shift_traffic"},
        )

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.reason, "rollback_failed")
        self.assertEqual(result.actions[0].status, "failed")


if __name__ == "__main__":
    unittest.main()
