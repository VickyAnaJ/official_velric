import unittest

from services.ops_graph.mock_metrics import generate_metrics_payload, parse_metrics_payload
from services.ops_graph.triage import classify_incident


class TestHypothesisShape(unittest.TestCase):
    def test_hypothesis_has_required_fields(self):
        metrics = parse_metrics_payload(generate_metrics_payload())
        hypothesis = classify_incident(metrics)
        self.assertIsInstance(hypothesis.incident_type, str)
        self.assertTrue(0.0 <= hypothesis.confidence <= 1.0)
        self.assertTrue(hypothesis.summary)


if __name__ == "__main__":
    unittest.main()
