from __future__ import annotations

import unittest

from services.ops_graph.lifecycle_endpoint import process_lifecycle_request


class TestLifecycleEndpointContract(unittest.TestCase):
    def test_rejects_missing_incident_id(self) -> None:
        result = process_lifecycle_request({})
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.payload["error"], "incident_id is required")

    def test_rejects_missing_action_results(self) -> None:
        result = process_lifecycle_request(
            {
                "incident_id": "inc-001",
                "observed_metrics": {"vllm:e2e_request_latency_seconds": 0.20},
            }
        )

        self.assertEqual(result.status_code, 422)
        self.assertEqual(result.payload["error"], "invalid_execution_contract")

    def test_rejects_invalid_metric_payload(self) -> None:
        result = process_lifecycle_request(
            {
                "incident_id": "inc-001",
                "execute_status": "executed",
                "action_results": [
                    {
                        "action_type": "shift_traffic",
                        "target": "route:prod_split",
                        "status": "succeeded",
                        "message": "executed",
                    }
                ],
                "observed_metrics": "bad",
            }
        )

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.payload["error"], "observed_metrics must be an object")

    def test_success_contract(self) -> None:
        result = process_lifecycle_request(
            {
                "incident_id": "inc-001",
                "execute_status": "executed",
                "action_results": [
                    {
                        "action_type": "shift_traffic",
                        "target": "route:prod_split",
                        "status": "succeeded",
                        "message": "executed",
                    }
                ],
                "observed_metrics": {"vllm:e2e_request_latency_seconds": 0.30},
                "created_at": 1000.0,
                "execution_completed_at": 1010.0,
                "lifecycle_completed_at": 1020.0,
            }
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.payload["status"], "resolved")
        self.assertIn("mttr", result.payload)
        self.assertIn("audit", result.payload)

    def test_fail_then_rollback_contract(self) -> None:
        result = process_lifecycle_request(
            {
                "incident_id": "inc-001",
                "execute_status": "executed",
                "action_results": [
                    {
                        "action_type": "set_deployment_status",
                        "target": "deployment:canary",
                        "status": "succeeded",
                        "message": "executed",
                    }
                ],
                "observed_metrics": {"vllm:e2e_request_latency_seconds": 1.40},
                "created_at": 1000.0,
                "execution_completed_at": 1010.0,
                "lifecycle_completed_at": 1040.0,
            }
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.payload["status"], "resolved_with_rollback")
        self.assertEqual(result.payload["rollback"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
