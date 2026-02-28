from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import Any

from .config import AppConfig, load_config
from .graph import InMemoryGraphStore, incident_to_response
from .mock_metrics import generate_metrics_payload
from .orchestrator import IncidentOrchestrator, MetricsSource, MetricsSourceError


class StaticMetricsSource(MetricsSource):
    def __init__(self, payload_factory=generate_metrics_payload):
        self._payload_factory = payload_factory

    def get_payload(self) -> str:
        return self._payload_factory()


class OpsGraphApp:
    def __init__(self, config: AppConfig, metrics_source: MetricsSource | None = None) -> None:
        self.config = config
        self.store = InMemoryGraphStore()
        self.metrics_source = metrics_source if metrics_source is not None else StaticMetricsSource()
        self.orchestrator = IncidentOrchestrator(self.store, self.metrics_source)

    def get_metrics(self) -> tuple[int, str, str]:
        return 200, "text/plain; version=0.0.4", self.metrics_source.get_payload()

    def trigger_incident(self, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        incident_key = body.get("incident_key")
        if incident_key is not None and (not isinstance(incident_key, str) or not incident_key.strip()):
            return 400, {"error": "incident_key must be a non-empty string when provided"}

        try:
            result = self.orchestrator.trigger_incident(incident_key=incident_key)
            return result.status_code, result.payload
        except MetricsSourceError:
            return 503, {
                "error": "metrics_source_unavailable",
                "status": "manual_review_required",
            }
        except ValueError as exc:
            return 422, {
                "error": "invalid_metrics_payload",
                "detail": str(exc),
                "status": "manual_review_required",
            }

    def get_incident(self, incident_id: str) -> tuple[int, dict[str, Any]]:
        record = self.store.get_incident(incident_id)
        if record is None:
            return 404, {"error": "incident_not_found"}
        return 200, incident_to_response(record)


def create_app(env: dict[str, str] | None = None, metrics_source: MetricsSource | None = None) -> OpsGraphApp:
    return OpsGraphApp(config=load_config(env=env), metrics_source=metrics_source)


def build_handler(app: OpsGraphApp):
    class Handler(BaseHTTPRequestHandler):
        def _write_json(self, code: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _write_text(self, code: int, payload: str, content_type: str) -> None:
            body = payload.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self) -> dict[str, Any]:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length == 0:
                return {}
            raw = self.rfile.read(content_length)
            return json.loads(raw.decode("utf-8"))

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/metrics":
                code, ctype, payload = app.get_metrics()
                self._write_text(code, payload, ctype)
                return

            if self.path.startswith("/incident/"):
                incident_id = self.path.removeprefix("/incident/")
                code, payload = app.get_incident(incident_id)
                self._write_json(code, payload)
                return

            self._write_json(404, {"error": "route_not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path == "/incident/trigger":
                try:
                    body = self._read_json()
                except json.JSONDecodeError:
                    self._write_json(400, {"error": "invalid_json"})
                    return
                code, payload = app.trigger_incident(body)
                self._write_json(code, payload)
                return
            self._write_json(404, {"error": "route_not_found"})

        def log_message(self, _format: str, *_args: object) -> None:
            # Keep tests deterministic and silent.
            return

    return Handler


def start_server(app: OpsGraphApp, host: str = "127.0.0.1", port: int = 0):
    server = ThreadingHTTPServer((host, port), build_handler(app))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread
