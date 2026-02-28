import unittest

from services.ops_graph.app import create_app
from tests.support.deterministic import fixed_env, fixed_incident_key


class TestOutcomeOrchestratorPaths(unittest.TestCase):
    def test_lifecycle_pass_path(self):
        app = create_app(env=fixed_env())
        s1, trigger = app.trigger_incident({"incident_key": fixed_incident_key(60)})
        self.assertEqual(s1, 201)

        s2, _exec = app.execute_incident({"incident_id": trigger["incident_id"]})
        self.assertEqual(s2, 200)

        s3, lifecycle = app.process_lifecycle(
            {
                "incident_id": trigger["incident_id"],
                "observed_metrics": {"vllm:e2e_request_latency_seconds": 0.2},
            }
        )
        self.assertEqual(s3, 200)
        self.assertEqual(lifecycle["verification_result"]["status"], "passed")

    def test_lifecycle_triggers_rollback_on_fail(self):
        app = create_app(env=fixed_env())
        s1, trigger = app.trigger_incident({"incident_key": fixed_incident_key(61)})
        self.assertEqual(s1, 201)
        s2, _exec = app.execute_incident({"incident_id": trigger["incident_id"]})
        self.assertEqual(s2, 200)

        s3, lifecycle = app.process_lifecycle(
            {
                "incident_id": trigger["incident_id"],
                "observed_metrics": {"vllm:e2e_request_latency_seconds": 1.5},
            }
        )
        self.assertEqual(s3, 200)
        self.assertEqual(lifecycle["verification_result"]["status"], "failed")
        self.assertIn(lifecycle["rollback_result"]["status"], {"completed", "failed"})


if __name__ == "__main__":
    unittest.main()
