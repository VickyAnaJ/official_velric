from __future__ import annotations

import unittest

from tests.support.lifecycle_fixtures import (
    assert_audit_append_only,
    build_execution_state_fixture,
)


class TestLifecycleFixtures(unittest.TestCase):
    def test_fixture_is_deterministic_for_verify_pass(self) -> None:
        one = build_execution_state_fixture(scenario="verify_pass")
        two = build_execution_state_fixture(scenario="verify_pass")
        self.assertEqual(one, two)

    def test_fixture_is_deterministic_for_verify_fail(self) -> None:
        one = build_execution_state_fixture(scenario="verify_fail")
        two = build_execution_state_fixture(scenario="verify_fail")
        self.assertEqual(one, two)

    def test_fixture_rejects_unsupported_scenario(self) -> None:
        with self.assertRaises(ValueError):
            build_execution_state_fixture(scenario="something_else")

    def test_audit_append_only_accepts_prefix_preserved_growth(self) -> None:
        before = [{"step": "verify", "summary": "ok"}]
        after = [
            {"step": "verify", "summary": "ok"},
            {"step": "audit", "summary": "Lifecycle audit entries appended."},
        ]
        assert_audit_append_only(before, after)

    def test_audit_append_only_rejects_shrink(self) -> None:
        before = [{"step": "verify", "summary": "ok"}]
        after: list[dict[str, str]] = []
        with self.assertRaises(AssertionError):
            assert_audit_append_only(before, after)

    def test_audit_append_only_rejects_prefix_mutation(self) -> None:
        before = [{"step": "verify", "summary": "ok"}]
        after = [
            {"step": "verify", "summary": "changed"},
            {"step": "audit", "summary": "Lifecycle audit entries appended."},
        ]
        with self.assertRaises(AssertionError):
            assert_audit_append_only(before, after)


if __name__ == "__main__":
    unittest.main()
