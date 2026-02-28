#!/usr/bin/env python3
from __future__ import annotations

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REQUIRED_METRIC_NAMES = (
    "vllm:e2e_request_latency_seconds",
    "vllm:kv_cache_usage_perc",
    "vllm:num_requests_running",
    "vllm:request_success_total",
)


def scenario_metrics(scenario: str) -> dict[str, float]:
    if scenario == "healthy":
        return {
            "vllm:e2e_request_latency_seconds": 0.18,
            "vllm:kv_cache_usage_perc": 0.42,
            "vllm:num_requests_running": 6.0,
            "vllm:request_success_total": 2401.0,
        }

    return {
        "vllm:e2e_request_latency_seconds": 1.34,
        "vllm:kv_cache_usage_perc": 0.94,
        "vllm:num_requests_running": 47.0,
        "vllm:request_success_total": 1821.0,
    }


def generate_metrics_payload(scenario: str = "rollout_regression") -> str:
    metrics = scenario_metrics(scenario)
    lines = [
        "# HELP vllm:e2e_request_latency_seconds End-to-end request latency",
        "# TYPE vllm:e2e_request_latency_seconds histogram",
        f'{REQUIRED_METRIC_NAMES[0]}{{model_name="canary"}} {metrics[REQUIRED_METRIC_NAMES[0]]}',
        "# HELP vllm:kv_cache_usage_perc KV cache utilization",
        "# TYPE vllm:kv_cache_usage_perc gauge",
        f'{REQUIRED_METRIC_NAMES[1]}{{model_name="canary"}} {metrics[REQUIRED_METRIC_NAMES[1]]}',
        "# HELP vllm:num_requests_running Number running",
        "# TYPE vllm:num_requests_running gauge",
        f'{REQUIRED_METRIC_NAMES[2]}{{model_name="canary"}} {metrics[REQUIRED_METRIC_NAMES[2]]}',
        f'{REQUIRED_METRIC_NAMES[2]}{{model_name="baseline"}} 8.0',
        "# HELP vllm:request_success_total Number of successful requests",
        "# TYPE vllm:request_success_total counter",
        f'{REQUIRED_METRIC_NAMES[3]}{{finished_reason="stop"}} {metrics[REQUIRED_METRIC_NAMES[3]]}',
        "",
    ]
    return "\n".join(lines)


def build_handler(metrics_payload: str):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/healthz":
                body = b"ok"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/metrics":
                body = metrics_payload.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; version=0.0.4")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            self.send_response(404)
            self.end_headers()

        def log_message(self, _format: str, *_args: object) -> None:
            return

    return Handler


def main() -> int:
    host = os.environ.get("MOCK_VLLM_HOST", "127.0.0.1")
    port = int(os.environ.get("MOCK_VLLM_PORT", "9000"))
    scenario = os.environ.get("MOCK_VLLM_SCENARIO", "rollout_regression")
    payload = generate_metrics_payload(scenario)

    server = ThreadingHTTPServer((host, port), build_handler(payload))
    print(f"mock_vllm serving {scenario} metrics on http://{host}:{port}/metrics")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
