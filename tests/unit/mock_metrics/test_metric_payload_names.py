import unittest

from services.ops_graph.mock_metrics import REQUIRED_METRIC_NAMES, generate_metrics_payload, parse_metrics_payload


class TestMetricPayloadNames(unittest.TestCase):
    def test_payload_contains_required_metrics(self):
        payload = generate_metrics_payload()
        for name in REQUIRED_METRIC_NAMES:
            self.assertIn(name, payload)

    def test_parse_rejects_missing_metrics(self):
        with self.assertRaises(ValueError):
            parse_metrics_payload("vllm:e2e_request_latency_seconds 1.0")


if __name__ == "__main__":
    unittest.main()
