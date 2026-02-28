from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN_JAC = ROOT / "main.jac"


class TestSliceOps03PromptChainContract(unittest.TestCase):
    def setUp(self) -> None:
        self.source = MAIN_JAC.read_text()

    def test_execute_path_triggers_lifecycle_walkers(self) -> None:
        self.assertIn("root spawn verify_walker(", self.source)
        self.assertIn("root spawn rollback_walker(", self.source)
        self.assertIn("root spawn audit_walker(", self.source)

    def test_get_incident_state_exposes_lifecycle_payload(self) -> None:
        self.assertIn('"verification": verification_payload(execution_state.get("verification", None))', self.source)
        self.assertIn('"rollback": rollback_payload(execution_state.get("rollback", None))', self.source)
        self.assertIn('"audit": audit_payload(execution_state.get("audit", []))', self.source)
        self.assertIn('"mttr": execution_state.get("mttr", build_mttr_metrics(None, None))', self.source)

    def test_ui_mentions_verification_and_mttr(self) -> None:
        self.assertIn("<h2>Audit Log + MTTR</h2>", self.source)
        self.assertIn("Recovery seconds:", self.source)
        self.assertIn("Manual baseline:", self.source)
        self.assertIn("Verification:", self.source)
        self.assertIn('incident = await execute_incident(seed["incident_id"])', self.source)
        self.assertIn("useEffect(lambda -> None {", self.source)
        self.assertIn("setInterval(lambda -> None { refresh_incident(); }, 1000);", self.source)

    def test_audit_contract_covers_success_and_failure_paths(self) -> None:
        self.assertIn('step="verify"', self.source)
        self.assertIn('step="rollback"', self.source)
        self.assertIn('step="audit"', self.source)
        self.assertIn("known_good_path_restored", self.source)


if __name__ == "__main__":
    unittest.main()
