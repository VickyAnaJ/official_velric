import unittest

from services.ops_graph.contracts import ActionResult
from services.ops_graph.rollback import inverse_action, run_rollback


class TestInverseActionMapping(unittest.TestCase):
    def test_inverse_mapping_for_shift_traffic(self):
        inverse = inverse_action(
            ActionResult(action_type="shift_traffic", target="route:prod", status="succeeded", message="ok")
        )
        self.assertEqual(inverse.action_type, "shift_traffic")

    def test_rollback_not_needed_without_actions(self):
        result = run_rollback([])
        self.assertEqual(result.status, "not_needed")


if __name__ == "__main__":
    unittest.main()
