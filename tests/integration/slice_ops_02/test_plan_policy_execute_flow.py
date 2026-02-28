import json
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from services.ops_graph.app import create_app, start_server
from services.ops_graph.contracts import PolicyConfig
from tests.support.deterministic import fixed_env, fixed_incident_key


class TestPlanPolicyExecuteFlow(unittest.TestCase):
    def test_execute_success_path(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            trigger_req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=json.dumps({"incident_key": fixed_incident_key(40)}).encode("utf-8"),
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
                self.assertEqual(res.status, 200)
                self.assertEqual(payload["execute_status"], "executed")
                self.assertEqual(payload["policy_decision"]["status"], "PASS")
        finally:
            server.shutdown()
            server.server_close()

    def test_policy_block_path(self):
        app = create_app(
            env=fixed_env(),
            policy_config=PolicyConfig(
                allowlisted_actions=("shift_traffic", "set_deployment_status", "rollback_config"),
                confidence_threshold=0.99,
                require_approval=False,
            ),
        )
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            trigger_req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=json.dumps({"incident_key": fixed_incident_key(41)}).encode("utf-8"),
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
            with self.assertRaises(HTTPError) as ctx:
                urlopen(execute_req)
            payload = json.loads(ctx.exception.read().decode("utf-8"))
            self.assertEqual(ctx.exception.code, 403)
            self.assertEqual(payload["execute_status"], "blocked")
            self.assertEqual(payload["policy_decision"]["status"], "POLICY_BLOCKED")
        finally:
            server.shutdown()
            server.server_close()

    def test_action_failure_path(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            trigger_req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=json.dumps({"incident_key": fixed_incident_key(42)}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(trigger_req) as res:
                incident_id = json.loads(res.read().decode("utf-8"))["incident_id"]

            execute_req = Request(
                f"http://{host}:{port}/incident/execute",
                data=json.dumps({"incident_id": incident_id, "force_fail": True}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(execute_req) as res:
                payload = json.loads(res.read().decode("utf-8"))
                self.assertEqual(res.status, 200)
                self.assertEqual(payload["execute_status"], "failed")
                self.assertTrue(any(r["status"] == "failed" for r in payload["action_results"]))
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
