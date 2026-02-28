from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

from mock_vllm import generate_metrics_payload


ROOT = Path(__file__).resolve().parents[2]


class TestPhase1SliceContracts(unittest.TestCase):
    def test_mock_vllm_payload_contains_labeled_canary_metrics(self) -> None:
        payload = generate_metrics_payload()
        self.assertIn('vllm:e2e_request_latency_seconds{model_name="canary"}', payload)
        self.assertIn('vllm:kv_cache_usage_perc{model_name="canary"}', payload)

    def test_main_jac_contains_phase1_metric_parsing_helpers(self) -> None:
        source = (ROOT / "main.jac").read_text()
        self.assertIn("def parse_prometheus_metrics(payload: str) -> dict", source)
        self.assertIn("def primary_signal_names(metrics: dict) -> list[str]", source)
        self.assertIn("def fallback_incident_hypothesis(metrics: dict, signals: list[str]) -> IncidentHypothesis", source)

    def test_main_jac_contains_metric_node_and_phase1_incident_fields(self) -> None:
        source = (ROOT / "main.jac").read_text()
        self.assertIn("node Metric {", source)
        self.assertIn("has primary_signal_names: list[str] = [];", source)
        self.assertIn('has current_stage: str = "bootstrap";', source)

    def test_main_jac_contains_root_persistence_helper(self) -> None:
        source = (ROOT / "main.jac").read_text()
        self.assertIn("def persist_phase_1_incident(", source)
        self.assertIn("root ++> Incident(", source)
        self.assertIn("incident ++> Alert(", source)

    def test_main_jac_contains_triage_walker_flow(self) -> None:
        source = (ROOT / "main.jac").read_text()
        self.assertIn("walker triage_walker {", source)
        self.assertIn("can start with Root entry {", source)
        self.assertIn("root spawn triage_walker(incident_id=incident_id)", source)

    def test_main_jac_compiles_with_jac_runtime(self) -> None:
        result = subprocess.run(
            [str(ROOT / ".venv" / "bin" / "jac"), "run", "main.jac"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
