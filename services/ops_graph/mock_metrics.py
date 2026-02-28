from __future__ import annotations

REQUIRED_METRIC_NAMES = (
    "vllm:e2e_request_latency_seconds",
    "vllm:kv_cache_usage_perc",
    "vllm:num_requests_running",
    "vllm:request_success_total",
)


def generate_metrics_payload(
    latency_seconds: float = 1.25,
    kv_cache_usage: float = 0.86,
    requests_running: int = 37,
    request_success_total: int = 1452,
) -> str:
    # Prometheus text exposition format (minimal and deterministic for tests).
    return "\n".join(
        [
            f"{REQUIRED_METRIC_NAMES[0]} {latency_seconds}",
            f"{REQUIRED_METRIC_NAMES[1]} {kv_cache_usage}",
            f"{REQUIRED_METRIC_NAMES[2]} {requests_running}",
            f"{REQUIRED_METRIC_NAMES[3]} {request_success_total}",
            "",
        ]
    )


def parse_metrics_payload(payload: str) -> dict[str, float]:
    parsed: dict[str, float] = {}
    for raw_line in payload.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid metric line: {line}")
        key, value = parts
        parsed[key] = float(value)

    missing = [name for name in REQUIRED_METRIC_NAMES if name not in parsed]
    if missing:
        raise ValueError(f"Missing required metrics: {', '.join(missing)}")
    return parsed
