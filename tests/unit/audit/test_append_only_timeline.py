import unittest

from services.ops_graph.audit import build_lifecycle_audit_entries
from services.ops_graph.contracts import RollbackResult, VerificationResult


class TestAppendOnlyTimeline(unittest.TestCase):
    def test_builds_verify_and_audit_entries(self):
        entries = build_lifecycle_audit_entries(
            verification=VerificationResult(
                status="passed",
                reason="ok",
                observed_latency_seconds=0.2,
                threshold_seconds=0.8,
            ),
            rollback=RollbackResult(status="not_needed", actions=[], reason="verification_passed"),
        )
        self.assertGreaterEqual(len(entries), 2)
        self.assertEqual(entries[0].step, "verify")


if __name__ == "__main__":
    unittest.main()
