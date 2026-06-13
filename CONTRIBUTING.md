# Contributing to CrewAI Book Generator

First off, thank you for considering contributing to the CrewAI Book Generator project!

## Code Standards
- **PEP 8 Compliance**: All code must pass `ruff check` with zero violations. We enforce line lengths, naming conventions, and simplicity checks.
- **Type Checking**: We use strict type checking. All code must pass `mypy --strict`.
- **File Length Limits**: Following our architectural guidelines, no single python file should exceed 150 lines of code. Please modularize logic using Mixins or utility modules.
- **Test Coverage**: We enforce a strict **85%** test coverage gate. New features must be accompanied by appropriate unit or integration tests.

## Branching Strategy
1. **main**: The stable, production-ready branch.
2. **feature/***: For new features (e.g., `feature/new-agent-role`).
3. **bugfix/***: For resolving issues (e.g., `bugfix/latex-compilation-error`).

## Pull Request Process
1. Create a branch from `main`.
2. Ensure you have run `uv sync` to set up the environment.
3. Make your changes, adding tests as necessary.
4. Run the full validation suite: `make check-all` (which runs pytest, ruff, and mypy).
5. Open a Pull Request. Include a clear description of the problem solved or feature added.
6. A peer code review is required before merging.

## Development Environment Setup
See the `docs/DEVELOPER_GUIDE.md` for full setup instructions using `uv`.
