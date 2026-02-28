import unittest

from services.ops_graph.contracts import PlanAction, PolicyConfig, RemediationPlan
from services.ops_graph.policy import evaluate_policy


class TestPolicyGateDecisions(unittest.TestCase):
    def setUp(self):
        self.plan = RemediationPlan(
            plan_id="p1",
            incident_id="inc-1",
            actions=[
                PlanAction(
                    action_type="shift_traffic",
                    target="route:prod",
                    params={"canary_percentage": 0},
                )
            ],
            verification_condition="ok",
            rollback_required=True,
        )

    def test_policy_blocks_low_confidence(self):
        decision = evaluate_policy(
            plan=self.plan,
            confidence=0.5,
            config=PolicyConfig(("shift_traffic",), 0.8, False),
            approval_token=None,
        )
        self.assertEqual(decision.status, "POLICY_BLOCKED")

    def test_policy_requires_approval(self):
        decision = evaluate_policy(
            plan=self.plan,
            confidence=0.9,
            config=PolicyConfig(("shift_traffic",), 0.8, True),
            approval_token=None,
        )
        self.assertEqual(decision.status, "APPROVAL_REQUIRED")

    def test_policy_passes(self):
        decision = evaluate_policy(
            plan=self.plan,
            confidence=0.9,
            config=PolicyConfig(("shift_traffic",), 0.8, True),
            approval_token="approved",
        )
        self.assertEqual(decision.status, "PASS")


if __name__ == "__main__":
    unittest.main()
