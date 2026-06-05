# Changelog

All notable changes to the CrewAI Multi-Agent Book Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-06-05

### Added

- Initial project scaffolding and repository structure
- `pyproject.toml` with all dependencies and tool configurations
- `Makefile` with standard development targets
- `.env.example` with all configuration keys documented
- `.pre-commit-config.yaml` with ruff, mypy, and codespell hooks
- `.gitignore` for Python, LaTeX, IDE, and secret files
- Product Requirements Document (`docs/PRD.md`)
- Architecture and Implementation Plan (`docs/PLAN.md`)
- Master execution plan (`docs/TODO.md`)
- CLI entry point stub (`crewai-book` command)
- Complete directory skeleton for all source packages:
  - `config/` — Configuration management
  - `domain/` — Pydantic domain models
  - `sdk/` — External service wrappers
  - `services/` — Business logic
  - `agents/` — CrewAI agent definitions
  - `tools/` — Custom tool implementations
  - `workflows/` — Crew orchestration
  - `latex/` — LaTeX templates and rendering
  - `observability/` — Logging and metrics
  - `utils/` — Shared utilities
- Complete test directory structure (unit, integration, evaluation)
- Topic selected: "Multi-Agent Systems in AI: Theoretical Foundations and Modern Applications"

[Unreleased]: https://github.com/yanal/crewai-book-generator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yanal/crewai-book-generator/releases/tag/v0.1.0
