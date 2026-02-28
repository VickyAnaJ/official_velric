import json
import unittest
from urllib.request import urlopen, Request

from services.ops_graph.app import create_app, start_server
from tests.support.deterministic import fixed_env


class TestMetricsEndpointHTTP(unittest.TestCase):
    def test_metrics_endpoint_returns_required_metrics(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            with urlopen(f"http://{host}:{port}/metrics") as res:
                payload = res.read().decode("utf-8")
                self.assertEqual(res.status, 200)
                self.assertIn("vllm:e2e_request_latency_seconds", payload)
                self.assertIn("vllm:request_success_total", payload)
        finally:
            server.shutdown()
            server.server_close()

    def test_invalid_json_on_trigger(self):
        app = create_app(env=fixed_env())
        server, _thread = start_server(app)
        host, port = server.server_address
        try:
            req = Request(
                f"http://{host}:{port}/incident/trigger",
                data=b"{not-json}",
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(Exception):
                urlopen(req)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
