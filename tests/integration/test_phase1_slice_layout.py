from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestPhase1SliceLayout(unittest.TestCase):
    def test_trigger_incident_exposes_phase1_contract_fields(self) -> None:
        source = (ROOT / "main.jac").read_text()
        self.assertIn('"status": "pipeline_started"', source)
        self.assertIn('"primary_signals": incident.primary_signal_names', source)
        self.assertIn('"poll_url": "/walker/get_incident_state/" + incident_id', source)

    def test_get_incident_state_returns_typed_lifecycle_shape(self) -> None:
        source = (ROOT / "main.jac").read_text()
        self.assertIn('"current_stage": incident.current_stage', source)
        self.assertIn('"hypothesis": hypothesis_payload(hypothesis_from_incident(incident))', source)
        self.assertIn('"verification": verification_payload(None)', source)
        self.assertIn('"audit": []', source)
        self.assertIn('"requires_manual_review": incident.requires_manual_review', source)

    def test_ui_copy_mentions_incident_lifecycle_and_audit(self) -> None:
        source = (ROOT / "main.jac").read_text()
        self.assertIn("Walker-native inference incident response with verification, rollback, audit, and MTTR visibility.", source)
        self.assertIn("<h2>Incident Feed</h2>", source)
        self.assertIn("Verification:", source)
        self.assertIn("<h2>Typed Decisions</h2>", source)
        self.assertIn("Audit entries:", source)


if __name__ == "__main__":
    unittest.main()
