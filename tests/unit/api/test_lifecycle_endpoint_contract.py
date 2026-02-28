import unittest

from services.ops_graph.app import create_app
from tests.support.deterministic import fixed_env


class TestLifecycleEndpointContract(unittest.TestCase):
    def test_requires_incident_id(self):
        app = create_app(env=fixed_env())
        status, payload = app.process_lifecycle({})
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "incident_id is required")


if __name__ == "__main__":
    unittest.main()
