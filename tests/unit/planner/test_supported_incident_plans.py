import unittest

from services.ops_graph.contracts import IncidentHypothesis, IncidentRecord
from services.ops_graph.planner import UnsupportedIncidentTypeError, build_remediation_plan


class TestSupportedIncidentPlans(unittest.TestCase):
    def test_build_latency_plan(self):
        incident = IncidentRecord(
            incident_id="inc-1",
            incident_key=None,
            status="active",
            severity="high",
            metrics={},
            hypothesis=IncidentHypothesis(
                incident_type="latency_regression",
                confidence=0.9,
                summary="latency high",
            ),
        )
        plan = build_remediation_plan(incident)
        self.assertEqual(plan.incident_id, "inc-1")
        self.assertGreaterEqual(len(plan.actions), 1)

    def test_unsupported_incident_type(self):
        incident = IncidentRecord(
            incident_id="inc-2",
            incident_key=None,
            status="active",
            severity="high",
            metrics={},
            hypothesis=IncidentHypothesis(
                incident_type="manual_review_required",
                confidence=0.5,
                summary="manual",
            ),
        )
        with self.assertRaises(UnsupportedIncidentTypeError):
            build_remediation_plan(incident)


if __name__ == "__main__":
    unittest.main()
