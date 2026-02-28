import unittest

from services.ops_graph.verification import evaluate_recovery


class TestRecoveryEvaluation(unittest.TestCase):
    def test_pass_when_latency_below_threshold(self):
        result = evaluate_recovery(observed_metrics={"vllm:e2e_request_latency_seconds": 0.2})
        self.assertEqual(result.status, "passed")

    def test_fail_when_latency_above_threshold(self):
        result = evaluate_recovery(observed_metrics={"vllm:e2e_request_latency_seconds": 1.2})
        self.assertEqual(result.status, "failed")


if __name__ == "__main__":
    unittest.main()
