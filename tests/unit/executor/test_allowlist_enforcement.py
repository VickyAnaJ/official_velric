import unittest

from services.ops_graph.contracts import PlanAction
from services.ops_graph.executor import LocalActionAdapter


class TestAllowlistEnforcement(unittest.TestCase):
    def test_local_action_adapter_succeeds(self):
        adapter = LocalActionAdapter()
        result = adapter.run(
            PlanAction(
                action_type="shift_traffic",
                target="route:prod",
                params={"canary_percentage": 0},
            )
        )
        self.assertEqual(result.status, "succeeded")

    def test_local_action_adapter_can_fail(self):
        adapter = LocalActionAdapter()
        result = adapter.run(
            PlanAction(
                action_type="shift_traffic",
                target="route:prod",
                params={"force_fail": True},
            )
        )
        self.assertEqual(result.status, "failed")


if __name__ == "__main__":
    unittest.main()
