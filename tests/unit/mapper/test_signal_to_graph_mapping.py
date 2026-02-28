import unittest

from services.ops_graph.graph import InMemoryGraphStore
from services.ops_graph.mock_metrics import generate_metrics_payload, parse_metrics_payload
from services.ops_graph.triage import classify_incident


class TestSignalToGraphMapping(unittest.TestCase):
    def test_save_incident_from_parsed_metrics(self):
        store = InMemoryGraphStore()
        metrics = parse_metrics_payload(generate_metrics_payload())
        hypothesis = classify_incident(metrics)
        record = store.save_incident(
            incident_id="incident-a",
            incident_key="key-a",
            metrics=metrics,
            hypothesis=hypothesis,
        )
        self.assertEqual(record.incident_id, "incident-a")
        self.assertEqual(record.metrics["vllm:kv_cache_usage_perc"], 0.86)


if __name__ == "__main__":
    unittest.main()
