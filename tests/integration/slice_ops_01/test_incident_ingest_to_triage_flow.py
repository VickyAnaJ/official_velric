import json
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from services.ops_graph.app import create_app, start_server
from services.ops_graph.orchestrator import MetricsSource
from tests.support.deterministic import fixed_env, fixed_incident_key


class BrokenMetricsSource(MetricsSource):
    def get_payload(self) -> str:
        raise RuntimeError("boom")


class TestIncidentIngestToTriageFlow(unittest.TestCase):
    def test_trigger_and_fetch_incident(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            body = json.dumps({"incident_key": fixed_incident_key(1)}).encode("utf-8")
            req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req) as res:
                self.assertEqual(res.status, 201)
                payload = json.loads(res.read().decode("utf-8"))

            incident_id = payload["incident_id"]
            with urlopen(f"http://{host}:{port}/incident/{incident_id}") as res:
                fetched = json.loads(res.read().decode("utf-8"))
                self.assertEqual(res.status, 200)
                self.assertEqual(fetched["incident_id"], incident_id)
                self.assertEqual(fetched["hypothesis"]["incident_type"], "latency_regression")
        finally:
            server.shutdown()
            server.server_close()

    def test_idempotent_trigger_with_same_incident_key(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            body = json.dumps({"incident_key": fixed_incident_key(2)}).encode("utf-8")
            req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req) as res:
                first = json.loads(res.read().decode("utf-8"))

            req2 = Request(
                f"http://{host}:{port}/incident/trigger",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req2) as res:
                second = json.loads(res.read().decode("utf-8"))
                self.assertEqual(res.status, 200)

            self.assertEqual(first["incident_id"], second["incident_id"])
            self.assertTrue(second["idempotent"])
        finally:
            server.shutdown()
            server.server_close()

    def test_unavailable_metrics_source_returns_fail_closed(self):
        app = create_app(env=fixed_env(), metrics_source=BrokenMetricsSource())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=b"{}",
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(HTTPError) as ctx:
                urlopen(req)
            payload = json.loads(ctx.exception.read().decode("utf-8"))
            self.assertEqual(ctx.exception.code, 503)
            self.assertEqual(payload["status"], "manual_review_required")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
