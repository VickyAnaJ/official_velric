import unittest

from services.ops_graph.app import create_app
from tests.support.deterministic import fixed_env, fixed_incident_key


class TestExecutePipelineOrder(unittest.TestCase):
    def test_execute_requires_existing_incident(self):
        app = create_app(env=fixed_env())
        status, body = app.execute_incident({"incident_id": "missing"})
        self.assertEqual(status, 404)
        self.assertEqual(body["error"], "incident_not_found")

    def test_trigger_then_execute_success(self):
        app = create_app(env=fixed_env())
        s1, payload = app.trigger_incident({"incident_key": fixed_incident_key(20)})
        self.assertEqual(s1, 201)
        incident_id = payload["incident_id"]

        s2, exec_payload = app.execute_incident({"incident_id": incident_id})
        self.assertEqual(s2, 200)
        self.assertEqual(exec_payload["execute_status"], "executed")


if __name__ == "__main__":
    unittest.main()
