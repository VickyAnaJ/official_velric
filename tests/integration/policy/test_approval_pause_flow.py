import json
import unittest
from urllib.request import Request, urlopen

from services.ops_graph.app import create_app, start_server
from services.ops_graph.contracts import PolicyConfig
from tests.support.deterministic import fixed_env, fixed_incident_key


class TestApprovalPauseFlow(unittest.TestCase):
    def test_execute_returns_approval_required_without_token(self):
        app = create_app(
            env=fixed_env(),
            policy_config=PolicyConfig(
                allowlisted_actions=("shift_traffic", "set_deployment_status", "rollback_config"),
                confidence_threshold=0.8,
                require_approval=True,
            ),
        )
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            trigger_req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=json.dumps({"incident_key": fixed_incident_key(30)}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(trigger_req) as res:
                incident_id = json.loads(res.read().decode("utf-8"))["incident_id"]

            execute_req = Request(
                f"http://{host}:{port}/incident/execute",
                data=json.dumps({"incident_id": incident_id}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(execute_req) as res:
                payload = json.loads(res.read().decode("utf-8"))
                self.assertEqual(res.status, 202)
                self.assertEqual(payload["execute_status"], "approval_required")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
