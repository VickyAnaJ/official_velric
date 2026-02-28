.PHONY: build lint test test-unit test-integration test-coverage

build:
	@python3 tools/bootstrap_check.py

lint:
	@python3 -m py_compile mock_vllm.py tools/bootstrap_check.py

test:
	@./scripts/test.sh

test-unit:
	@./scripts/test_unit.sh

test-integration:
	@./scripts/test_integration.sh

test-coverage:
	@./scripts/test_coverage.sh
