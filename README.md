# Ops Graph

Ops Graph is a Jac/Jaseci-native incident response demo for inference-serving failures.
It ingests mock vLLM metrics, builds typed incident state, and runs the walker pipeline
inside [`main.jac`](main.jac).

## What Runs Here

- [`main.jac`](main.jac): canonical Jac entrypoint for the backend and Jac UI
- [`mock_vllm.py`](mock_vllm.py): local mock Prometheus `/metrics` server
- [`requirements.txt`](requirements.txt): local Jac/Jaseci Python dependencies
- [`scripts/test_unit.sh`](scripts/test_unit.sh): unit test entrypoint
- [`scripts/test_integration.sh`](scripts/test_integration.sh): integration test entrypoint
- [`scripts/test_coverage.sh`](scripts/test_coverage.sh): coverage gate

## One-Time Setup

Create and activate a virtualenv, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional but expected for live byLLM-backed summaries:

```bash
export ANTHROPIC_API_KEY=your-key
```

Without `ANTHROPIC_API_KEY`, the app still runs. The audit summary path falls back to deterministic local text.

## Start The System

Open two terminals.

Terminal 1:

```bash
source .venv/bin/activate
python3 mock_vllm.py
```

Terminal 2:

```bash
source .venv/bin/activate
jac start main.jac
```

Default local services:

- mock metrics: `http://127.0.0.1:9000/metrics`
- Jac app: `http://127.0.0.1:8000`

## Quick Verification

Run the local checks:

```bash
make build
./scripts/test_unit.sh
./scripts/test_integration.sh
./scripts/test_coverage.sh
```

## Notes

- The system uses real-named mock vLLM metrics and a Jac-native single-entrypoint architecture.
- Generated runtime/cache artifacts such as `.jac/` and `__pycache__/` are intentionally ignored.
