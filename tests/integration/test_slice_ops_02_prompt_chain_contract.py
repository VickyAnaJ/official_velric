from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN_JAC = ROOT / "main.jac"


class TestSliceOps02PromptChainContract(unittest.TestCase):
    def setUp(self) -> None:
        self.source = MAIN_JAC.read_text()

    def test_plan_policy_execute_sequence_is_present(self) -> None:
        self.assertIn("build_plan_from_hypothesis", self.source)
        self.assertIn("evaluate_policy", self.source)
        self.assertIn("run_allowlisted_actions", self.source)
        self.assertIn("project_graph_updates", self.source)

    def test_approval_pause_contract_is_present(self) -> None:
        self.assertIn("MANUAL_APPROVAL_REQUIRED", self.source)
        self.assertIn("approval_required", self.source)

    def test_policy_block_contract_is_present(self) -> None:
        self.assertIn("LOW_CONFIDENCE", self.source)
        self.assertIn("ACTION_NOT_ALLOWLISTED", self.source)
        self.assertIn("execute_status\": \"blocked\"", self.source)

    def test_invalid_input_contract_is_present(self) -> None:
        self.assertIn("execute_status\": \"invalid_input\"", self.source)
        self.assertIn("current_stage\": \"input_validation\"", self.source)
        self.assertIn("INVALID_CONFIDENCE_RANGE", self.source)

    def test_execute_status_contracts_cover_success_and_failure(self) -> None:
        self.assertIn("execute_status = \"executed\"", self.source)
        self.assertIn("execute_status = \"partial_execution\"", self.source)
        self.assertIn("mock_execution_failure", self.source)


if __name__ == "__main__":
    unittest.main()
