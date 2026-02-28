from __future__ import annotations

import unittest

from services.ops_graph.lifecycle_endpoint import process_lifecycle_request


class TestLifecycleEndpointOrchestrator(unittest.TestCase):
    def _base_body(self) -> dict[str, object]:
        return {
            "incident_id": "inc-lifecycle-001",
            "execute_status": "executed",
            "action_results": [
                {
                    "action_type": "shift_traffic",
                    "target": "route:prod_split",
                    "status": "succeeded",
                    "message": "executed",
                }
            ],
            "observed_metrics": {"vllm:e2e_request_latency_seconds": 0.25},
            "created_at": 1000.0,
            "execution_completed_at": 1010.0,
            "lifecycle_completed_at": 1020.0,
        }

    def test_resolved_path_when_verification_passes(self) -> None:
        result = process_lifecycle_request(self._base_body())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.payload["status"], "resolved")
        self.assertEqual(result.payload["rollback"]["status"], "not_needed")

    def test_resolved_with_rollback_when_verification_fails(self) -> None:
        body = self._base_body()
        body["observed_metrics"] = {"vllm:e2e_request_latency_seconds": 1.20}

        result = process_lifecycle_request(body)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.payload["status"], "resolved_with_rollback")
        self.assertEqual(result.payload["rollback"]["status"], "completed")

    def test_manual_review_when_rollback_fails(self) -> None:
        body = self._base_body()
        body["observed_metrics"] = {"vllm:e2e_request_latency_seconds": 1.20}
        body["rollback_fail_on"] = ["shift_traffic"]

        result = process_lifecycle_request(body)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.payload["status"], "manual_review_required")
        self.assertEqual(result.payload["rollback"]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
