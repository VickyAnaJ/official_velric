from __future__ import annotations

import unittest
import importlib.util
from pathlib import Path

from mock_vllm import REQUIRED_METRIC_NAMES, generate_metrics_payload, scenario_metrics


ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP_CHECK_PATH = ROOT / "tools" / "bootstrap_check.py"

spec = importlib.util.spec_from_file_location("bootstrap_check", BOOTSTRAP_CHECK_PATH)
assert spec is not None and spec.loader is not None
bootstrap_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap_check)


class TestBootstrapArtifacts(unittest.TestCase):
    def test_main_jac_exists(self) -> None:
        self.assertTrue((ROOT / "main.jac").exists())

    def test_mock_metrics_payload_contains_required_names(self) -> None:
        payload = generate_metrics_payload()
        for metric_name in REQUIRED_METRIC_NAMES:
            self.assertIn(metric_name, payload)

    def test_healthy_scenario_metrics_are_lower_risk(self) -> None:
        metrics = scenario_metrics("healthy")
        self.assertLess(metrics["vllm:e2e_request_latency_seconds"], 1.0)
        self.assertLess(metrics["vllm:kv_cache_usage_perc"], 0.9)

    def test_default_scenario_metrics_match_incident_shape(self) -> None:
        metrics = scenario_metrics("rollout_regression")
        self.assertGreater(metrics["vllm:e2e_request_latency_seconds"], 1.0)
        self.assertGreater(metrics["vllm:kv_cache_usage_perc"], 0.9)

    def test_requirements_declares_jaseci(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text()
        self.assertIn("jaseci", requirements)

    def test_bootstrap_check_passes(self) -> None:
        self.assertEqual(bootstrap_check.main(), 0)


if __name__ == "__main__":
    unittest.main()
