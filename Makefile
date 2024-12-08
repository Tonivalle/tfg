SRC_DIR	= src
TEST_DIR = tests
CHECK_DIRS = $(SRC_DIR) $(TEST_DIR)
PYTEST_FLAGS = -vv

.PHONY: check ## Launch all the checks (formatting, linting, type checking)
check: format-check lint type-check test 

.PHONY: format
format: ## Format repository code
	poetry run ruff format
	poetry run ruff check --select I001 --fix

.PHONY: format-check
format-check: ## Check the code format with no actual side effects
	poetry run ruff format --check
	poetry run ruff check --select I001

.PHONY: install
install: ## Install the dependencies from the lock file
	poetry run pip install --upgrade pip
	poetry install -v

.PHONY: lint
lint: ## Launch the linting tool
	poetry run ruff check

.PHONY: test
test: 
	poetry run pytest $(PYTEST_FLAGS) $(TEST_DIR)

.PHONY: type-check
type-check: ## Launch the type checking tool
	poetry run mypy $(CHECK_DIRS)

.PHONY: update
update: ## Update python dependencies
	poetry update

.PHONY: run
run: ## Run streamlit app
	poetry run streamlit run ./src/tfg/frontend/main.py

.PHONY: help
help: ## Show the available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'