import unittest

from services.ops_graph.app import create_app
from tests.support.deterministic import fixed_env


class TestIncidentControllerValidation(unittest.TestCase):
    def test_invalid_incident_key(self):
        app = create_app(env=fixed_env())
        status, body = app.trigger_incident({"incident_key": ""})
        self.assertEqual(status, 400)
        self.assertIn("error", body)


if __name__ == "__main__":
    unittest.main()
