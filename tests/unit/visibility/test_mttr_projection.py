import unittest

from services.ops_graph.contracts import IncidentHypothesis, IncidentRecord
from services.ops_graph.visibility import compute_mttr


class TestMttrProjection(unittest.TestCase):
    def test_mttr_projection(self):
        incident = IncidentRecord(
            incident_id="inc-mttr",
            incident_key=None,
            status="resolved",
            severity="high",
            metrics={},
            hypothesis=IncidentHypothesis(
                incident_type="latency_regression",
                confidence=0.9,
                summary="ok",
            ),
            created_at=100.0,
            execution_completed_at=110.0,
            lifecycle_completed_at=120.0,
        )
        mttr = compute_mttr(incident, manual_baseline_s=1800.0)
        self.assertGreater(mttr.time_to_recovery_s, 0)
        self.assertGreaterEqual(mttr.improvement_s, 0)


if __name__ == "__main__":
    unittest.main()
