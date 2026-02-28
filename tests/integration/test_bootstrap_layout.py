from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestBootstrapLayout(unittest.TestCase):
    def test_readme_contains_three_command_flow(self) -> None:
        readme = (ROOT / "README.md").read_text()
        self.assertIn("export ANTHROPIC_API_KEY", readme)
        self.assertIn("python3 mock_vllm.py", readme)
        self.assertIn("jac start main.jac", readme)

    def test_main_jac_contains_required_walkers(self) -> None:
        source = (ROOT / "main.jac").read_text()
        for walker_name in (
            "triage_walker",
            "plan_walker",
            "execute_walker",
            "verify_walker",
            "rollback_walker",
            "audit_walker",
        ):
            self.assertIn(walker_name, source)


if __name__ == "__main__":
    unittest.main()
