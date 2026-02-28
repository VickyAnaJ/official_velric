import json
import unittest
from urllib.request import Request, urlopen

from services.ops_graph.app import create_app, start_server
from tests.support.deterministic import fixed_env, fixed_incident_key


class TestVerifyToRollbackToAuditFlow(unittest.TestCase):
    def test_verify_success_audit_visibility(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            trigger_req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=json.dumps({"incident_key": fixed_incident_key(70)}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(trigger_req) as res:
                incident_id = json.loads(res.read().decode("utf-8"))["incident_id"]

            exec_req = Request(
                f"http://{host}:{port}/incident/execute",
                data=json.dumps({"incident_id": incident_id}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(exec_req) as res:
                self.assertEqual(res.status, 200)

            lifecycle_req = Request(
                f"http://{host}:{port}/incident/lifecycle",
                data=json.dumps(
                    {
                        "incident_id": incident_id,
                        "observed_metrics": {"vllm:e2e_request_latency_seconds": 0.2},
                    }
                ).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(lifecycle_req) as res:
                payload = json.loads(res.read().decode("utf-8"))
                self.assertEqual(res.status, 200)
                self.assertEqual(payload["verification_result"]["status"], "passed")
                self.assertEqual(payload["rollback_result"]["status"], "not_needed")
                self.assertTrue(payload["audit_entries"])
                self.assertIn("mttr_summary", payload)
        finally:
            server.shutdown()
            server.server_close()

    def test_verify_failure_triggers_rollback(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            trigger_req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=json.dumps({"incident_key": fixed_incident_key(71)}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(trigger_req) as res:
                incident_id = json.loads(res.read().decode("utf-8"))["incident_id"]

            exec_req = Request(
                f"http://{host}:{port}/incident/execute",
                data=json.dumps({"incident_id": incident_id}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(exec_req) as res:
                self.assertEqual(res.status, 200)

            lifecycle_req = Request(
                f"http://{host}:{port}/incident/lifecycle",
                data=json.dumps(
                    {
                        "incident_id": incident_id,
                        "observed_metrics": {"vllm:e2e_request_latency_seconds": 1.4},
                    }
                ).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(lifecycle_req) as res:
                payload = json.loads(res.read().decode("utf-8"))
                self.assertEqual(res.status, 200)
                self.assertEqual(payload["verification_result"]["status"], "failed")
                self.assertNotEqual(payload["rollback_result"]["status"], "not_needed")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
