from __future__ import annotations

import unittest

from services.ops_graph.audit import AuditEntry
from services.ops_graph.rollback import RollbackResult
from services.ops_graph.verification import VerificationResult
from services.ops_graph.visibility import (
    DEFAULT_MANUAL_BASELINE_SECONDS,
    build_visibility_payload,
    compute_mttr,
)


class TestVisibilityProjection(unittest.TestCase):
    def _verification(self) -> VerificationResult:
        return VerificationResult(
            status="passed",
            reason="latency_recovered",
            metric="vllm:e2e_request_latency_seconds",
            observed_value=0.31,
            expected_direction="decreasing",
            threshold_seconds=0.80,
        )

    def _rollback(self) -> RollbackResult:
        return RollbackResult(status="not_needed", reason="verification_passed", actions=())

    def test_compute_mttr_with_partial_lifecycle_uses_safe_defaults(self) -> None:
        mttr = compute_mttr(
            created_at=1000.0,
            execution_completed_at=None,
            lifecycle_completed_at=None,
        )

        self.assertEqual(mttr.time_to_diagnosis_s, 1.0)
        self.assertEqual(mttr.time_to_safe_action_s, 1.0)
        self.assertEqual(mttr.time_to_recovery_s, 1.0)
        self.assertEqual(mttr.manual_baseline_s, DEFAULT_MANUAL_BASELINE_SECONDS)

    def test_compute_mttr_with_completed_timestamps(self) -> None:
        mttr = compute_mttr(
            created_at=1000.0,
            execution_completed_at=1012.0,
            lifecycle_completed_at=1030.0,
        )

        self.assertEqual(mttr.time_to_safe_action_s, 12.0)
        self.assertEqual(mttr.time_to_recovery_s, 30.0)
        self.assertEqual(mttr.improvement_s, DEFAULT_MANUAL_BASELINE_SECONDS - 30.0)

    def test_build_visibility_payload_contains_typed_and_plain_fields(self) -> None:
        audit_entries = (
            AuditEntry(
                step="verify",
                typed_data={"status": "passed"},
                plain_summary="Verification passed.",
                timestamp=1700000000.0,
            ),
        )
        mttr = compute_mttr(
            created_at=1000.0,
            execution_completed_at=1012.0,
            lifecycle_completed_at=1020.0,
        )

        payload = build_visibility_payload(
            incident_id="inc-lifecycle-001",
            lifecycle_status="resolved",
            verification=self._verification(),
            rollback=self._rollback(),
            audit_entries=audit_entries,
            mttr=mttr,
        )

        self.assertEqual(payload["incident_id"], "inc-lifecycle-001")
        self.assertEqual(payload["status"], "resolved")
        self.assertEqual(payload["verification"]["status"], "passed")
        self.assertEqual(payload["rollback"]["status"], "not_needed")
        self.assertEqual(len(payload["audit"]), 1)
        self.assertIn("plain_summary", payload)


if __name__ == "__main__":
    unittest.main()
