from __future__ import annotations

import unittest

from services.ops_graph.audit import append_audit_entries, build_lifecycle_audit_entries
from services.ops_graph.rollback import RollbackResult
from services.ops_graph.verification import VerificationResult
from tests.support.lifecycle_fixtures import assert_audit_append_only


class TestAuditAppendOnly(unittest.TestCase):
    def _verification(self, *, status: str) -> VerificationResult:
        return VerificationResult(
            status=status,
            reason="latency_recovered" if status == "passed" else "latency_above_threshold",
            metric="vllm:e2e_request_latency_seconds",
            observed_value=0.32 if status == "passed" else 1.20,
            expected_direction="decreasing",
            threshold_seconds=0.80,
        )

    def test_builds_verify_and_audit_entries_when_no_rollback(self) -> None:
        entries = build_lifecycle_audit_entries(
            verification=self._verification(status="passed"),
            rollback=RollbackResult(status="not_needed", reason="verification_passed", actions=()),
            now=1700000000.0,
        )

        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].step, "verify")
        self.assertEqual(entries[1].step, "audit")

    def test_builds_verify_rollback_and_audit_entries_when_rollback_occurs(self) -> None:
        entries = build_lifecycle_audit_entries(
            verification=self._verification(status="failed"),
            rollback=RollbackResult(status="completed", reason="rollback_completed", actions=()),
            now=1700000001.0,
        )

        self.assertEqual(len(entries), 3)
        self.assertEqual([entry.step for entry in entries], ["verify", "rollback", "audit"])

    def test_append_audit_entries_preserves_prefix(self) -> None:
        existing = build_lifecycle_audit_entries(
            verification=self._verification(status="passed"),
            rollback=RollbackResult(status="not_needed", reason="verification_passed", actions=()),
            now=1700000002.0,
        )
        new_entries = build_lifecycle_audit_entries(
            verification=self._verification(status="failed"),
            rollback=RollbackResult(status="failed", reason="rollback_failed", actions=()),
            now=1700000003.0,
        )

        combined = append_audit_entries(existing, new_entries)

        before_dicts = [
            {"step": e.step, "summary": e.plain_summary, "timestamp": e.timestamp}
            for e in existing
        ]
        after_dicts = [
            {"step": e.step, "summary": e.plain_summary, "timestamp": e.timestamp}
            for e in combined
        ]
        assert_audit_append_only(before_dicts, after_dicts)


if __name__ == "__main__":
    unittest.main()
