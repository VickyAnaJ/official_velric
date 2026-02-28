from __future__ import annotations

import unittest

from services.ops_graph.mock_execution_contract import (
    MockExecutionContractError,
    parse_mock_execution_state,
)


class TestMockExecutionContractAdapter(unittest.TestCase):
    def test_accepts_valid_mocked_execution_payload(self) -> None:
        payload = {
            "incident_id": "inc-123",
            "execute_status": "executed",
            "action_results": [
                {
                    "action_type": "shift_traffic",
                    "target": "route:prod_split",
                    "status": "succeeded",
                    "message": "ok",
                }
            ],
        }

        parsed = parse_mock_execution_state(payload)

        self.assertEqual(parsed.incident_id, "inc-123")
        self.assertEqual(parsed.execution_status, "executed")
        self.assertEqual(len(parsed.action_results), 1)
        self.assertEqual(parsed.action_results[0].action_type, "shift_traffic")

    def test_rejects_missing_action_results(self) -> None:
        with self.assertRaises(MockExecutionContractError):
            parse_mock_execution_state({"incident_id": "inc-123", "execute_status": "executed"})

    def test_rejects_unsupported_action_type(self) -> None:
        payload = {
            "incident_id": "inc-123",
            "execute_status": "executed",
            "action_results": [
                {
                    "action_type": "delete_cluster",
                    "target": "cluster:prod",
                    "status": "succeeded",
                    "message": "nope",
                }
            ],
        }

        with self.assertRaises(MockExecutionContractError):
            parse_mock_execution_state(payload)

    def test_rejects_malformed_action_status(self) -> None:
        payload = {
            "incident_id": "inc-123",
            "execute_status": "executed",
            "action_results": [
                {
                    "action_type": "rollback_config",
                    "target": "config:runtime",
                    "status": "unknown",
                    "message": "bad",
                }
            ],
        }

        with self.assertRaises(MockExecutionContractError):
            parse_mock_execution_state(payload)


if __name__ == "__main__":
    unittest.main()
