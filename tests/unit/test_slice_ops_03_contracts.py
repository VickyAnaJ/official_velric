from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN_JAC = ROOT / "main.jac"


class TestSliceOps03Contracts(unittest.TestCase):
    def setUp(self) -> None:
        self.source = MAIN_JAC.read_text()

    def test_lifecycle_contract_objects_exist(self) -> None:
        self.assertIn("obj VerificationResult", self.source)
        self.assertIn("obj RollbackResult", self.source)
        self.assertIn("obj AuditEntry", self.source)

    def test_lifecycle_walkers_exist(self) -> None:
        for walker_name in ("verify_walker", "rollback_walker", "audit_walker"):
            self.assertIn(f"walker {walker_name}", self.source)

    def test_verification_contract_helpers_exist(self) -> None:
        self.assertIn("def build_verification_result(", self.source)
        self.assertIn("def verification_threshold(metric: str) -> float", self.source)
        self.assertIn("force_verification_failure", self.source)

    def test_rollback_and_audit_helpers_exist(self) -> None:
        self.assertIn("def build_rollback_result(", self.source)
        self.assertIn("def build_audit_entries(", self.source)
        self.assertIn("def rollback_state_updates() -> dict", self.source)
        self.assertIn("def summarize_audit_step(step: str, typed_data: dict) -> str", self.source)

    def test_mttr_projection_exists(self) -> None:
        self.assertIn("def build_mttr_metrics(", self.source)
        self.assertIn('"manual_baseline_seconds"', self.source)
        self.assertIn('"seconds_saved_vs_manual"', self.source)


if __name__ == "__main__":
    unittest.main()
