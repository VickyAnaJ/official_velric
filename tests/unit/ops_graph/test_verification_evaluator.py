from __future__ import annotations

import unittest

from services.ops_graph.verification import (
    DEFAULT_THRESHOLD_SECONDS,
    LATENCY_METRIC,
    VerificationError,
    evaluate_recovery,
)


class TestVerificationEvaluator(unittest.TestCase):
    def test_passes_when_latency_is_below_threshold(self) -> None:
        result = evaluate_recovery({LATENCY_METRIC: 0.32})

        self.assertEqual(result.status, "passed")
        self.assertEqual(result.reason, "latency_recovered")
        self.assertEqual(result.metric, LATENCY_METRIC)
        self.assertEqual(result.expected_direction, "decreasing")

    def test_passes_when_latency_equals_threshold(self) -> None:
        result = evaluate_recovery({LATENCY_METRIC: DEFAULT_THRESHOLD_SECONDS})
        self.assertEqual(result.status, "passed")

    def test_fails_when_latency_is_above_threshold(self) -> None:
        result = evaluate_recovery({LATENCY_METRIC: 1.12})

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.reason, "latency_above_threshold")

    def test_rejects_missing_metric(self) -> None:
        with self.assertRaises(VerificationError):
            evaluate_recovery({})

    def test_rejects_non_positive_threshold(self) -> None:
        with self.assertRaises(VerificationError):
            evaluate_recovery({LATENCY_METRIC: 0.1}, threshold_seconds=0.0)


if __name__ == "__main__":
    unittest.main()
