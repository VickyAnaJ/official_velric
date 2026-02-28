import unittest

from services.ops_graph.contracts import IncidentHypothesis, IncidentRecord


class TestNodeContracts(unittest.TestCase):
    def test_incident_record_contract(self):
        hypothesis = IncidentHypothesis(
            incident_type="latency_regression",
            confidence=0.92,
            summary="ok",
        )
        record = IncidentRecord(
            incident_id="id-1",
            incident_key="key-1",
            status="active",
            severity="high",
            metrics={"vllm:e2e_request_latency_seconds": 1.2},
            hypothesis=hypothesis,
        )
        self.assertEqual(record.status, "active")
        self.assertEqual(record.hypothesis.incident_type, "latency_regression")


if __name__ == "__main__":
    unittest.main()
