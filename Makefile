# ============================================================================
# CrewAI Multi-Agent Book Generator — Makefile
# ============================================================================
# Usage: make <target>
# Run 'make help' for a list of all available targets.
# ============================================================================

.DEFAULT_GOAL := help
SHELL := /bin/bash
PYTHON := uv run python
PIP := uv pip
PYTEST := uv run pytest
SRC_DIR := src/crewai_book
TEST_DIR := tests
OUTPUT_DIR := output

.PHONY: help install install-dev run test lint type-check format clean docs pdf check-secrets pre-commit benchmark

# ----------------------------------------------------------------------------
# Help
# ----------------------------------------------------------------------------

help: ## Show this help message
	@echo "CrewAI Multi-Agent Book Generator"
	@echo "================================="
	@echo ""
	@echo "Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ----------------------------------------------------------------------------
# Installation
# ----------------------------------------------------------------------------

install: ## Install all dependencies (production + dev)
	uv sync

install-prod: ## Install production dependencies only
	uv sync --no-dev

# ----------------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------------

run: ## Run the full book generation pipeline
	mkdir -p $(OUTPUT_DIR)/latex/figures
	$(PYTHON) scripts/generate_graph.py
	$(PYTHON) -m crewai_book run
	$(PYTHON) scripts/clean_tex.py $(OUTPUT_DIR)/latex/book.tex

# ----------------------------------------------------------------------------
# Testing
# ----------------------------------------------------------------------------

test: ## Run all tests with coverage
	$(PYTEST) $(TEST_DIR) \
		--cov=$(SRC_DIR) \
		--cov-report=term-missing \
		--cov-report=html:output/coverage \
		-v

test-unit: ## Run unit tests only
	$(PYTEST) $(TEST_DIR)/unit -v --tb=short

test-integration: ## Run integration tests only
	$(PYTEST) $(TEST_DIR)/integration -v --tb=short

test-e2e: ## Run end-to-end tests (slow)
	$(PYTEST) $(TEST_DIR)/integration/test_e2e.py -v --tb=long

test-eval: ## Run evaluation tests
	$(PYTEST) $(TEST_DIR)/evaluation -v --tb=short

# ----------------------------------------------------------------------------
# Code Quality
# ----------------------------------------------------------------------------

lint: ## Run ruff linter
	ruff check $(SRC_DIR) $(TEST_DIR)

type-check: ## Run mypy type checker
	mypy $(SRC_DIR)

format: ## Format code with ruff
	ruff check --fix $(SRC_DIR) $(TEST_DIR)
	ruff format $(SRC_DIR) $(TEST_DIR)

check-all: lint type-check test ## Run all checks (lint + type-check + test)

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------

check-secrets: ## Run gitleaks scan for secrets
	@echo "Scanning for secrets..."
	@if command -v gitleaks &> /dev/null; then \
		gitleaks detect --source . --verbose; \
	else \
		echo "gitleaks not installed. Install with: brew install gitleaks"; \
	fi

# ----------------------------------------------------------------------------
# Pre-commit
# ----------------------------------------------------------------------------

pre-commit: ## Install and run pre-commit hooks
	pre-commit install
	pre-commit run --all-files

# ----------------------------------------------------------------------------
# Documentation
# ----------------------------------------------------------------------------

docs: ## Build documentation (placeholder)
	@echo "Documentation is in docs/ directory (Markdown files)."
	@echo "View on GitHub or with a Markdown viewer."

# ----------------------------------------------------------------------------
# LaTeX / PDF
# ----------------------------------------------------------------------------

pdf: ## Compile LaTeX to PDF
	@echo "Compiling LaTeX to PDF..."
	cd $(OUTPUT_DIR)/latex && latexmk -xelatex -bibtex -interaction=nonstopmode book.tex

# ----------------------------------------------------------------------------
# Evaluation
# ----------------------------------------------------------------------------

benchmark: ## Run evaluation benchmarks
	$(PYTEST) $(TEST_DIR)/evaluation -v --tb=short -m benchmark

report: ## Generate the run evaluation report
	$(PYTHON) scripts/generate_report.py

check-citations: ## Run the citation validation script
	$(PYTHON) scripts/check_citations.py

validate-latex: ## Run the LaTeX validation script
	$(PYTHON) scripts/validate_latex.py

# ----------------------------------------------------------------------------
# Cleanup
# ----------------------------------------------------------------------------


clean: ## Remove generated artifacts and caches
	rm -rf $(OUTPUT_DIR)/latex/*.aux $(OUTPUT_DIR)/latex/*.log $(OUTPUT_DIR)/latex/*.bbl
	rm -rf $(OUTPUT_DIR)/latex/*.blg $(OUTPUT_DIR)/latex/*.toc $(OUTPUT_DIR)/latex/*.out
	rm -rf $(OUTPUT_DIR)/latex/*.fls $(OUTPUT_DIR)/latex/*.fdb_latexmk
	rm -rf $(OUTPUT_DIR)/latex/*.idx $(OUTPUT_DIR)/latex/*.ilg $(OUTPUT_DIR)/latex/*.ind
	rm -rf $(OUTPUT_DIR)/latex/*.glo $(OUTPUT_DIR)/latex/*.gls $(OUTPUT_DIR)/latex/*.glg
	rm -rf $(OUTPUT_DIR)/coverage
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned."

clean-all: clean ## Remove all generated artifacts including PDF
	rm -rf $(OUTPUT_DIR)/latex/*.pdf $(OUTPUT_DIR)/*.pdf
	@echo "Cleaned all (including PDFs)."
