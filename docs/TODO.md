# TODO.md — Master Execution Plan
## CrewAI Multi-Agent LaTeX Book/Article Generator
### Version 1.0.0 | Status: Active | Classification: Master Planning Document

---

> **This document is the single source of truth for the entire project.**
> Every task, dependency, acceptance criterion, and definition of done is recorded here.
> No implementation decision should be made without consulting this document.

---

## Table of Contents

1. [Executive Overview](#1-executive-overview)
2. [Requirements Analysis](#2-requirements-analysis)
3. [Project Architecture Planning](#3-project-architecture-planning)
4. [CrewAI System Design](#4-crewai-system-design)
5. [Workflow Design](#5-workflow-design)
6. [Topic Selection Framework](#6-topic-selection-framework)
7. [LaTeX System Design](#7-latex-system-design)
8. [Research and Content Pipeline](#8-research-and-content-pipeline)
9. [Testing Strategy](#9-testing-strategy)
10. [Documentation Requirements](#10-documentation-requirements)
11. [Research and Evaluation Section](#11-research-and-evaluation-section)
12. [Project Timeline](#12-project-timeline)
13. [Definition of Done](#13-definition-of-done)
14. [Excellence Beyond Requirements](#14-excellence-beyond-requirements)

---

## 1. Executive Overview

### 1.1 Project Objective

Design, architect, implement, test, document, and deliver a **production-grade multi-agent AI system** powered by **CrewAI** that autonomously generates a professional, publication-quality article or small book on a selected topic. The system must produce a fully formatted **PDF document** compiled from **LaTeX** source, backed by verified citations, multi-pass editorial review, and a reproducible software pipeline meeting the highest engineering standards.

The project simultaneously satisfies:
- All homework specification requirements (CrewAI, LaTeX, multi-agent collaboration, PDF output).
- All software engineering guidelines (architecture, testing, documentation, security, observability).
- The aspirational goal of producing the **best possible submission** that impresses instructors and reviewers beyond all peer work.

### 1.2 Success Criteria

| ID | Criterion | Measurement |
|----|-----------|-------------|
| SC-01 | System uses CrewAI framework | CrewAI version pinned in `pyproject.toml`; at least 6 distinct agents active |
| SC-02 | LaTeX document compiles without errors | `pdflatex` / `latexmk` exits with code 0 |
| SC-03 | Multiple collaborating agents | Minimum 8 agents with distinct roles and measurable handoffs |
| SC-04 | Professional PDF output | ≥20 pages, structured chapters, bibliography, index, glossary |
| SC-05 | All tests pass | `pytest` exits with code 0; coverage ≥85% |
| SC-06 | Documentation complete | All required `.md` files present, spell-checked, and cross-referenced |
| SC-07 | Reproducibility | Running `make run` twice produces semantically equivalent output |
| SC-08 | Citation integrity | 100% of cited sources are real, accessible, and correctly formatted |
| SC-09 | Engineering compliance | All guideline checklist items verified |
| SC-10 | Submission package complete | All deliverables present in submission archive |

### 1.3 Expected Deliverables

```
Deliverable D-01: Full Python project repository (source code)
Deliverable D-02: Generated LaTeX source tree (output/latex/)
Deliverable D-03: Compiled professional PDF (output/article.pdf or output/book.pdf)
Deliverable D-04: Bibliography file (output/references.bib)
Deliverable D-05: README.md (project overview and quickstart)
Deliverable D-06: docs/PRD.md (Product Requirements Document)
Deliverable D-07: docs/PLAN.md (Architectural Plan)
Deliverable D-08: docs/TODO.md (this document, kept current)
Deliverable D-09: docs/ARCHITECTURE.md (system architecture with diagrams)
Deliverable D-10: docs/RESEARCH.md (research methodology and results)
Deliverable D-11: docs/USER_GUIDE.md (end-user instructions)
Deliverable D-12: docs/DEVELOPER_GUIDE.md (developer instructions)
Deliverable D-13: tests/ (complete test suite with coverage report)
Deliverable D-14: evaluation/ (benchmarks, metrics, experiments)
Deliverable D-15: Submission archive (.zip or .tar.gz)
```

### 1.4 Definition of Project Completion

The project is **complete** when and only when:

1. All 15 deliverables above exist and are non-empty and valid.
2. `make install && make run` completes without error on a clean environment.
3. `make test` passes with coverage ≥85%.
4. `make lint` passes with zero errors.
5. The PDF compiles and is readable.
6. Every requirement in Section 2 is marked `[VERIFIED]`.
7. Every item in Section 13 (Definition of Done) is satisfied.
8. A final peer-review checklist has been signed off.

---

## 2. Requirements Analysis

### 2.1 Functional Requirements

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| FR-01 | System must use the CrewAI framework as its orchestration backbone | Homework Spec | CRITICAL | Import statement; `crewai` in `pyproject.toml` |
| FR-02 | System must employ multiple AI agents with distinct, non-overlapping roles | Homework Spec | CRITICAL | Agent registry; role audit log |
| FR-03 | Agents must collaborate and pass context between one another | Homework Spec | CRITICAL | Context passing integration test |
| FR-04 | System must generate a professional article or small book | Homework Spec | CRITICAL | PDF ≥20 pages, structured, readable |
| FR-05 | Document must be produced using LaTeX | Homework Spec | CRITICAL | LaTeX source files present; pdflatex compilation passes |
| FR-06 | Output must be a professional PDF document | Homework Spec | CRITICAL | PDF renders correctly in viewer |
| FR-07 | Topic must be of our choice and demonstrate depth | Homework Spec | HIGH | Topic evaluation score ≥4/5 on all axes |
| FR-08 | Agents must perform research on the selected topic | Implicit | HIGH | Research agent produces ≥15 verified sources |
| FR-09 | System must generate citations and a bibliography | Implicit | HIGH | `.bib` file present; all in-text citations resolve |
| FR-10 | Content must be factually accurate and verified | Guideline | HIGH | Fact-check agent audit log with zero unresolved flags |
| FR-11 | System must log all agent activities | Guideline | HIGH | Structured log file with per-agent entries |
| FR-12 | System must handle and recover from failures gracefully | Guideline | HIGH | Error recovery integration test passes |
| FR-13 | System must produce reproducible output | Guideline | MEDIUM | Two sequential runs produce structurally identical PDF |
| FR-14 | System must provide a CLI entry point | Guideline | MEDIUM | `python -m crewai_book --help` works |
| FR-15 | System must support configurable topics via config file or CLI | Guideline | MEDIUM | Topic changed via config without code change |

### 2.2 Non-Functional Requirements

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| NFR-01 | Code must be PEP 8 compliant | Guideline | HIGH | `ruff check` exits 0 |
| NFR-02 | Type annotations on all public functions | Guideline | HIGH | `mypy --strict` passes |
| NFR-03 | Docstrings on all modules, classes, and public methods | Guideline | HIGH | `pydocstyle` passes |
| NFR-04 | No hardcoded secrets or API keys in source | Guideline / Security | CRITICAL | `gitleaks` scan clean; `.env` in `.gitignore` |
| NFR-05 | All configuration via environment variables or config files | Guideline | HIGH | `grep -r "sk-" src/` returns nothing |
| NFR-06 | System must be installable in a clean virtualenv | Guideline | CRITICAL | Fresh venv install test passes |
| NFR-07 | Dependencies pinned with exact versions | Guideline | HIGH | `pyproject.toml` and `requirements.lock` present |
| NFR-08 | Logging must be structured (JSON) and leveled | Guideline | MEDIUM | Log output parseable by `jq` |
| NFR-09 | Runtime for full pipeline ≤30 minutes on standard hardware | Implicit | MEDIUM | Timing benchmark recorded |
| NFR-10 | Memory usage reasonable; no unbounded context accumulation | Guideline | MEDIUM | Memory profiling report present |
| NFR-11 | Code coverage ≥85% | Guideline | HIGH | `pytest --cov` report shows ≥85% |
| NFR-12 | All commits must have meaningful messages following Conventional Commits | Guideline | MEDIUM | Git log audit |
| NFR-13 | Git history must be clean; no merge conflicts or WIP commits in main | Guideline | MEDIUM | `git log --oneline` review |
| NFR-14 | CHANGELOG.md maintained with semantic versioning | Guideline | MEDIUM | File present and non-empty |
| NFR-15 | Project must work on Linux and macOS | Guideline | MEDIUM | CI matrix includes both |

### 2.3 Technical Requirements

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| TR-01 | Python ≥3.11 | Guideline | CRITICAL | `python_requires` in `pyproject.toml` |
| TR-02 | CrewAI ≥0.28 (latest stable) | Homework Spec | CRITICAL | Version in `pyproject.toml` |
| TR-03 | LaTeX distribution available (TeX Live or MiKTeX) | Homework Spec | CRITICAL | `latexmk --version` in CI passes |
| TR-04 | All agents must be individually testable in isolation | Guideline | HIGH | Unit tests per agent pass independently |
| TR-05 | Configuration via Pydantic BaseSettings models | Guideline | HIGH | Config model present with validators |
| TR-06 | SDK/Service/Domain layer separation | Guideline | HIGH | Architecture review passes |
| TR-07 | Dependency injection for all external services | Guideline | MEDIUM | No global state; services injected into agents |
| TR-08 | Async-capable where beneficial | Guideline | MEDIUM | Async pipeline where I/O bound |
| TR-09 | All file I/O uses `pathlib.Path` | Guideline | MEDIUM | `grep -r "open(" src/` audit |
| TR-10 | Environment managed via `python-dotenv` and `.env` file | Guideline | HIGH | `.env.example` present with all keys |
| TR-11 | Makefile with standard targets | Guideline | HIGH | `make help` lists all targets |
| TR-12 | `pyproject.toml` as single build configuration | Guideline | HIGH | No `setup.py`; no `setup.cfg` |
| TR-13 | Pre-commit hooks configured | Guideline | MEDIUM | `.pre-commit-config.yaml` present |
| TR-14 | GitHub Actions CI pipeline | Guideline | MEDIUM | `.github/workflows/ci.yml` present |

### 2.4 Documentation Requirements

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| DR-01 | README.md with overview, quickstart, and architecture summary | Guideline | CRITICAL | File present; renders on GitHub |
| DR-02 | docs/PRD.md (Product Requirements Document) | Guideline | CRITICAL | File present and complete |
| DR-03 | docs/PLAN.md (Architecture and Implementation Plan) | Guideline | CRITICAL | File present and complete |
| DR-04 | docs/TODO.md (this file; kept updated throughout) | Guideline | CRITICAL | File present; reflects current state |
| DR-05 | docs/ARCHITECTURE.md with Mermaid or ASCII diagrams | Guideline | HIGH | Diagrams render; cover all layers |
| DR-06 | docs/RESEARCH.md with research methodology | Guideline | HIGH | File present; includes metrics |
| DR-07 | docs/USER_GUIDE.md | Guideline | HIGH | Step-by-step instructions verified |
| DR-08 | docs/DEVELOPER_GUIDE.md | Guideline | HIGH | Setup, extension, contribution guide |
| DR-09 | Inline docstrings on all public APIs | Guideline | HIGH | `pydocstyle` passes |
| DR-10 | CHANGELOG.md with semantic versioning | Guideline | MEDIUM | File present and structured |
| DR-11 | docs/agents/README.md per-agent documentation | Guideline | MEDIUM | One file per agent |
| DR-12 | Additional PRD for each major mechanism (Research, LaTeX, PDF) | Guideline | MEDIUM | Files present |

### 2.5 Testing Requirements

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| TST-01 | Unit tests for every agent | Guideline | CRITICAL | Test files per agent; all pass |
| TST-02 | Unit tests for all tools | Guideline | CRITICAL | Tool test files; all pass |
| TST-03 | Integration test: full pipeline end-to-end | Guideline | CRITICAL | `test_e2e.py` passes |
| TST-04 | Integration test: LaTeX compilation | Guideline | HIGH | LaTeX test generates valid PDF |
| TST-05 | Integration test: citation pipeline | Guideline | HIGH | All citations resolve |
| TST-06 | Integration test: error recovery | Guideline | HIGH | Simulated failures trigger retry |
| TST-07 | Configuration validation tests | Guideline | HIGH | Invalid configs rejected cleanly |
| TST-08 | Coverage ≥85% | Guideline | HIGH | `pytest --cov` report |
| TST-09 | Performance/timing benchmarks | Guideline | MEDIUM | Benchmark results logged |
| TST-10 | Content quality evaluation | Guideline | MEDIUM | Readability score computed |

### 2.6 Research Requirements

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| RR-01 | ≥15 real, verifiable academic or professional sources | Implicit | HIGH | Sources list in RESEARCH.md |
| RR-02 | All sources accessible via URL or DOI | Implicit | HIGH | URL/DOI check script passes |
| RR-03 | Citation format: BibTeX | Homework Spec | HIGH | `.bib` file valid |
| RR-04 | No hallucinated citations | Guideline | CRITICAL | Fact-check agent audit |
| RR-05 | Research agent documents its search strategy | Guideline | MEDIUM | Search log present |
| RR-06 | Comparative evaluation: agent vs baseline | Guideline | MEDIUM | RESEARCH.md section present |

### 2.7 Submission Requirements

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| SR-01 | All source code in repository | Homework Spec | CRITICAL | `git status` clean |
| SR-02 | Generated PDF included in submission | Homework Spec | CRITICAL | `output/` directory contains PDF |
| SR-03 | LaTeX source included | Homework Spec | HIGH | `output/latex/` present |
| SR-04 | All documentation included | Guideline | HIGH | `docs/` directory complete |
| SR-05 | Installation instructions work on clean machine | Guideline | CRITICAL | Tested in fresh virtualenv |
| SR-06 | Submission archive well-organized | Guideline | HIGH | Archive structure matches spec |

---

## 3. Project Architecture Planning

### 3.1 Repository Structure

**Task ARCH-01: Define and Create Repository Layout**

```
crewai-book-generator/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # Main CI pipeline
│   │   └── release.yml             # Release automation
│   └── PULL_REQUEST_TEMPLATE.md
├── .pre-commit-config.yaml         # Pre-commit hooks (ruff, mypy, etc.)
├── .env.example                    # All required env vars documented
├── .gitignore                      # Python, LaTeX, IDE, secrets
├── Makefile                        # Standard targets
├── pyproject.toml                  # Single build config
├── README.md                       # Project overview
├── CHANGELOG.md                    # Semantic versioned changelog
├── docs/
│   ├── TODO.md                     # This file
│   ├── PRD.md
│   ├── PLAN.md
│   ├── ARCHITECTURE.md
│   ├── RESEARCH.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   ├── agents/                     # Per-agent documentation
│   │   ├── research_agent.md
│   │   ├── fact_verification_agent.md
│   │   ├── outline_architect_agent.md
│   │   ├── writer_agent.md
│   │   ├── editor_agent.md
│   │   ├── reviewer_agent.md
│   │   ├── citation_agent.md
│   │   ├── latex_formatter_agent.md
│   │   ├── pdf_production_agent.md
│   │   └── qa_agent.md
│   └── prds/
│       ├── PRD_research_pipeline.md
│       ├── PRD_latex_system.md
│       └── PRD_pdf_production.md
├── src/
│   └── crewai_book/
│       ├── __init__.py
│       ├── __main__.py             # CLI entry point
│       ├── version.py              # Single version source
│       ├── config/                 # Configuration layer
│       │   ├── __init__.py
│       │   ├── settings.py         # Pydantic BaseSettings
│       │   └── agent_configs.py    # Agent role/goal/backstory configs
│       ├── domain/                 # Domain models
│       │   ├── __init__.py
│       │   ├── article.py          # Article, Chapter, Section models
│       │   ├── citation.py         # Source, Citation, Bibliography models
│       │   ├── agent_output.py     # Typed agent output models
│       │   └── pipeline_state.py   # Pipeline state machine
│       ├── sdk/                    # External service wrappers
│       │   ├── __init__.py
│       │   ├── llm_client.py       # LLM provider abstraction
│       │   ├── search_client.py    # Web/academic search abstraction
│       │   └── latex_client.py     # LaTeX compilation abstraction
│       ├── services/               # Business logic services
│       │   ├── __init__.py
│       │   ├── research_service.py
│       │   ├── citation_service.py
│       │   ├── content_service.py
│       │   ├── latex_service.py
│       │   └── pdf_service.py
│       ├── agents/                 # CrewAI agent definitions
│       │   ├── __init__.py
│       │   ├── base_agent.py       # Shared base configuration
│       │   ├── research_agent.py
│       │   ├── fact_verification_agent.py
│       │   ├── outline_architect_agent.py
│       │   ├── writer_agent.py
│       │   ├── editor_agent.py
│       │   ├── reviewer_agent.py
│       │   ├── citation_agent.py
│       │   ├── latex_formatter_agent.py
│       │   ├── pdf_production_agent.py
│       │   └── qa_agent.py
│       ├── tools/                  # CrewAI custom tools
│       │   ├── __init__.py
│       │   ├── web_search_tool.py
│       │   ├── arxiv_tool.py
│       │   ├── citation_validator_tool.py
│       │   ├── latex_compiler_tool.py
│       │   ├── readability_scorer_tool.py
│       │   └── fact_check_tool.py
│       ├── workflows/              # Crew definitions and orchestration
│       │   ├── __init__.py
│       │   ├── main_crew.py        # Primary Crew definition
│       │   ├── research_crew.py    # Research sub-crew
│       │   └── editorial_crew.py   # Editorial sub-crew
│       ├── latex/                  # LaTeX templates and utilities
│       │   ├── __init__.py
│       │   ├── templates/
│       │   │   ├── book.tex.j2     # Jinja2 book template
│       │   │   ├── article.tex.j2  # Jinja2 article template
│       │   │   └── preamble.tex    # Shared LaTeX preamble
│       │   └── renderer.py        # Template rendering engine
│       ├── observability/          # Logging, metrics, tracing
│       │   ├── __init__.py
│       │   ├── logger.py           # Structured JSON logger
│       │   ├── metrics.py          # Runtime metrics collector
│       │   └── agent_tracker.py    # Per-agent activity tracker
│       └── utils/                  # Shared utilities
│           ├── __init__.py
│           ├── text_utils.py
│           ├── file_utils.py
│           └── validation_utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Fixtures, mocks, test config
│   ├── unit/
│   │   ├── agents/                 # Per-agent unit tests
│   │   ├── tools/                  # Per-tool unit tests
│   │   ├── services/               # Per-service unit tests
│   │   ├── domain/                 # Domain model tests
│   │   └── config/                 # Configuration tests
│   ├── integration/
│   │   ├── test_research_pipeline.py
│   │   ├── test_latex_pipeline.py
│   │   ├── test_citation_pipeline.py
│   │   ├── test_error_recovery.py
│   │   └── test_e2e.py
│   └── evaluation/
│       ├── test_content_quality.py
│       ├── test_citation_quality.py
│       └── test_reproducibility.py
├── evaluation/                     # Benchmarks and experiments
│   ├── experiments/
│   ├── results/
│   └── reports/
├── output/                         # Generated artifacts (gitignored except PDF)
│   ├── latex/
│   └── .gitkeep
└── scripts/                        # Utility scripts
    ├── check_citations.py
    ├── validate_latex.py
    └── generate_report.py
```

**Dependencies:** None (first task)
**Completion Criteria:** Directory structure created; all `__init__.py` files contain module docstrings; `git init` done; first commit pushed.

---

### 3.2 Package Structure

**Task ARCH-02: Configure `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "crewai-book-generator"
version = "0.1.0"
description = "Multi-agent LaTeX book/article generator powered by CrewAI"
requires-python = ">=3.11"
dependencies = [
    "crewai>=0.28",
    "crewai-tools>=0.1",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "python-dotenv>=1.0",
    "jinja2>=3.1",
    "httpx>=0.25",
    "rich>=13.0",
    "typer>=0.9",
    "loguru>=0.7",
    "textstat>=0.7",
    "bibtexparser>=1.4",
    "arxiv>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-cov>=4.1",
    "pytest-asyncio>=0.21",
    "pytest-mock>=3.12",
    "ruff>=0.1",
    "mypy>=1.7",
    "pydocstyle>=6.3",
    "pre-commit>=3.5",
    "gitleaks",
]

[project.scripts]
crewai-book = "crewai_book.__main__:app"
```

**Completion Criteria:** `pip install -e ".[dev]"` succeeds in a fresh virtualenv.

---

### 3.3 Makefile Targets

**Task ARCH-03: Create Makefile with All Standard Targets**

```makefile
.PHONY: help install run test lint type-check format clean docs pdf

help:          ## Show this help
install:       ## Install all dependencies
run:           ## Run the full pipeline
test:          ## Run all tests with coverage
lint:          ## Run ruff linter
type-check:    ## Run mypy
format:        ## Format code with ruff
clean:         ## Remove generated artifacts
docs:          ## Build documentation
pdf:           ## Compile LaTeX to PDF
check-secrets: ## Run gitleaks scan
pre-commit:    ## Install and run pre-commit hooks
benchmark:     ## Run evaluation benchmarks
```

**Completion Criteria:** All targets execute; `make help` displays all targets.

---

### 3.4 Layer Architecture Design

**Task ARCH-04: Implement SDK Layer**

The SDK layer wraps all external services with a stable interface. No other layer may import from external libraries directly.

- `LLMClient`: wraps OpenAI / Anthropic / local LLM, returns typed responses.
- `SearchClient`: wraps Serper / DuckDuckGo / ArXiv APIs with rate limiting.
- `LaTeXClient`: wraps subprocess calls to `latexmk`/`pdflatex` with timeout and error capture.

Every SDK class must:
- Accept configuration via injected `Settings` object.
- Implement `__repr__` for debugging.
- Have a corresponding mock in `tests/conftest.py`.
- Raise only domain-specific exceptions (not raw HTTP or OS errors).

---

**Task ARCH-05: Implement Domain Layer**

Pydantic v2 models for all business entities:

```python
class Section(BaseModel):
    title: str
    content: str
    word_count: int
    citations: list[CitationRef]

class Chapter(BaseModel):
    number: int
    title: str
    sections: list[Section]
    chapter_summary: str

class Article(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    chapters: list[Chapter]
    bibliography: Bibliography
    metadata: ArticleMetadata

class PipelineState(BaseModel):
    stage: PipelineStage
    article: Article | None
    errors: list[PipelineError]
    retry_count: int
    start_time: datetime
```

---

**Task ARCH-06: Implement Service Layer**

Services contain all business logic. They are injected into agents via CrewAI tool wrappers.

- `ResearchService`: orchestrates searches, deduplicates, scores relevance.
- `CitationService`: validates, formats, and cross-references citations.
- `ContentService`: manages article assembly, word count, readability.
- `LaTeXService`: renders Jinja2 templates into `.tex` files.
- `PDFService`: triggers LaTeX compilation; captures and reports errors.

---

**Task ARCH-07: Configuration Management**

```python
class Settings(BaseSettings):
    # LLM
    openai_api_key: SecretStr
    openai_model: str = "gpt-4o"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 4096

    # Search
    serper_api_key: SecretStr | None = None
    max_search_results: int = 10
    max_sources: int = 30

    # Pipeline
    topic: str
    output_dir: Path = Path("output")
    latex_dir: Path = Path("output/latex")
    document_type: Literal["article", "book"] = "book"
    target_word_count: int = 15000
    max_retries: int = 3

    # Quality gates
    min_readability_score: float = 60.0
    min_citation_count: int = 15
    min_pages: int = 20

    model_config = SettingsConfigDict(env_file=".env")
```

---

**Task ARCH-08: Logging and Observability**

- Structured JSON logging via `loguru` with configurable level.
- Each log entry includes: `timestamp`, `level`, `agent_name`, `task_id`, `message`, `metadata`.
- Per-agent activity log: inputs received, outputs produced, tools called, duration.
- Pipeline metrics: total tokens used, total cost estimate, wall-clock time per stage.
- `AgentTracker` class records all agent invocations for post-run analysis.
- Logs written to `output/logs/run_{timestamp}.jsonl`.

---

**Task ARCH-09: Error Handling Strategy**

```
Exception Hierarchy:
  CrewBookError (base)
  ├── ConfigurationError
  ├── ResearchError
  │   ├── SearchError
  │   └── CitationValidationError
  ├── ContentError
  │   ├── HallucinationDetectedError
  │   └── QualityGateError
  ├── LaTeXError
  │   ├── CompilationError
  │   └── TemplateRenderError
  └── PipelineError
      ├── AgentFailureError
      └── RetryExhaustedError
```

All exceptions include: `message`, `context: dict`, `recoverable: bool`, `stage: PipelineStage`.
Recoverable errors trigger automatic retry with exponential backoff (max 3 attempts).
Non-recoverable errors are logged and surfaced with actionable resolution guidance.

---

**Task ARCH-10: Security Requirements**

- [ ] `.env` in `.gitignore`; verified before first commit.
- [ ] `.env.example` contains all keys with placeholder values and descriptions.
- [ ] `gitleaks` pre-commit hook configured.
- [ ] `SecretStr` used for all API keys in Settings.
- [ ] No `print()` of secrets anywhere in code.
- [ ] HTTP clients configured with timeouts; no unbounded requests.
- [ ] Input sanitization before LaTeX rendering (escape special characters).
- [ ] Security scan result documented in `docs/SECURITY.md`.

---

**Task ARCH-11: Version Management**

- Single version source: `src/crewai_book/version.py` → `__version__ = "0.1.0"`.
- `pyproject.toml` reads from `version.py` via `hatch-vcs` or manual sync.
- Semantic versioning: `MAJOR.MINOR.PATCH`.
- CHANGELOG.md updated on every version bump.
- Git tags: `v0.1.0` on release.

---

## 4. CrewAI System Design

### 4.1 Agent Architecture Overview

The system uses a **hierarchical crew** composed of two sub-crews:

```
MAIN CREW (Manager LLM orchestrates)
├── RESEARCH SUB-CREW
│   ├── Research Agent
│   ├── Fact Verification Agent
│   └── Citation Agent
└── EDITORIAL SUB-CREW
    ├── Outline Architect Agent
    ├── Writer Agent
    ├── Editor Agent
    ├── Reviewer Agent
    ├── LaTeX Formatter Agent
    ├── PDF Production Agent
    └── Quality Assurance Agent
```

### 4.2 Agent Definitions

---

#### Agent A-01: Research Agent

**Task: Define Research Agent**

| Field | Value |
|-------|-------|
| **Role** | Senior Research Scientist |
| **Goal** | Discover, collect, and organize the most relevant, authoritative, and up-to-date sources on the assigned topic. Produce a structured research corpus with at least 20 verified sources. |
| **Backstory** | A seasoned academic researcher with 15 years of experience conducting literature reviews across scientific disciplines. Expert in identifying primary sources, evaluating source credibility, and synthesizing research into coherent knowledge structures. Has published in top-tier journals and understands the difference between a citation that adds value and one that merely pads a bibliography. |
| **Inputs** | Topic string; optional seed keywords; target audience description |
| **Outputs** | Structured source list (title, authors, year, URL/DOI, abstract, relevance score, credibility score); grouped by subtopic |
| **Tools** | `WebSearchTool`, `ArXivTool`, `CitationValidatorTool`, `ReadabilityScoreTool` |
| **Memory** | Short-term (within crew run); entity memory for source deduplication |
| **Quality Metrics** | ≥20 sources; all sources have URL/DOI; relevance score >0.7 for all included; no duplicates; ≥5 academic sources |
| **Max Iterations** | 5 |
| **Verbose** | True (logged) |

**Planning Sub-tasks:**
- [ ] Write agent role/goal/backstory strings in `config/agent_configs.py`
- [ ] Define agent in `agents/research_agent.py` with injected tools
- [ ] Write unit tests: mock search tools, assert output structure
- [ ] Write `docs/agents/research_agent.md`
- [ ] Define quality metric evaluation function

---

#### Agent A-02: Fact Verification Agent

**Task: Define Fact Verification Agent**

| Field | Value |
|-------|-------|
| **Role** | Critical Fact Checker and Accuracy Auditor |
| **Goal** | Verify every factual claim in the research corpus. Flag unverifiable claims, detect hallucinations, and assign a confidence score to each fact. Produce a verified-facts report with zero unresolved critical flags. |
| **Backstory** | A former investigative journalist turned AI safety researcher. Has developed systematic methodologies for verifying AI-generated content against primary sources. Deeply skeptical of any claim that cannot be traced to a citable, accessible source. Known for catching subtle inaccuracies that others miss. |
| **Inputs** | Research corpus from Research Agent; list of key claims extracted |
| **Outputs** | Verified facts list with confidence scores; flagged claims list; hallucination report; recommended source additions |
| **Tools** | `WebSearchTool`, `CitationValidatorTool`, `FactCheckTool` |
| **Memory** | Short-term; access to Research Agent outputs |
| **Quality Metrics** | 100% of claims checked; confidence score assigned to each; zero HIGH-severity unresolved flags |
| **Max Iterations** | 3 |

**Planning Sub-tasks:**
- [ ] Design hallucination detection heuristics (cross-reference, date validation, author verification)
- [ ] Implement `FactCheckTool` that queries multiple sources for a claim
- [ ] Define confidence scoring rubric (0.0–1.0 scale with tier labels)
- [ ] Write unit tests with known hallucinations as test cases

---

#### Agent A-03: Outline Architect Agent

**Task: Define Outline Architect Agent**

| Field | Value |
|-------|-------|
| **Role** | Senior Technical Author and Information Architect |
| **Goal** | Design the complete hierarchical structure of the book/article. Create a compelling, logically sequenced outline with clear chapter arcs, section objectives, and estimated word counts. The outline must serve as a complete blueprint that a writer can execute without ambiguity. |
| **Backstory** | A technical author who has structured documentation for major open-source projects and written three published technical books. Expert in information architecture, progressive disclosure, and narrative flow in technical writing. Believes that a great outline is 80% of a great book. |
| **Inputs** | Verified research corpus; topic; target audience; document type (article/book); target word count |
| **Outputs** | Structured outline: title, abstract template, chapter list with section breakdown, estimated word counts, transition summaries, key points per section |
| **Tools** | None (reasoning-only agent) |
| **Memory** | Short-term; access to research corpus |
| **Quality Metrics** | All chapters have ≥3 sections; total estimated word count within 10% of target; logical narrative progression; no orphaned sections |
| **Max Iterations** | 2 |

---

#### Agent A-04: Writer Agent

**Task: Define Writer Agent**

| Field | Value |
|-------|-------|
| **Role** | Expert Technical Writer and Science Communicator |
| **Goal** | Transform the approved outline and research corpus into compelling, accurate, well-structured prose. Write each chapter and section to the specified depth, incorporating citations naturally, maintaining consistent voice and terminology throughout. |
| **Backstory** | A science communicator with a PhD in the relevant field, who has spent a decade making complex technical content accessible to educated non-specialists. Writes with precision and clarity, never sacrificing accuracy for readability. Has a gift for finding the perfect analogy and the right level of abstraction for the target audience. |
| **Inputs** | Approved outline; verified research corpus with citations; writing style guide; target audience profile |
| **Outputs** | Full manuscript: all chapters written in Markdown with in-text citation markers; word count per section; readability scores |
| **Tools** | `ReadabilityScoreTool` |
| **Memory** | Long-term (to maintain consistency across chapters); entity memory for defined terms |
| **Quality Metrics** | Word count within 5% of target per section; readability score ≥60 (Flesch-Kincaid); all key outline points addressed; no orphaned citation markers |
| **Max Iterations** | 3 per chapter |

---

#### Agent A-05: Editor Agent

**Task: Define Editor Agent**

| Field | Value |
|-------|-------|
| **Role** | Senior Copy Editor and Style Guardian |
| **Goal** | Perform a thorough editorial pass on the complete manuscript. Correct grammar, improve clarity, ensure consistent terminology, eliminate redundancy, strengthen transitions, and ensure the document reads as a unified whole rather than a collection of independently written sections. |
| **Backstory** | A professional editor with 20 years of experience at academic and technical publishers. Has developed an instinct for the exact word, the cleaner sentence, and the structural shift that makes a paragraph land. Respects the author's voice while ruthlessly improving it. |
| **Inputs** | Full manuscript from Writer Agent; style guide; glossary of defined terms |
| **Outputs** | Edited manuscript with tracked changes (diff); list of major editorial decisions; updated glossary; readability improvement metrics |
| **Tools** | `ReadabilityScoreTool` |
| **Memory** | Short-term |
| **Quality Metrics** | Readability score improvement ≥5 points; zero grammatical errors (sampled check); consistent terminology throughout |
| **Max Iterations** | 2 |

---

#### Agent A-06: Reviewer Agent

**Task: Define Reviewer Agent**

| Field | Value |
|-------|-------|
| **Role** | Peer Reviewer and Subject Matter Expert |
| **Goal** | Conduct a rigorous peer review of the manuscript as if reviewing for a top academic or technical publication. Identify logical errors, missing arguments, unsupported claims, structural weaknesses, and opportunities to strengthen the contribution. |
| **Backstory** | A prolific academic who has reviewed hundreds of papers for top journals. Known for constructive, thorough reviews that always improve the final product. Holds the work to a high standard but provides actionable, specific feedback rather than vague criticism. |
| **Inputs** | Edited manuscript; verified research corpus; review rubric |
| **Outputs** | Structured review report: major concerns (must fix), minor concerns (should fix), suggestions (consider); verdict: accept/revise/reject; specific line-level feedback |
| **Tools** | `CitationValidatorTool`, `FactCheckTool` |
| **Memory** | Short-term |
| **Quality Metrics** | Review report addresses all major sections; zero unaddressed major concerns before proceeding; review references specific page/section locations |
| **Max Iterations** | 2 |

---

#### Agent A-07: Citation Agent

**Task: Define Citation Agent**

| Field | Value |
|-------|-------|
| **Role** | Bibliographer and Citation Management Specialist |
| **Goal** | Audit, validate, and format all citations in the manuscript. Produce a clean, complete BibTeX bibliography file. Ensure every in-text citation has a corresponding bibliography entry and vice versa. Detect and report any hallucinated or incorrectly attributed citations. |
| **Backstory** | A research librarian with deep expertise in academic citation standards, BibTeX formatting, and digital object identifiers. Has rescued multiple dissertations from citation disasters. Perfectionist about bibliography consistency and completeness. |
| **Inputs** | Edited manuscript with citation markers; research corpus with source metadata |
| **Outputs** | Clean `.bib` file; citation audit report (matched/unmatched/invalid); updated manuscript with corrected citation keys; citation statistics |
| **Tools** | `CitationValidatorTool`, `WebSearchTool` |
| **Memory** | Short-term |
| **Quality Metrics** | 100% citation match rate; zero hallucinated citations; all DOIs verified; BibTeX validates without errors |
| **Max Iterations** | 3 |

---

#### Agent A-08: LaTeX Formatter Agent

**Task: Define LaTeX Formatter Agent**

| Field | Value |
|-------|-------|
| **Role** | LaTeX Typesetting Specialist |
| **Goal** | Transform the validated manuscript and bibliography into professional, compilable LaTeX source code. Apply the selected template, structure chapters and sections correctly, insert citations, format tables and figures, and produce a LaTeX document that compiles without errors on the first attempt. |
| **Backstory** | A computational scientist who has typeset dozens of journal articles, conference papers, and technical reports in LaTeX. Knows every package, every escape sequence, and every edge case. Takes personal pride in producing LaTeX that compiles cleanly and renders beautifully. |
| **Inputs** | Final edited manuscript; `.bib` file; LaTeX template; figure specifications; table data |
| **Outputs** | Complete LaTeX source tree: main `.tex` file, chapter files, preamble, bibliography file; compilation log (must show success) |
| **Tools** | `LaTeXCompilerTool` |
| **Memory** | Short-term |
| **Quality Metrics** | LaTeX compiles without errors; all citations render; no overfull hboxes; PDF output ≥20 pages; visual inspection passes |
| **Max Iterations** | 5 (iterative compilation fixing) |

---

#### Agent A-09: PDF Production Agent

**Task: Define PDF Production Agent**

| Field | Value |
|-------|-------|
| **Role** | Document Production and Quality Control Specialist |
| **Goal** | Execute the final LaTeX compilation pipeline, optimize the PDF, verify all elements render correctly, and produce the submission-ready PDF document. |
| **Backstory** | A publishing house production manager who has overseen the final output of thousands of professional documents. Expert in the entire LaTeX-to-PDF pipeline, PDF optimization, and pre-press quality control. Nothing ships without passing production QC. |
| **Inputs** | Validated LaTeX source tree from LaTeX Formatter Agent |
| **Outputs** | Final `article.pdf` or `book.pdf`; compilation log; PDF metadata; page count; file size |
| **Tools** | `LaTeXCompilerTool` |
| **Memory** | Short-term |
| **Quality Metrics** | PDF compiles successfully; all pages render; TOC links work; bibliography complete; file ≤50MB |
| **Max Iterations** | 3 |

---

#### Agent A-10: Quality Assurance Agent

**Task: Define Quality Assurance Agent**

| Field | Value |
|-------|-------|
| **Role** | Chief Quality Officer and Final Gatekeeper |
| **Goal** | Perform the final holistic quality assessment of the complete deliverable: content, citations, formatting, readability, completeness, and professional standards. Produce a signed-off QA report that certifies the document is ready for submission. Block submission if any critical quality gate fails. |
| **Backstory** | A seasoned quality engineer with cross-domain expertise who has defined quality standards for several AI and publishing organizations. Uncompromising on the criteria that matter; pragmatic about everything else. Every QA report is thorough enough to be used as a project post-mortem. |
| **Inputs** | Final PDF; LaTeX source; citation audit report; review report; all preceding agent outputs |
| **Outputs** | QA report: all quality gates with pass/fail status; final score; certification or rejection with required fixes |
| **Tools** | `ReadabilityScoreTool`, `CitationValidatorTool` |
| **Memory** | Short-term; access to all prior outputs |
| **Quality Metrics** | All critical gates pass; QA report signed; final document certified |
| **Max Iterations** | 2 |

---

### 4.3 Agent Evaluation Task

**Task AGENT-EVAL-01: Evaluate Whether Additional Agents Are Needed**

After initial design, perform a structured evaluation:

1. Is there a gap in the research pipeline? → Consider `Literature Review Agent`.
2. Is glossary management too burdensome for the editor? → Consider `Glossary Agent`.
3. Are figures/diagrams required? → Consider `Figure Generation Agent` (uses code execution).
4. Is the LaTeX template complex enough to warrant split roles? → Consider `Template Specialist Agent`.
5. Evaluation rubric: identify any task currently assigned to an agent that is >40% of that agent's workload and could be independently valuable.

**Decision documented in:** `docs/ARCHITECTURE.md` → Agent Design Rationale section.

---

## 5. Workflow Design

### 5.1 Pipeline Stages

```
STAGE 0: Initialization
  → Load config; validate settings; setup output directories; initialize logger

STAGE 1: Topic Finalization
  → Validate topic; expand topic into subtopics; define target audience and scope

STAGE 2: Research
  → Research Agent collects sources
  → Fact Verification Agent validates claims
  → Citation Agent pre-validates source metadata
  [QUALITY GATE 1: ≥15 verified sources; ≥0 hallucinations resolved]

STAGE 3: Outline
  → Outline Architect Agent generates hierarchical outline
  [QUALITY GATE 2: Outline completeness check; word count feasibility]
  [HUMAN CHECKPOINT: Optional outline review before writing begins]

STAGE 4: Writing
  → Writer Agent produces manuscript (chapter by chapter)
  → Editor Agent refines each chapter in turn (or full document pass)
  [QUALITY GATE 3: Word count ±10%; readability ≥60]

STAGE 5: Review
  → Reviewer Agent conducts peer review
  → Writer Agent addresses major concerns (revision loop, max 2 iterations)
  [QUALITY GATE 4: No unresolved major concerns]

STAGE 6: Citation Finalization
  → Citation Agent audits and produces .bib file
  [QUALITY GATE 5: 100% citation match; zero hallucinated]

STAGE 7: LaTeX Formatting
  → LaTeX Formatter Agent transforms manuscript to .tex
  → Iterative compilation fixing
  [QUALITY GATE 6: Compilation succeeds; ≥20 pages]

STAGE 8: PDF Production
  → PDF Production Agent runs final compilation
  → Optimizes PDF metadata
  [QUALITY GATE 7: PDF opens; all elements render]

STAGE 9: Final QA
  → QA Agent holistic review
  [QUALITY GATE 8: All gates passed; QA report signed]

STAGE 10: Output
  → Copy artifacts to output/
  → Generate pipeline summary report
  → Archive LaTeX source
```

### 5.2 Sequential vs. Hierarchical Workflow

**Task WF-01: Implement Sequential Core Pipeline**

The main pipeline is sequential (each stage depends on the previous). CrewAI `Process.sequential` used for the main flow.

**Task WF-02: Implement Hierarchical Sub-Crews**

Research and Editorial phases use `Process.hierarchical` with a manager LLM to distribute subtasks within each phase.

```python
research_crew = Crew(
    agents=[research_agent, fact_verification_agent, citation_agent],
    tasks=[...],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o"),
)

editorial_crew = Crew(
    agents=[editor_agent, reviewer_agent],
    tasks=[...],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o"),
)
```

### 5.3 Context Passing Strategy

**Task WF-03: Design Context Passing**

Context is passed between agents via:
1. **Task output chaining**: `task.output` → next task's `context` parameter.
2. **Shared `PipelineState` object**: written to disk as `output/pipeline_state.json` at each stage boundary.
3. **Crew memory**: CrewAI entity memory enabled for within-crew cross-agent awareness.
4. **Explicit Pydantic models**: all outputs are `BaseModel` instances serialized to JSON.

No agent may access another agent's outputs except via the above mechanisms (no global variables).

### 5.4 Retry Mechanisms

**Task WF-04: Implement Retry Logic**

```python
class RetryConfig:
    max_attempts: int = 3
    initial_delay_seconds: float = 2.0
    backoff_multiplier: float = 2.0
    max_delay_seconds: float = 30.0
    retry_on: tuple[type[Exception]] = (AgentFailureError, SearchError)
```

- Agent-level retries: built-in CrewAI `max_iter`; custom retry wrapper for tool calls.
- Stage-level retries: `PipelineStage.execute_with_retry()` wraps each stage.
- Non-recoverable failures: immediately surface with `PipelineError`; log full context; suggest resolution.

### 5.5 Human-in-the-Loop Checkpoints

**Task WF-05: Implement Optional Human Checkpoints**

```
CHECKPOINT-1: After outline generation (optional)
  - If HUMAN_REVIEW_OUTLINE=true in .env, pause and display outline via Rich console
  - Prompt: "Approve outline? [Y/n/edit]"
  - If 'edit': accept free-form text corrections
  - Timeout: 60 seconds (auto-approve on timeout)

CHECKPOINT-2: After first draft (optional)
  - If HUMAN_REVIEW_DRAFT=true in .env
  - Display first 500 words of each chapter
  - Prompt: "Approve draft? [Y/n]"

CHECKPOINT-3: After QA report (always)
  - Display QA summary with gate results
  - If any gate FAILED: require explicit human decision to proceed or abort
```

### 5.6 Quality Gates — Detailed Specification

**Task WF-06: Implement Quality Gate System**

```python
class QualityGate:
    name: str
    stage: PipelineStage
    check: Callable[[PipelineState], QualityGateResult]
    severity: Literal["blocking", "warning"]
    on_failure: Literal["retry", "abort", "human_review"]
```

| Gate | Check | Threshold | On Failure |
|------|-------|-----------|------------|
| QG-1 | Source count | ≥15 verified | retry (max 2) |
| QG-2 | Hallucination count | 0 critical | abort |
| QG-3 | Outline completeness | All sections present | retry |
| QG-4 | Word count | ±10% of target | warning |
| QG-5 | Readability | Flesch ≥60 | warning |
| QG-6 | Major review concerns | 0 unresolved | retry (1 revision) |
| QG-7 | Citation match rate | 100% | abort |
| QG-8 | LaTeX compilation | Exit code 0 | retry (3 attempts) |
| QG-9 | PDF page count | ≥20 pages | abort |
| QG-10 | QA sign-off | All critical pass | abort |

---

## 6. Topic Selection Framework

### 6.1 Topic Evaluation Matrix

**Task TOPIC-01: Evaluate and Select Optimal Topic**

Score each candidate topic on all axes (1–5 scale):

| Axis | Description | Weight |
|------|-------------|--------|
| **Originality** | Avoids overused AI topics; fresh angle | 20% |
| **Educational Value** | Genuinely teaches the reader something valuable | 20% |
| **Research Depth** | Sufficient academic literature exists | 20% |
| **Visual/Structural Appeal** | Lends itself to figures, tables, diagrams | 15% |
| **Multi-Agent Showcase** | Requires diverse agent expertise to cover well | 15% |
| **Impressiveness** | Will impress a technically sophisticated reviewer | 10% |

**Minimum qualifying score:** 3.8/5.0 weighted average.

### 6.2 Candidate Topic Recommendations

**Task TOPIC-02: Evaluate the Following Candidate Topics**

| # | Topic | Rationale |
|---|-------|-----------|
| 1 | *The Architecture of Trust: How Modern AI Systems Are Designed to Be Safe* | Highly relevant, rich literature, multi-chapter structure natural |
| 2 | *Emergent Capabilities in Large Language Models: Mechanisms, Evidence, and Open Questions* | Deep research, active debate, impressive to reviewers |
| 3 | *The Mathematics of Diffusion Models: From Score Matching to Stable Diffusion* | Technical depth, strong visual potential (figures), demonstrates rigor |
| 4 | *Multi-Agent Systems in AI: Theoretical Foundations and Modern Applications* | Meta-relevant (our system IS multi-agent), rich literature, broad audience |
| 5 | *The History and Future of Symbolic and Neural AI: A Unified Perspective* | Historical narrative + technical depth; strong structure |
| 6 | *Causal Inference in Machine Learning: From Pearl's Ladder to Modern Practice* | Deep math, strong academic base, impressive and educational |

### 6.3 Topic Selection Criteria and Documentation

**Task TOPIC-03: Document Topic Selection**

- Evaluate all candidates using the scoring matrix.
- Select the highest-scoring topic.
- Document the selection rationale in `docs/PRD.md` → Topic Selection section.
- Define 5–8 key research questions the book must answer.
- Define the target audience profile (knowledge level, background, goals).
- Define the scope boundaries (what is in scope; what is explicitly excluded).

**Recommended topic:** **Option 4 or 6** — both offer exceptional research depth, impressive technical content, and natural multi-chapter structure. Option 4 has the meta-advantage of being directly related to the system building it.

---

## 7. LaTeX System Design

### 7.1 Document Class and Template Selection

**Task LATEX-01: Select and Configure LaTeX Template**

Primary recommendation: **`memoir` class** (most powerful for books) or **`scrbook`** from KOMA-Script.

```latex
% Book template: src/crewai_book/latex/templates/book.tex.j2
\documentclass[
    12pt,
    a4paper,
    twoside,
    openright,
    final
]{memoir}

\usepackage{fontenc}        % Font encoding
\usepackage{inputenc}       % UTF-8
\usepackage{microtype}      % Microtypography
\usepackage{hyperref}       % Hyperlinks and PDF metadata
\usepackage{cleveref}       % Smart cross-referencing
\usepackage{natbib}         % Author-year citations
\usepackage{biblatex}       % Alternative: full bibliography control
\usepackage{graphicx}       % Figures
\usepackage{booktabs}       % Professional tables
\usepackage{listings}       % Code listings
\usepackage{amsmath}        % Mathematics
\usepackage{algorithm2e}    % Algorithms
\usepackage{tikz}           % Diagrams
\usepackage{pgfplots}       % Charts
\usepackage{xcolor}         % Colors
\usepackage{fancyhdr}       % Headers/footers
\usepackage{glossaries}     % Glossary
\usepackage{makeidx}        % Index
\usepackage{epigraph}       % Chapter epigraphs
\usepackage{mdframed}       % Framed environments (definitions, theorems)
```

### 7.2 Document Structure

**Task LATEX-02: Define Complete Document Structure**

```
book.tex (main file)
├── frontmatter/
│   ├── titlepage.tex
│   ├── dedication.tex
│   ├── abstract.tex
│   ├── acknowledgements.tex
│   └── toc.tex
├── chapters/
│   ├── ch01_introduction.tex
│   ├── ch02_[topic_chapter_2].tex
│   ├── ch03_[topic_chapter_3].tex
│   ├── ch04_[topic_chapter_4].tex
│   ├── ch05_[topic_chapter_5].tex
│   └── ch06_conclusion.tex
├── backmatter/
│   ├── appendix_a.tex
│   ├── appendix_b.tex
│   ├── glossary.tex
│   ├── bibliography.tex
│   └── index.tex
└── assets/
    ├── figures/
    ├── tables/
    └── listings/
```

### 7.3 Typography and Professional Standards

**Task LATEX-03: Implement Professional Typography**

- **Font:** `\usepackage{palatino}` or `\usepackage{lmodern}` — professional book fonts.
- **Microtype:** Enable `\usepackage[protrusion=true,expansion=true]{microtype}` for paragraph-level typographic optimization.
- **Line spacing:** `\OnehalfSpacing` (memoir) for readability.
- **Chapter style:** Custom `\chapterstyle{ell}` or similar — decorative but professional.
- **Headers:** `\pagestyle{ruled}` with chapter/section names.
- **Color scheme:** Deep navy `#003366` for headings; black for body text.
- **Hyperref colors:** Internal links in navy; citations in dark green; URLs in dark red.
- **PDF metadata:** Title, author, subject, keywords all set via `\hypersetup`.

### 7.4 Bibliography and Citation Management

**Task LATEX-04: Configure BibLaTeX and Bibliography**

- Use **BibLaTeX** with **Biber** backend (modern, Unicode-safe, full control).
- Style: `\usepackage[style=apa]{biblatex}` or `style=authoryear-comp` for academic feel.
- Inline citations: `\textcite{key}` (Author, Year) and `\parencite{key}` [(Author, Year)].
- Bibliography section: full entries, DOI links active.
- `.bib` file: `output/references.bib`; maintained by Citation Agent.
- Validation: `biber --validate-datamodel` run as part of CI.

### 7.5 Figures and Tables

**Task LATEX-05: Define Figure and Table Standards**

- All figures wrapped in `\begin{figure}[htbp]` with `\caption` and `\label`.
- All tables use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`); no vertical rules.
- Large tables use `longtable` for multi-page.
- Complex diagrams: TikZ (generated via Python `tikzplotlib` or written by LaTeX Agent).
- Charts: `pgfplots` or included as PDF figures generated by Python `matplotlib`.
- List of Figures and List of Tables included in frontmatter.

### 7.6 Glossary and Index

**Task LATEX-06: Implement Glossary and Index**

- Glossary: 15–30 terms; defined using `\newglossaryentry`; printed at back.
- Acronyms: separate acronym list using `glossaries` package.
- Index: key terms indexed throughout text using `\index{term}`; compiled with `makeindex`.
- Cross-references: `\cref{label}` used everywhere (never hardcoded "Figure 3").

### 7.7 Appendices

**Task LATEX-07: Design Appendix Content**

```
Appendix A: System Architecture Diagrams (the CrewAI pipeline itself)
Appendix B: Full Agent Prompts (Role/Goal/Backstory for each agent)
Appendix C: Raw Research Corpus (annotated source list)
Appendix D: Pipeline Run Statistics (tokens, cost, time)
```

### 7.8 LaTeX Compilation Pipeline

**Task LATEX-08: Implement Compilation Sequence**

```bash
# Full compilation sequence (handled by LaTeXClient)
cd output/latex
pdflatex -interaction=nonstopmode book.tex
biber book
makeglossaries book
makeindex book
pdflatex -interaction=nonstopmode book.tex
pdflatex -interaction=nonstopmode book.tex  # Third pass for refs
```

Or via `latexmk`:
```bash
latexmk -pdf -bibtex -interaction=nonstopmode book.tex
```

Error handling: parse `.log` file for errors; surface with line numbers in Python exception.

---

## 8. Research and Content Pipeline

### 8.1 Source Collection Strategy

**Task RESEARCH-01: Define Source Collection Strategy**

The Research Agent uses a multi-source strategy:

| Source Type | Tool | Target Count | Credibility Weight |
|-------------|------|-------------|-------------------|
| Academic papers (ArXiv, SemanticScholar) | `ArXivTool` | ≥8 | 1.0 |
| Peer-reviewed journal articles | `WebSearchTool` (Scholar) | ≥5 | 1.0 |
| Authoritative books/textbooks | `WebSearchTool` | ≥3 | 0.9 |
| Conference papers (NeurIPS, ICML, etc.) | `ArXivTool` | ≥4 | 0.95 |
| Official documentation/reports | `WebSearchTool` | ≥2 | 0.85 |
| High-quality technical blogs (distill.pub, etc.) | `WebSearchTool` | ≤3 | 0.7 |

**Total minimum:** 20 sources; **target:** 25–30.

Search query strategy:
1. Broad topic search (3–5 queries).
2. Subtopic deep-dive (2–3 queries per subtopic).
3. Citation snowballing (follow references from top papers).
4. Recency filter: prioritize sources from last 5 years.

### 8.2 Source Validation

**Task RESEARCH-02: Implement Source Validation Pipeline**

Each source must pass:
- [ ] **Accessibility check**: URL or DOI resolves successfully.
- [ ] **Date verification**: Publication year confirmed from page, not just query.
- [ ] **Author verification**: At least one author is identifiable.
- [ ] **Content relevance**: Abstract/summary matches topic (relevance score ≥0.7).
- [ ] **Credibility assessment**: Source is not a preprint farm, predatory journal, or anonymous blog.

Validation is implemented in `CitationValidatorTool` and `FactCheckTool`.

### 8.3 Hallucination Detection

**Task RESEARCH-03: Implement Hallucination Detection**

Multi-layer hallucination detection:

**Layer 1: Citation existence verification**
- Every cited paper: title + authors verified via ArXiv or CrossRef API.
- DOIs validated against doi.org resolver.

**Layer 2: Claim cross-verification**
- Every factual claim cross-checked against ≥2 independent sources.
- Statistical claims verified against primary source data.
- Date/timeline claims verified against multiple sources.

**Layer 3: Consistency checking**
- Fact Verification Agent uses an LLM with lower temperature (0.0) to evaluate claim consistency across the corpus.
- Contradictions flagged and escalated.

**Layer 4: Confidence scoring**
```
Score 0.9–1.0: Verified against ≥3 primary sources, zero contradictions
Score 0.7–0.89: Verified against ≥2 sources, minor ambiguity
Score 0.5–0.69: Single source, plausible, flagged for review
Score < 0.5: Unverifiable; must be removed or heavily caveated
```

### 8.4 Knowledge Synthesis

**Task RESEARCH-04: Define Knowledge Synthesis Process**

After research validation, the Outline Architect Agent performs synthesis:
1. Groups sources into thematic clusters.
2. Identifies consensus views vs. contested claims.
3. Maps key concepts and their relationships.
4. Identifies gaps in the literature that the book can address.
5. Produces a "knowledge map" (structured dict) passed to Writer Agent.

### 8.5 Content Quality Standards

**Task RESEARCH-05: Define Content Quality Metrics**

| Metric | Tool | Threshold |
|--------|------|-----------|
| Flesch Reading Ease | `textstat` | ≥60 (readable) |
| Flesch-Kincaid Grade | `textstat` | ≤14 (graduate level, appropriate) |
| Gunning Fog Index | `textstat` | ≤16 |
| Citation density | custom | 1 citation per 300–500 words |
| Passive voice ratio | custom regex | ≤25% of sentences |
| Average sentence length | `textstat` | 15–25 words |
| Technical term consistency | entity memory | 100% consistent usage |

---

## 9. Testing Strategy

### 9.1 Test Configuration

**Task TEST-00: Configure Test Infrastructure**

```python
# tests/conftest.py

@pytest.fixture
def mock_llm():
    """Returns a mock LLM that returns deterministic responses."""

@pytest.fixture
def mock_search_client():
    """Returns a mock search client with a pre-seeded source list."""

@pytest.fixture
def sample_settings():
    """Returns a Settings instance with test-safe values."""

@pytest.fixture
def sample_research_corpus():
    """Returns a realistic but synthetic research corpus."""

@pytest.fixture
def sample_manuscript():
    """Returns a complete synthetic manuscript for editor/formatter tests."""

@pytest.fixture
def sample_bib_file(tmp_path):
    """Creates a temporary .bib file for citation tests."""
```

`pytest.ini` / `pyproject.toml` test config:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "unit: fast, no I/O",
    "integration: may use temp files",
    "e2e: full pipeline, slow",
    "benchmark: performance tests",
]
```

---

### 9.2 Unit Tests

#### 9.2.1 Agent Unit Tests

**Task TEST-01: Write Research Agent Unit Tests**

File: `tests/unit/agents/test_research_agent.py`

| Test | Goal | Method | Expected | DoD |
|------|------|--------|----------|-----|
| `test_agent_initialization` | Agent creates with correct config | Assert role/goal/backstory fields | Fields match config | Passes |
| `test_agent_tool_assignment` | Agent has correct tools | Assert tool list | WebSearch, ArXiv, CitationValidator | Passes |
| `test_agent_produces_typed_output` | Output matches domain model | Mock LLM; assert return type | `ResearchCorpus` instance | Passes |
| `test_agent_deduplicates_sources` | No duplicate URLs | Feed duplicate sources | Single entry in output | Passes |
| `test_agent_respects_min_source_count` | At least 15 sources | Mock with 10 sources | Triggers retry | Passes |
| `test_agent_handles_search_failure` | Graceful error handling | Raise `SearchError` | `ResearchError` raised | Passes |

**Task TEST-02: Write Fact Verification Agent Unit Tests**

File: `tests/unit/agents/test_fact_verification_agent.py`

| Test | Goal | Method | Expected | DoD |
|------|------|--------|----------|-----|
| `test_flags_hallucinated_citation` | Detects fake paper | Input known-fake citation | Flag with severity=HIGH | Passes |
| `test_confidence_scoring` | Scores correlate with verification depth | 3-source vs 1-source claim | 3-source scores higher | Passes |
| `test_zero_tolerance_critical_flags` | Pipeline blocked on critical flag | Input critical hallucination | `HallucinationDetectedError` | Passes |
| `test_valid_claims_pass` | Real claims pass verification | Input verified facts | All pass, no flags | Passes |

**Task TEST-03: Write Writer Agent Unit Tests**

File: `tests/unit/agents/test_writer_agent.py`

| Test | Goal | Method | Expected | DoD |
|------|------|--------|----------|-----|
| `test_produces_correct_word_count` | Word count within 5% of target | Mock LLM; set target | Within tolerance | Passes |
| `test_includes_citation_markers` | Citations inserted | Input corpus with sources | ≥N citation markers | Passes |
| `test_consistent_terminology` | No term drift | Check entity memory | Consistent usage | Passes |
| `test_readability_score` | Flesch ≥60 | Check score on output | ≥60 | Passes |

**Task TEST-04–TEST-10: Write Unit Tests for Remaining Agents**

Analogous test files for: `editor_agent`, `reviewer_agent`, `citation_agent`, `latex_formatter_agent`, `pdf_production_agent`, `qa_agent`.

Each file must include:
- Initialization test
- Happy path test
- Failure/error test
- Output type validation test

---

#### 9.2.2 Tool Unit Tests

**Task TEST-11: Write Tool Unit Tests**

File: `tests/unit/tools/`

| Tool | Key Tests |
|------|-----------|
| `WebSearchTool` | Returns results; handles rate limit; handles no results |
| `ArXivTool` | Queries by keyword; returns paper metadata; handles connection error |
| `CitationValidatorTool` | Valid DOI passes; invalid DOI fails; URL check |
| `LaTeXCompilerTool` | Valid .tex compiles; invalid .tex raises `CompilationError` with log |
| `ReadabilityScoreTool` | Returns score >0 for non-empty text; handles empty string |
| `FactCheckTool` | Cross-verification logic; confidence scoring |

---

#### 9.2.3 Service Unit Tests

**Task TEST-12: Write Service Unit Tests**

File: `tests/unit/services/`

All external dependencies mocked. Tests cover:
- Business logic correctness.
- Edge cases (empty input, oversized input, malformed data).
- Exception propagation.

---

#### 9.2.4 Configuration Tests

**Task TEST-13: Write Configuration Unit Tests**

File: `tests/unit/config/test_settings.py`

| Test | Expected |
|------|----------|
| Valid config loads | `Settings` instance created |
| Missing required key | `ValidationError` raised |
| Invalid model name | `ValidationError` raised |
| API key not exposed in repr | `SecretStr` masks value |
| Default values correct | Defaults match spec |

---

### 9.3 Integration Tests

**Task TEST-14: Research Pipeline Integration Test**

File: `tests/integration/test_research_pipeline.py`

- Goal: Verify Research Agent + Fact Verification Agent + Citation Agent work together.
- Method: Real tools with controlled topic; limited to 5 sources.
- Expected: `ResearchCorpus` with verified sources, no hallucinations.
- DoD: Test passes; corpus persisted to temp dir.

**Task TEST-15: LaTeX Pipeline Integration Test**

File: `tests/integration/test_latex_pipeline.py`

- Goal: Verify a sample manuscript converts to compilable LaTeX.
- Method: Input synthetic manuscript; run LaTeX Formatter → PDF Production.
- Expected: `output/test_output.pdf` created; `pdflatex` exits 0.
- DoD: PDF exists and has ≥1 page.

**Task TEST-16: Citation Pipeline Integration Test**

File: `tests/integration/test_citation_pipeline.py`

- Goal: Verify citation markers in manuscript match entries in `.bib`.
- Method: Input manuscript with known citations; run Citation Agent.
- Expected: 100% match rate; `.bib` valid.
- DoD: `biber --validate-datamodel` exits 0.

**Task TEST-17: Error Recovery Integration Test**

File: `tests/integration/test_error_recovery.py`

- Goal: Verify pipeline recovers from transient failures.
- Method: Inject `SearchError` on first call; second call succeeds.
- Expected: Pipeline completes; retry count = 1 in logs.
- DoD: Test passes; log shows retry event.

**Task TEST-18: End-to-End Integration Test**

File: `tests/integration/test_e2e.py`

- Goal: Full pipeline produces a PDF from a simple topic.
- Method: Run full pipeline with minimal topic ("Introduction to Machine Learning"); use mock LLM for speed.
- Expected: PDF exists; ≥5 pages (mock content is shorter); all quality gates passed.
- DoD: Test passes in <5 minutes with mocked LLM.

---

### 9.4 Quality Evaluation Tests

**Task TEST-19: Content Quality Evaluation**

File: `tests/evaluation/test_content_quality.py`

- Readability score ≥60 (Flesch).
- Word count within 10% of target.
- Passive voice ≤25%.
- No placeholder text (`TODO`, `FIXME`, `[INSERT]`) in final document.

**Task TEST-20: Citation Quality Evaluation**

File: `tests/evaluation/test_citation_quality.py`

- 100% citation-to-bibliography match.
- Zero broken URLs/DOIs.
- Citation count ≥15.
- BibTeX validates cleanly.

**Task TEST-21: Reproducibility Test**

File: `tests/evaluation/test_reproducibility.py`

- Run pipeline twice with same seed and config.
- Compare structural output (chapter count, section count, citation count).
- Expected: Identical structure (content may vary slightly due to LLM temperature).
- DoD: Structure diff is empty.

---

## 10. Documentation Requirements

### 10.1 README.md

**Task DOC-01: Write README.md**

Structure:
```markdown
# CrewAI Multi-Agent Book Generator

## Overview (3–4 sentences; include architecture summary)
## Features (bullet list of key capabilities)
## Quick Start
  ### Prerequisites
  ### Installation
  ### Configuration
  ### Running the Pipeline
## Architecture Overview (Mermaid diagram)
## Project Structure (tree of key directories)
## Documentation Index (links to all docs/)
## Testing
## Contributing
## License
```

Standards:
- ≤5 minutes to follow from zero to running.
- All commands copy-pasteable.
- Mermaid diagram embedded (renders on GitHub).
- Badges: CI status, coverage, Python version.

---

### 10.2 docs/PRD.md

**Task DOC-02: Write Product Requirements Document**

Structure:
```markdown
# Product Requirements Document
## 1. Executive Summary
## 2. Problem Statement
## 3. Goals and Non-Goals
## 4. Target Users
## 5. Functional Requirements (reference FR-XX table)
## 6. Non-Functional Requirements (reference NFR-XX table)
## 7. System Constraints
## 8. Topic Selection (rationale, scoring, decision)
## 9. Success Metrics
## 10. Risk Analysis
## 11. Open Questions
## Appendix: Requirements Traceability Matrix
```

---

### 10.3 docs/PLAN.md

**Task DOC-03: Write Architecture and Implementation Plan**

Structure:
```markdown
# Implementation Plan
## 1. Architecture Philosophy
## 2. Technology Stack (justified choices)
## 3. Layer Architecture (SDK / Service / Domain / Agents)
## 4. CrewAI Design Decisions
## 5. LaTeX Strategy
## 6. Quality Strategy
## 7. Implementation Phases
## 8. Risk Mitigation
## 9. Decision Log (ADRs — Architecture Decision Records)
```

---

### 10.4 docs/ARCHITECTURE.md

**Task DOC-04: Write Architecture Document with Diagrams**

Required diagrams:
1. **System Context Diagram**: user → system → external APIs.
2. **Agent Collaboration Diagram**: agent interactions and data flows.
3. **Pipeline Stage Diagram**: sequence of stages with quality gates.
4. **Layer Architecture Diagram**: SDK → Service → Domain → Agent layers.
5. **LaTeX Compilation Diagram**: from manuscript to PDF.

All diagrams in Mermaid (renderable on GitHub).

---

### 10.5 docs/RESEARCH.md

**Task DOC-05: Write Research Methodology Document**

Structure:
```markdown
# Research Methodology and Results
## 1. Research Questions
## 2. Source Collection Strategy
## 3. Quality Evaluation Methodology
## 4. Hallucination Detection Results
## 5. Citation Statistics
## 6. Comparative Evaluation (agent vs baseline)
## 7. Experiments and Findings
## 8. Failure Analysis
## 9. Cost Analysis
## 10. Runtime Analysis
```

---

### 10.6 docs/USER_GUIDE.md

**Task DOC-06: Write User Guide**

Covers:
- Installation on macOS and Linux.
- Configuration (`.env` setup).
- Running the pipeline.
- Understanding the output.
- Customizing the topic.
- Troubleshooting common errors.

Verified by: following guide on a clean machine and completing successfully.

---

### 10.7 docs/DEVELOPER_GUIDE.md

**Task DOC-07: Write Developer Guide**

Covers:
- Development environment setup.
- Running tests.
- Adding a new agent.
- Adding a new tool.
- Extending the LaTeX template.
- CI pipeline explanation.
- Release process.
- Code style and conventions.
- How to update this TODO.

---

### 10.8 Per-Agent Documentation

**Task DOC-08: Write Agent Documentation Files**

For each of the 10 agents, create `docs/agents/{agent_name}.md`:

```markdown
# {Agent Name}

## Role
## Goal
## Backstory
## Inputs
## Outputs
## Tools Used
## Quality Metrics
## Integration Points
## Known Limitations
## Test Coverage
```

---

### 10.9 Additional PRDs

**Task DOC-09: Write PRD for Research Pipeline**
File: `docs/prds/PRD_research_pipeline.md`

**Task DOC-10: Write PRD for LaTeX System**
File: `docs/prds/PRD_latex_system.md`

**Task DOC-11: Write PRD for PDF Production**
File: `docs/prds/PRD_pdf_production.md`

---

## 11. Research and Evaluation Section

### 11.1 Experiments

**Task EVAL-01: Baseline Comparison Experiment**

Compare the multi-agent system output against a naive single-prompt baseline:
- **Baseline**: Single GPT-4o prompt with topic → generate article.
- **System**: Full multi-agent pipeline.
- **Metrics**: Word count, citation count, readability score, factual accuracy (manual spot-check), structural completeness.
- **Expected**: System outperforms baseline on all metrics.
- **Result documented in**: `evaluation/reports/baseline_comparison.md`.

**Task EVAL-02: Agent Ablation Experiment**

Remove one agent at a time and measure impact:
- Remove Fact Verification Agent → measure hallucination rate.
- Remove Editor Agent → measure readability drop.
- Remove Citation Agent → measure citation error rate.
- **Result documented in**: `evaluation/reports/ablation_study.md`.

**Task EVAL-03: Pipeline Stress Test**

Run pipeline on 3 different topics:
- Simple topic (narrow scope, many sources).
- Complex topic (broad scope, contested literature).
- Niche topic (limited sources, requires synthesis).
- **Result documented in**: `evaluation/reports/stress_test.md`.

### 11.2 Metrics

**Task EVAL-04: Define and Collect All Metrics**

| Metric | Collection Method | Target |
|--------|------------------|--------|
| Total pipeline runtime | `time.perf_counter()` | ≤30 min |
| Total tokens used | OpenAI usage API | Logged |
| Estimated cost | Token count × price | Logged |
| Citation count | Citation Agent output | ≥15 |
| Hallucination rate | Fact check results | 0% critical |
| Readability score | `textstat` | ≥60 Flesch |
| PDF page count | `pypdf` | ≥20 pages |
| LaTeX compilation time | Timer | ≤60 sec |
| Agent retry count | Pipeline state | Logged |
| QA gate pass rate | QA report | 100% critical |

All metrics persisted to `evaluation/results/metrics.json`.

### 11.3 Cost Analysis

**Task EVAL-05: Document Cost Analysis**

- Record token usage per agent (input + output).
- Compute per-stage and total cost at current API pricing.
- Identify most expensive agents; propose optimizations.
- Document in `evaluation/reports/cost_analysis.md`.

### 11.4 Runtime Analysis

**Task EVAL-06: Profile Pipeline Runtime**

- Time each stage separately.
- Identify bottlenecks.
- Profile memory usage per stage.
- Compute tokens-per-second throughput.
- Document in `evaluation/reports/runtime_analysis.md`.

### 11.5 Failure Analysis

**Task EVAL-07: Document Failure Modes**

From test runs and stress tests, document:
- All observed failure modes.
- Their frequency and severity.
- Mitigation strategies implemented.
- Remaining risks.
- Document in `evaluation/reports/failure_analysis.md`.

---

## 12. Project Timeline

### Phase 0 — Analysis (Day 1)

**Goal:** Fully understand requirements; make no implementation decisions prematurely.

| Task | Deliverable | Completion Criteria |
|------|-------------|---------------------|
| Read all provided documents | Full understanding | No open questions |
| Create this TODO.md | Approved TODO.md | All sections complete |
| Create repository skeleton | Empty repo with structure | `git push` success |
| Validate all tools available | Tool checklist | Python 3.11+, LaTeX, make all accessible |

**Phase 0 is complete when:** This TODO.md exists, is committed, and the repository skeleton is in place.

---

### Phase 1 — Planning (Day 1–2)

**Goal:** All planning documents written; topic selected; architecture finalized.

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| Write `docs/PRD.md` | PRD.md | Phase 0 | All sections complete |
| Write `docs/PLAN.md` | PLAN.md | PRD.md | All ADRs documented |
| Topic evaluation | Topic decision | PRD.md | Score ≥3.8/5.0; documented |
| `.env.example` | `.env.example` | Architecture | All keys documented |
| `pyproject.toml` | Build config | Phase 0 | `pip install -e ".[dev]"` works |
| Makefile | Makefile | Phase 0 | All targets defined |
| Pre-commit hooks | `.pre-commit-config.yaml` | pyproject.toml | Hooks install and run |

**Phase 1 is complete when:** All planning documents committed; topic selected; build system works.

---

### Phase 2 — Architecture (Day 2–3)

**Goal:** All layers designed; configuration working; domain models complete.

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| Domain models | `domain/` | Phase 1 | `mypy --strict` passes |
| Settings model | `config/settings.py` | `.env.example` | All configs load from `.env` |
| SDK layer | `sdk/` | Domain | All clients testable |
| Service layer | `services/` | SDK | Business logic isolated |
| Logger/observability | `observability/` | Settings | Structured logs produced |
| Error hierarchy | exceptions defined | Domain | All exception types present |
| `docs/ARCHITECTURE.md` | Architecture doc | All above | Diagrams render on GitHub |

**Phase 2 is complete when:** All layers compile; `mypy` passes; ARCHITECTURE.md committed.

---

### Phase 3 — Implementation (Day 3–7)

**Goal:** All agents, tools, and workflows fully implemented.

**Sub-phase 3a: Tools (Day 3–4)**

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| `WebSearchTool` | Tool class | SDK layer | Manual test returns results |
| `ArXivTool` | Tool class | SDK layer | ArXiv query returns papers |
| `CitationValidatorTool` | Tool class | SDK layer | DOI validation works |
| `LaTeXCompilerTool` | Tool class | LaTeX client | Compilation test passes |
| `ReadabilityScoreTool` | Tool class | `textstat` | Score returned for sample text |
| `FactCheckTool` | Tool class | SDK layer | Cross-check logic works |

**Sub-phase 3b: Agents (Day 4–5)**

Implement agents in dependency order:
1. Research Agent (A-01)
2. Fact Verification Agent (A-02)
3. Citation Agent (A-07)
4. Outline Architect Agent (A-03)
5. Writer Agent (A-04)
6. Editor Agent (A-05)
7. Reviewer Agent (A-06)
8. LaTeX Formatter Agent (A-08)
9. PDF Production Agent (A-09)
10. Quality Assurance Agent (A-10)

**Sub-phase 3c: Workflows (Day 5–6)**

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| Research sub-crew | `workflows/research_crew.py` | Agents A01–03 | Crew runs successfully |
| Editorial sub-crew | `workflows/editorial_crew.py` | Agents A04–06 | Crew runs successfully |
| Main crew | `workflows/main_crew.py` | All agents | Full pipeline runs |
| Quality gates | Gate implementations | Workflows | All gates trigger correctly |
| Retry logic | Retry wrappers | Workflows | Retry tested with mock failure |
| Human checkpoints | Interactive prompts | Workflows | Prompts appear when configured |

**Sub-phase 3d: LaTeX System (Day 6–7)**

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| Book LaTeX template | `templates/book.tex.j2` | None | Compiles with sample data |
| Jinja2 renderer | `latex/renderer.py` | Template | Renders to valid `.tex` |
| Compilation pipeline | `LaTeXClient` | Renderer | Full compile succeeds |
| Bibliography integration | BibLaTeX config | Template | Citations render |
| Glossary/Index | LaTeX config | Template | Glossary and index compile |

**Phase 3 is complete when:** `make run` completes end-to-end (with real or mock LLM); PDF is produced.

---

### Phase 4 — Testing (Day 7–9)

**Goal:** All tests written and passing; coverage ≥85%.

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| Unit tests (all agents) | Test files | Phase 3 | All pass |
| Unit tests (all tools) | Test files | Phase 3 | All pass |
| Unit tests (services) | Test files | Phase 3 | All pass |
| Integration tests | Test files | Phase 3 | All pass |
| E2E test | Test file | Phase 3 | Passes in <5 min |
| Coverage check | Coverage report | All tests | ≥85% |
| `make lint` clean | Zero errors | Phase 3 | `ruff check` exits 0 |
| `mypy` clean | Zero errors | Phase 3 | `mypy --strict` exits 0 |

**Phase 4 is complete when:** `make test` passes with ≥85% coverage; `make lint` clean.

---

### Phase 5 — Evaluation (Day 9–10)

**Goal:** All evaluation experiments run; results documented.

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| Baseline comparison | `evaluation/reports/baseline_comparison.md` | Phase 3 | Report complete with data |
| Ablation study | `evaluation/reports/ablation_study.md` | Phase 3 | All agents tested |
| Stress test (3 topics) | `evaluation/reports/stress_test.md` | Phase 3 | 3 PDFs produced |
| Cost analysis | `evaluation/reports/cost_analysis.md` | Runs logged | Costs documented |
| Runtime analysis | `evaluation/reports/runtime_analysis.md` | Runs profiled | Bottlenecks identified |
| Failure analysis | `evaluation/reports/failure_analysis.md` | All tests | All modes documented |
| Metrics collection | `evaluation/results/metrics.json` | All runs | All metrics present |

**Phase 5 is complete when:** All evaluation reports committed; metrics.json populated.

---

### Phase 6 — Documentation (Day 10–11)

**Goal:** All documentation complete, reviewed, and spell-checked.

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| README.md (final) | README.md | All phases | Quickstart verified |
| PRD.md (finalized) | docs/PRD.md | Phase 5 | All sections complete |
| PLAN.md (finalized) | docs/PLAN.md | Phase 5 | ADRs all documented |
| ARCHITECTURE.md | docs/ARCHITECTURE.md | Phase 3 | Diagrams accurate |
| RESEARCH.md | docs/RESEARCH.md | Phase 5 | All metrics included |
| USER_GUIDE.md | docs/USER_GUIDE.md | Phase 3 | Verified on clean machine |
| DEVELOPER_GUIDE.md | docs/DEVELOPER_GUIDE.md | Phase 3 | All procedures verified |
| Per-agent docs | `docs/agents/*.md` | Phase 3 | All 10 agents documented |
| PRD subdocs | `docs/prds/*.md` | Phase 3 | All 3 files complete |
| Spell check all docs | — | All above | `aspell` / `codespell` clean |
| Cross-reference check | — | All above | All internal links resolve |
| Update TODO.md | This file | All phases | All tasks marked |

**Phase 6 is complete when:** All documentation committed; `codespell` clean; links verified.

---

### Phase 7 — Final Submission (Day 11–12)

**Goal:** Submission-ready package produced and verified.

| Task | Deliverable | Dependency | Completion Criteria |
|------|-------------|------------|---------------------|
| Final `make run` | Final PDF | Phase 6 | PDF ≥20 pages; QA pass |
| Final `make test` | Test report | Phase 4 | All green; ≥85% coverage |
| Final `make lint` | Lint report | Phase 4 | Zero errors |
| Security scan | `gitleaks` report | Phase 6 | Zero secrets found |
| Submission archive | `.zip` / `.tar.gz` | All | All D-01 to D-15 present |
| Archive structure check | Checklist | Archive | Matches required layout |
| Fresh-environment install test | Install log | Archive | Works on clean machine |
| Final peer review | Sign-off checklist | All | All items checked |
| Tag release | `git tag v1.0.0` | Final commit | Tag pushed to remote |
| Submit | Submission confirmed | Archive | Confirmation received |

**Phase 7 is complete when:** Submission is confirmed; tag pushed; all deliverables verified.

---

## 13. Definition of Done

### 13.1 Repository and Code

| Subsystem | Acceptance Criteria | Validation Method | Evidence Required |
|-----------|--------------------|--------------------|-------------------|
| Repository structure | Matches spec exactly | `tree` command output | Screenshot / log |
| `pyproject.toml` | All deps pinned; install works | Fresh venv install | Install log |
| Makefile | All targets execute | `make help`; each target run | Command output |
| Type annotations | `mypy --strict` exits 0 | CI log | mypy report |
| Code style | `ruff check` exits 0 | CI log | ruff report |
| Docstrings | `pydocstyle` exits 0 | CI log | pydocstyle report |
| Security | `gitleaks` clean | Pre-commit + CI | Scan report |
| Pre-commit hooks | All hooks pass | `pre-commit run --all-files` | Hook output |

### 13.2 CrewAI System

| Subsystem | Acceptance Criteria | Validation Method | Evidence Required |
|-----------|--------------------|--------------------|-------------------|
| All 10 agents defined | Agent files exist; configs complete | File list + config review | File listing |
| Agent unit tests | All pass; coverage ≥85% per agent | `pytest tests/unit/agents/` | Test report |
| Tools implemented | All 6 tools work | Tool unit tests | Test report |
| Workflows defined | Research + Editorial + Main crews | Import + run test | Run log |
| Quality gates | All 10 gates trigger correctly | Integration test | Gate test results |
| Retry logic | Retries on transient failure | Error recovery test | Test log |
| Human checkpoints | Appear when configured | Manual run with flag | Console output |
| Context passing | Data flows correctly between agents | E2E test | Pipeline state JSON |

### 13.3 LaTeX and PDF

| Subsystem | Acceptance Criteria | Validation Method | Evidence Required |
|-----------|--------------------|--------------------|-------------------|
| LaTeX template | Compiles with sample data | `latexmk` test | Compilation log |
| Full document | ≥20 pages; all sections present | PDF inspection | Page count; visual |
| Bibliography | All citations render; `.bib` valid | `biber --validate` | Validation log |
| Glossary | Glossary compiles; ≥15 terms | PDF inspection | Glossary page |
| Index | Index compiles | PDF inspection | Index page |
| Typography | Professional appearance | Visual inspection | PDF screenshot |
| PDF metadata | Title, author, keywords set | `pdfinfo` | Metadata output |

### 13.4 Research and Content

| Subsystem | Acceptance Criteria | Validation Method | Evidence Required |
|-----------|--------------------|--------------------|-------------------|
| Source count | ≥20 verified sources | Citation list count | Sources log |
| Hallucination rate | 0% critical hallucinations | Fact check report | Audit log |
| Readability | Flesch ≥60 | `textstat` result | Score report |
| Citation match | 100% in-text ↔ bibliography | Citation Agent report | Match report |
| Word count | ±10% of target | Word count check | Count log |

### 13.5 Testing

| Subsystem | Acceptance Criteria | Validation Method | Evidence Required |
|-----------|--------------------|--------------------|-------------------|
| Unit tests | All pass | `pytest tests/unit/` | Test output |
| Integration tests | All pass | `pytest tests/integration/` | Test output |
| E2E test | Passes in <5 min | `pytest tests/integration/test_e2e.py` | Test output |
| Coverage | ≥85% | `pytest --cov` | Coverage report |
| Evaluation tests | All pass | `pytest tests/evaluation/` | Test output |

### 13.6 Documentation

| Document | Acceptance Criteria | Validation Method | Evidence Required |
|----------|--------------------|--------------------|-------------------|
| README.md | Quickstart works on clean machine | Manual test | Install log |
| PRD.md | All sections complete | Review checklist | Reviewed |
| PLAN.md | All ADRs present | Review checklist | Reviewed |
| ARCHITECTURE.md | Diagrams render on GitHub | Push and view | Screenshot |
| RESEARCH.md | All metrics included | Metrics checklist | Reviewed |
| USER_GUIDE.md | Guide works end-to-end | Manual test | Follow-through log |
| DEVELOPER_GUIDE.md | All procedures verified | Manual test | Follow-through log |
| Agent docs | All 10 present and complete | File listing | Review |
| Spell check | `codespell` clean | CI log | Scan report |

---

## 14. Excellence Beyond Requirements

> *This section defines advanced enhancements that are NOT required but would significantly differentiate this project from all peer submissions. Each is evaluated on feasibility, impact, and ROI.*

---

### E-01: Self-Review Loop with Multi-Pass Refinement

**Description:** After the Writer Agent completes each chapter, trigger an automated multi-pass refinement cycle: Writer → Editor → Reviewer → Writer (revision) → Editor (final pass). Up to 3 cycles before proceeding.

**Why it improves the project:** Mimics real professional publishing workflows; measurably improves output quality; demonstrates sophisticated agent orchestration.

**Implementation effort:** Medium (3–4 hours). Requires: cycle counter in `PipelineState`; convergence criterion (readability improvement <2 points = stop); cycle tracking in QA report.

**Expected impact on grading:** High. Demonstrates deep understanding of multi-agent orchestration patterns.

**Recommended priority:** HIGH — implement as part of Phase 3.

---

### E-02: Agent Performance Analytics Dashboard

**Description:** After each pipeline run, generate an HTML report showing per-agent statistics: tokens used, time taken, retry count, quality score improvement, cost, tool calls. Visualized with bar charts and timelines.

**Why it improves the project:** Provides concrete evidence of multi-agent collaboration; makes the system's inner workings visible; impressive in a presentation.

**Implementation effort:** Medium (4–6 hours). Requires: `AgentTracker` class (already planned in observability layer); HTML template with inline Chart.js; `make report` target.

**Expected impact on grading:** High. Gives reviewers something tangible to examine beyond the PDF.

**Recommended priority:** HIGH — implement in Phase 5.

---

### E-03: Citation Confidence Scoring System

**Description:** Every citation in the final document receives a machine-verified confidence score (0.0–1.0) based on: DOI validity, author count, publication venue, year, cross-reference count. Published as a citation quality appendix in the book.

**Why it improves the project:** Addresses hallucination concerns head-on; adds a novel quality signal not found in any typical homework submission; demonstrates rigorous epistemic standards.

**Implementation effort:** Medium (3–4 hours). Requires: `CitationConfidenceScorer` class; integration into Citation Agent; LaTeX appendix template.

**Expected impact on grading:** Very high. Directly addresses one of the hardest problems with AI-generated content.

**Recommended priority:** HIGH — implement in Phase 3c.

---

### E-04: Knowledge Graph Generation

**Description:** After research collection, generate a visual knowledge graph showing relationships between key concepts, authors, and papers. Include in the book's appendix as a TikZ diagram or embedded PDF figure.

**Why it improves the project:** Visually demonstrates the research depth; adds a genuinely novel figure type; shows that agents can synthesize, not just aggregate.

**Implementation effort:** High (6–8 hours). Requires: entity extraction from research corpus; `networkx` graph construction; export to TikZ or Graphviz.

**Expected impact on grading:** High. Visually impressive and technically sophisticated.

**Recommended priority:** MEDIUM — implement if time permits.

---

### E-05: Autonomous Hallucination Detection Pipeline with Report

**Description:** Run a dedicated hallucination detection pass using a separate LLM call with the prompt: "Given this claim and these sources, rate the probability that this claim is hallucinated (0–100%). Explain." Report published as an appendix.

**Why it improves the project:** Makes the system self-aware about its own limitations; addresses AI trustworthiness concerns; publishable methodology.

**Implementation effort:** Medium (4–5 hours). Requires: dedicated `HallucinationDetector` class; confidence calibration; LaTeX appendix.

**Expected impact on grading:** Very high. Demonstrates AI safety awareness.

**Recommended priority:** HIGH — implement in Phase 3b.

---

### E-06: Multiple Publication Format Export

**Description:** In addition to PDF, export the generated content as: (1) HTML (readable in browser), (2) EPUB (readable on e-reader), (3) Markdown (clean, navigable).

**Why it improves the project:** Demonstrates that the LaTeX source is high-quality and reusable; shows engineering breadth; provides multiple submission formats.

**Implementation effort:** Medium (4–6 hours). Requires: `pandoc` CLI wrapper; format-specific templates; `make html`, `make epub`, `make md` targets.

**Expected impact on grading:** Medium-High. Shows versatility without requiring much extra content work.

**Recommended priority:** MEDIUM — implement in Phase 3d.

---

### E-07: Research Traceability Report

**Description:** Every paragraph in the final document is tagged with the source(s) that informed it. A "traceability matrix" in the appendix maps each paragraph to its sources, showing the research → writing provenance chain.

**Why it improves the project:** Provides complete audit trail; demonstrates that no content was hallucinated; shows that agents collaborated with clear data lineage.

**Implementation effort:** High (6–8 hours). Requires: Writer Agent to embed source tags in output; Citation Agent to process tags; LaTeX macro for footnote-based tracing; appendix generation.

**Expected impact on grading:** Very high. No other submission will have this.

**Recommended priority:** MEDIUM — implement if time permits.

---

### E-08: Reproducibility Report as Book Appendix

**Description:** Include in the book itself an appendix titled "How This Document Was Generated" that describes the multi-agent pipeline, agents used, quality gates passed, total cost, runtime, and metrics. Meta-documentation embedded in the artifact.

**Why it improves the project:** The book explains its own creation process; extraordinarily impressive and recursive; makes the engineering work visible to the reviewer reading the PDF.

**Implementation effort:** Low (2–3 hours). Requires: template appendix; data injection from `metrics.json` into LaTeX template.

**Expected impact on grading:** Extremely high. Every reviewer will notice this. Unique in the history of this type of homework.

**Recommended priority:** CRITICAL — implement in Phase 3d. This is the single highest ROI enhancement.

---

### E-09: Agent Collaboration Visualization

**Description:** Generate a visual diagram (Mermaid or TikZ) showing the actual collaboration graph from a real pipeline run: which agent handed off to which, how many rounds of revision occurred, where quality gates fired.

**Why it improves the project:** Makes the multi-agent aspect concrete and visual; goes beyond "we used multiple agents" to "here is exactly how they collaborated."

**Implementation effort:** Low-Medium (2–3 hours). Requires: `AgentTracker` data → Mermaid diagram generator; include in pipeline report and potentially in book appendix.

**Expected impact on grading:** High. Visual proof of multi-agent collaboration.

**Recommended priority:** HIGH — implement in Phase 5.

---

### E-10: Adaptive Quality Agent with Learning

**Description:** The QA Agent maintains a "quality memory" across chapters. If Chapter 2 has a consistent readability problem, it updates the Writer Agent's instructions for Chapter 3. Implements a feedback loop within the pipeline run.

**Why it improves the project:** Demonstrates advanced agent coordination; makes the system genuinely adaptive; results in higher final quality.

**Implementation effort:** High (6–8 hours). Requires: QA-to-Writer feedback mechanism; instruction update protocol; tracking of cross-chapter quality trends.

**Expected impact on grading:** High. Shows deep understanding of adaptive multi-agent systems.

**Recommended priority:** MEDIUM — implement in Phase 3b/3c.

---

### E-11: Cost Optimization Mode

**Description:** Implement a `--fast` / `--quality` CLI flag pair. In `--fast` mode: use GPT-3.5-Turbo for non-critical agents; reduce max iterations; skip optional review passes. In `--quality` mode: full pipeline. Report cost difference.

**Why it improves the project:** Shows production engineering thinking; makes the system practical for different budget constraints; demonstrates cost-conscious LLM usage.

**Implementation effort:** Low (2–3 hours). Requires: agent config variants; CLI flag; cost comparison report.

**Expected impact on grading:** Medium. Shows practical engineering judgment.

**Recommended priority:** LOW — implement after all high-priority items.

---

### E-12: Interactive HTML Export with Navigation

**Description:** Use `pandoc` + custom CSS to produce a polished, navigable HTML version with: collapsible sections, clickable TOC, inline citation tooltips, and a "generation metadata" sidebar showing which agent wrote each section.

**Why it improves the project:** Dramatically more impressive in a live demo; makes the project accessible online; shows full-stack engineering capability.

**Implementation effort:** High (8–10 hours). Requires: pandoc HTML template; custom CSS; JavaScript for interactivity; metadata injection.

**Expected impact on grading:** High, especially if presented live.

**Recommended priority:** LOW-MEDIUM — implement if time and scope permit.

---

### Enhancement Summary and Prioritization

| ID | Enhancement | Priority | Effort | Impact |
|----|-------------|----------|--------|--------|
| E-08 | Reproducibility Report as Book Appendix | **CRITICAL** | Low | Extremely High |
| E-01 | Self-Review Loop / Multi-Pass Refinement | HIGH | Medium | High |
| E-02 | Agent Performance Analytics Dashboard | HIGH | Medium | High |
| E-03 | Citation Confidence Scoring | HIGH | Medium | Very High |
| E-05 | Autonomous Hallucination Detection Pipeline | HIGH | Medium | Very High |
| E-09 | Agent Collaboration Visualization | HIGH | Low | High |
| E-04 | Knowledge Graph Generation | MEDIUM | High | High |
| E-06 | Multiple Publication Format Export | MEDIUM | Medium | Medium-High |
| E-07 | Research Traceability Report | MEDIUM | High | Very High |
| E-10 | Adaptive Quality Agent with Learning | MEDIUM | High | High |
| E-11 | Cost Optimization Mode | LOW | Low | Medium |
| E-12 | Interactive HTML Export | LOW | High | High |

---

## Appendix A: Requirements Traceability Matrix

| Requirement | Phase | Task | Test | Document |
|-------------|-------|------|------|----------|
| FR-01 (CrewAI) | 3b | IMPL-agents | TEST-01..10 | PRD, PLAN |
| FR-02 (Multi-agent) | 3b | IMPL-agents | TEST-01..10 | ARCHITECTURE |
| FR-03 (Collaboration) | 3c | WF-03 | TEST-14..18 | ARCHITECTURE |
| FR-04 (Professional doc) | 3d | LATEX-02 | TEST-15 | USER_GUIDE |
| FR-05 (LaTeX) | 3d | LATEX-01..08 | TEST-15 | PRD |
| FR-06 (PDF) | 3d | IMPL-pdf | TEST-15 | USER_GUIDE |
| NFR-04 (No secrets) | 1 | ARCH-10 | TST-sec | DEVELOPER_GUIDE |
| NFR-11 (Coverage) | 4 | TEST-00..21 | All | DEVELOPER_GUIDE |
| TR-01 (Python 3.11) | 1 | ARCH-02 | Env test | README |
| TR-05 (Pydantic) | 2 | ARCH-07 | TEST-13 | DEVELOPER_GUIDE |

---

## Appendix B: Glossary of Project Terms

| Term | Definition |
|------|------------|
| **Agent** | A CrewAI AI agent with a defined role, goal, backstory, and tool set |
| **Crew** | A collection of agents working toward a common goal in CrewAI |
| **Pipeline** | The sequential execution of all stages from topic to PDF |
| **Quality Gate** | An automated checkpoint that blocks pipeline progress if criteria are unmet |
| **Hallucination** | An AI-generated claim that is factually incorrect or unverifiable |
| **BibTeX** | The standard bibliography format used with LaTeX |
| **Traceability** | The ability to trace every output artifact back to its generating input and agent |
| **Confidence Score** | A 0.0–1.0 numeric assessment of a claim's verifiability |
| **Sub-crew** | A specialized crew operating within the main pipeline for a specific phase |
| **Domain Model** | A Pydantic BaseModel representing a core business entity |

---

## Appendix C: Quick Reference Checklist

Use this checklist for final submission validation.

### Code Quality
- [ ] `make install` succeeds on clean virtualenv
- [ ] `make run` completes; PDF produced
- [ ] `make test` passes; coverage ≥85%
- [ ] `make lint` exits 0
- [ ] `mypy --strict` exits 0
- [ ] `pydocstyle` passes
- [ ] `gitleaks` scan clean
- [ ] Pre-commit hooks pass on all files

### Deliverables
- [ ] D-01: Source code complete
- [ ] D-02: LaTeX source present
- [ ] D-03: PDF ≥20 pages
- [ ] D-04: `.bib` file complete
- [ ] D-05: README.md
- [ ] D-06: docs/PRD.md
- [ ] D-07: docs/PLAN.md
- [ ] D-08: docs/TODO.md (this file)
- [ ] D-09: docs/ARCHITECTURE.md
- [ ] D-10: docs/RESEARCH.md
- [ ] D-11: docs/USER_GUIDE.md
- [ ] D-12: docs/DEVELOPER_GUIDE.md
- [ ] D-13: tests/ with coverage report
- [ ] D-14: evaluation/ with all reports
- [ ] D-15: Submission archive

### Quality
- [ ] ≥20 verified sources
- [ ] 0 critical hallucinations
- [ ] Readability ≥60
- [ ] 100% citation match
- [ ] All quality gates passed
- [ ] QA report signed

### Excellence (target as many as possible)
- [ ] E-08: Reproducibility appendix in PDF
- [ ] E-01: Multi-pass refinement loop
- [ ] E-02: Agent analytics dashboard
- [ ] E-03: Citation confidence scoring
- [ ] E-05: Hallucination detection pipeline
- [ ] E-09: Agent collaboration diagram

---

*This document is maintained as the single source of truth for the entire project. Every task completion should be reflected by updating the relevant checkbox or status. The document version should be incremented on every significant update.*

**Document Version:** 1.0.0
**Last Updated:** Project initiation
**Owner:** Lead Architect / Project Manager
**Review Cadence:** End of each phase

---

*End of TODO.md*
