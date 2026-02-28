from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN_JAC = ROOT / "main.jac"


class TestSliceOps02Contracts(unittest.TestCase):
    def setUp(self) -> None:
        self.source = MAIN_JAC.read_text()

    def test_policy_and_action_contracts_exist(self) -> None:
        self.assertIn("obj PolicyDecision", self.source)
        self.assertIn("obj ActionResult", self.source)
        self.assertIn("POLICY_ALLOWLIST", self.source)

    def test_execute_incident_public_entry_exists(self) -> None:
        self.assertRegex(
            self.source,
            r"def:pub execute_incident\(",
        )

    def test_policy_states_are_typed_and_explicit(self) -> None:
        for state in ("PASS", "POLICY_BLOCKED", "APPROVAL_REQUIRED"):
            self.assertIn(state, self.source)

    def test_allowlist_contains_required_actions(self) -> None:
        for action in ("shift_traffic", "set_deployment_status", "rollback_config"):
            self.assertIn(action, self.source)

    def test_graph_update_projection_contract_exists(self) -> None:
        self.assertRegex(self.source, r"def project_graph_updates\(")
        self.assertIn("deployment:canary", self.source)
        self.assertIn("route:prod_split", self.source)

    def test_input_validation_contract_contains_incident_id_guard(self) -> None:
        self.assertIn("current_stage\": \"input_validation\"", self.source)
        self.assertIn("execute_status\": \"invalid_input\"", self.source)
        self.assertIn("INCIDENT_ID_REQUIRED", self.source)
        self.assertIn("INVALID_APPROVAL_TOKEN", self.source)
        self.assertIn("INVALID_CONFIDENCE_RANGE", self.source)


if __name__ == "__main__":
    unittest.main()
