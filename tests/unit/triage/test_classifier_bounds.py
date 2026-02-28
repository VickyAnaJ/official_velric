import unittest

from services.ops_graph.triage import classify_incident


class TestClassifierBounds(unittest.TestCase):
    def test_latency_regression_selected(self):
        hypothesis = classify_incident(
            {
                "vllm:e2e_request_latency_seconds": 1.3,
                "vllm:kv_cache_usage_perc": 0.4,
            }
        )
        self.assertEqual(hypothesis.incident_type, "latency_regression")

    def test_manual_review_on_low_signals(self):
        hypothesis = classify_incident(
            {
                "vllm:e2e_request_latency_seconds": 0.2,
                "vllm:kv_cache_usage_perc": 0.2,
            }
        )
        self.assertEqual(hypothesis.incident_type, "manual_review_required")


if __name__ == "__main__":
    unittest.main()
