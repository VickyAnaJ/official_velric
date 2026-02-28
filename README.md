# Ops Graph Bootstrap

This repository is bootstrapped for the Jac/Jaseci-based architecture defined in
[`docs/SYSTEM_DESIGN_PLAN.md`](docs/SYSTEM_DESIGN_PLAN.md).

## Architecture Bootstrap

- `main.jac` is the canonical Jac entrypoint for backend/frontend scaffolding.
- `mock_vllm.py` serves the mock Prometheus `/metrics` endpoint used by the slices.
- `requirements.txt` declares the Jac/Jaseci runtime dependency for local setup.

## One-Time Setup

Install Jac/Jaseci into your local Python environment:

```bash
pip install -r requirements.txt
```

## Three-Command Local Flow

```bash
export ANTHROPIC_API_KEY=your-key
python3 mock_vllm.py
jac start main.jac
```

## Notes

- The mock vLLM server is intentionally lightweight and uses real metric names sourced from `docs/external_apis.md/vLLM.md`.
- The Jac app is currently a Step 3.0 architecture skeleton. Slice logic should be added through the workflow, starting from a corrected Step 3.0 baseline.
