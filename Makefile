.PHONY: build lint test test-unit test-integration test-coverage

build:
	@echo "No build targets yet. Add app/service build tasks as slices become WIP."

lint:
	@echo "No lint targets yet. Add per-language linters when app/service scaffolds exist."

test:
	@./scripts/test.sh

test-unit:
	@./scripts/test_unit.sh

test-integration:
	@./scripts/test_integration.sh

test-coverage:
	@./scripts/test_coverage.sh
