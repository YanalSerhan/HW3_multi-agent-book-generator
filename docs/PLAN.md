# Architecture and Implementation Plan

## CrewAI Multi-Agent LaTeX Book/Article Generator

**Version:** 1.0.0
**Status:** Approved
**Last Updated:** 2026-06-05
**Owner:** Yanal Serhan

---

## 1. Architecture Philosophy

This project follows a **layered, domain-driven architecture** with strict separation of concerns:

- **No layer may bypass the one below it.** Agents call Services; Services call SDK; SDK calls external APIs.
- **All external dependencies are wrapped** in SDK abstractions. Swapping an LLM provider or search engine requires changes only in the SDK layer.
- **All data flows through typed Pydantic models.** No raw dictionaries, no `Any` types in public interfaces.
- **Dependency injection everywhere.** No global state; all services receive their dependencies via constructor injection.
- **Fail-fast with recovery.** Errors are domain-specific exceptions with context; recoverable errors trigger automatic retry.

---

## 2. Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Language | Python 3.11+ | Type annotations, `match` statements, performance improvements |
| Agent Framework | CrewAI ≥0.28 | Homework requirement; mature agent orchestration with roles, goals, tools |
| Data Models | Pydantic v2 | Strict validation, serialization, `BaseSettings` for config |
| CLI | Typer + Rich | Modern CLI with auto-help, colored output, progress indicators |
| HTTP Client | httpx | Async-capable, timeout support, modern API |
| Templating | Jinja2 | Proven LaTeX template rendering with filters and macros |
| Logging | Loguru | Structured JSON logging with rotation, filtering, context |
| Readability | textstat | Standard readability metrics (Flesch, Gunning Fog, etc.) |
| Bibliography | bibtexparser | Parse and validate BibTeX files |
| Academic Search | arxiv | Official ArXiv API client |
| Document | LaTeX (memoir class) | Professional book typesetting |
| PDF Compilation | latexmk + pdflatex | Automated multi-pass compilation |
| Testing | pytest + pytest-cov | Industry standard; fixtures, parametrize, coverage |
| Linting | ruff | Fast, comprehensive Python linter and formatter |
| Type Checking | mypy (strict mode) | Static type verification |
| Pre-commit | pre-commit | Automated code quality hooks |

---

## 3. Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                             │
│                   (__main__.py / Typer)                       │
├─────────────────────────────────────────────────────────────┤
│                    Workflow Layer                             │
│            (Crews, Pipeline, Quality Gates)                   │
│         main_crew.py │ research_crew.py │ editorial_crew.py  │
├─────────────────────────────────────────────────────────────┤
│                     Agent Layer                              │
│              (10 CrewAI Agent definitions)                    │
│          Each agent has: role, goal, backstory, tools         │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer                             │
│              (Business logic services)                        │
│    ResearchService │ CitationService │ ContentService         │
│    LaTeXService │ PDFService                                 │
├─────────────────────────────────────────────────────────────┤
│                      SDK Layer                               │
│            (External service wrappers)                        │
│       LLMClient │ SearchClient │ LaTeXClient                 │
├─────────────────────────────────────────────────────────────┤
│                    Domain Layer                              │
│              (Pydantic v2 models)                             │
│   Article │ Chapter │ Section │ Citation │ PipelineState      │
├─────────────────────────────────────────────────────────────┤
│                   Config Layer                               │
│         (Settings, AgentConfigs, .env loading)                │
├─────────────────────────────────────────────────────────────┤
│                 Observability Layer                           │
│           (Logger, Metrics, AgentTracker)                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 Domain Layer

All business entities as Pydantic v2 models with full validation:

- **`Article`**: Root model containing title, authors, abstract, chapters, bibliography, metadata
- **`Chapter`**: Numbered chapter with title, sections, summary
- **`Section`**: Title, content (Markdown), word count, citations
- **`Citation` / `Bibliography`**: Source metadata, BibTeX key, DOI, confidence score
- **`PipelineState`**: State machine tracking current stage, errors, retries, timing
- **`AgentOutput`**: Typed output models for each agent's deliverable

### 3.2 SDK Layer

Three SDK clients, each wrapping external services:

- **`LLMClient`**: Wraps OpenAI/Anthropic API; returns typed responses; tracks token usage
- **`SearchClient`**: Wraps Serper/DuckDuckGo/ArXiv; rate limiting; result caching
- **`LaTeXClient`**: Wraps subprocess calls to `latexmk`/`pdflatex`; timeout; log parsing

All SDK classes:
- Accept injected `Settings` configuration
- Implement `__repr__` for debugging
- Raise only domain-specific exceptions
- Have corresponding mocks in `tests/conftest.py`

### 3.3 Service Layer

Five services containing all business logic:

- **`ResearchService`**: Orchestrates searches, deduplicates, scores relevance
- **`CitationService`**: Validates, formats, and cross-references citations
- **`ContentService`**: Manages article assembly, word count, readability
- **`LaTeXService`**: Renders Jinja2 templates into `.tex` files
- **`PDFService`**: Triggers LaTeX compilation; captures and reports errors

### 3.4 Agent Layer

Ten CrewAI agents with distinct, non-overlapping roles:

| # | Agent | Role | Primary Output |
|---|-------|------|----------------|
| A-01 | Research Agent | Senior Research Scientist | Structured source corpus |
| A-02 | Fact Verification Agent | Critical Fact Checker | Verified facts + hallucination report |
| A-03 | Outline Architect Agent | Information Architect | Hierarchical outline blueprint |
| A-04 | Writer Agent | Expert Technical Writer | Full manuscript |
| A-05 | Editor Agent | Senior Copy Editor | Edited manuscript with improvements |
| A-06 | Reviewer Agent | Peer Reviewer | Structured review report |
| A-07 | Citation Agent | Bibliographer | Clean .bib file + audit report |
| A-08 | LaTeX Formatter Agent | Typesetting Specialist | Compilable LaTeX source tree |
| A-09 | PDF Production Agent | Production QC Specialist | Final PDF |
| A-10 | Quality Assurance Agent | Chief Quality Officer | QA certification report |

### 3.5 Workflow Layer

- **Main Pipeline**: Sequential (`Process.sequential`) — stages 0–10
- **Research Sub-Crew**: Hierarchical (`Process.hierarchical`) — agents A-01, A-02, A-07
- **Editorial Sub-Crew**: Hierarchical — agents A-05, A-06
- **Quality Gates**: 10 automated checkpoints between stages
- **Retry Logic**: Exponential backoff with configurable max attempts
- **Human Checkpoints**: Optional pause points controlled via `.env` flags

---

## 4. CrewAI Design Decisions

### ADR-01: Sequential Main Pipeline with Hierarchical Sub-Crews

**Context:** CrewAI supports both `Process.sequential` and `Process.hierarchical` execution.

**Decision:** Use sequential for the overall pipeline (each stage depends on the previous) and hierarchical within research and editorial phases (agents collaborate within a phase).

**Rationale:** The research phase benefits from a manager LLM coordinating which agent tackles which sub-task. The main pipeline is inherently sequential (you can't write before researching).

### ADR-02: Ten Agents with Distinct Roles

**Context:** Could use fewer agents with broader responsibilities.

**Decision:** Ten specialized agents, each with a narrow, well-defined role.

**Rationale:** Specialization produces better output quality. Each agent's prompt can be deeply optimized for its specific task. More agents also better demonstrate the multi-agent paradigm for evaluation.

### ADR-03: Typed Output Models for All Agents

**Context:** CrewAI agents return string output by default.

**Decision:** All agent outputs are parsed into Pydantic models.

**Rationale:** Type safety ensures downstream agents receive well-structured input. Enables automated quality gate checks. Makes testing significantly easier.

### ADR-04: PipelineState as Shared Context

**Context:** Need to pass data between pipeline stages.

**Decision:** A `PipelineState` Pydantic model is serialized to `output/pipeline_state.json` at each stage boundary.

**Rationale:** Provides persistence (can resume from failure), debugging (inspect state at any point), and reproducibility (same state → same output).

---

## 5. LaTeX Strategy

### 5.1 Template System

- **Document class:** `memoir` — the most powerful LaTeX class for books
- **Template engine:** Jinja2 with custom LaTeX-safe filters
- **Template location:** `src/crewai_book/latex/templates/`
- **Template files:**
  - `book.tex.j2` — Main book template
  - `article.tex.j2` — Alternative article template
  - `preamble.tex` — Shared package imports and configuration

### 5.2 Typography

- **Font:** Palatino (`\\usepackage{palatino}`) — professional book typography
- **Microtype:** Enabled for paragraph-level typographic optimization
- **Line spacing:** 1.5× for readability
- **Color scheme:** Deep navy (#003366) headings, black body text
- **Chapter style:** Decorative but professional (`\\chapterstyle{ell}`)

### 5.3 Bibliography

- **System:** BibLaTeX with Biber backend
- **Style:** APA (author-year) — `\\usepackage[style=apa]{biblatex}`
- **Citation commands:** `\\textcite{key}` and `\\parencite{key}`
- **Validation:** `biber --validate-datamodel` as CI check

### 5.4 Compilation Pipeline

```
pdflatex → biber → makeglossaries → makeindex → pdflatex → pdflatex
```

Or via `latexmk -pdf -bibtex` for automated multi-pass compilation.

---

## 6. Quality Strategy

### 6.1 Quality Gates

Ten automated quality gates between pipeline stages:

| Gate | Stage | Check | On Failure |
|------|-------|-------|------------|
| QG-1 | Research | ≥15 verified sources | Retry (2x) |
| QG-2 | Fact Check | 0 critical hallucinations | Abort |
| QG-3 | Outline | All sections present | Retry |
| QG-4 | Writing | Word count ±10% | Warning |
| QG-5 | Writing | Readability ≥60 | Warning |
| QG-6 | Review | 0 unresolved major concerns | Retry (1 revision) |
| QG-7 | Citation | 100% match rate | Abort |
| QG-8 | LaTeX | Compilation exits 0 | Retry (3 attempts) |
| QG-9 | PDF | ≥20 pages | Abort |
| QG-10 | QA | All critical gates pass | Abort |

### 6.2 Hallucination Prevention

Four-layer detection:
1. Citation existence verification (DOI/URL resolution)
2. Claim cross-verification (≥2 independent sources)
3. Consistency checking (zero-temperature LLM evaluation)
4. Confidence scoring (0.0–1.0 with tier labels)

### 6.3 Testing Strategy

- **Unit tests:** Every agent, tool, service, and domain model
- **Integration tests:** Research pipeline, LaTeX pipeline, citation pipeline, error recovery
- **E2E test:** Full pipeline with mocked LLM (< 5 min)
- **Evaluation tests:** Content quality, citation quality, reproducibility
- **Target coverage:** ≥85%

---

## 7. Implementation Phases

| Phase | Timeline | Goal | Key Deliverables |
|-------|----------|------|-----------------|
| Phase 0 | Day 1 | Analysis | TODO.md, repo skeleton |
| **Phase 1** | **Day 1–2** | **Planning** | **PRD, PLAN, pyproject.toml, Makefile** |
| Phase 2 | Day 2–3 | Architecture | Domain models, SDK, Services, Config, Logging |
| Phase 3 | Day 3–7 | Implementation | Tools, Agents, Workflows, LaTeX templates |
| Phase 4 | Day 7–9 | Testing | All tests written and passing, ≥85% coverage |
| Phase 5 | Day 9–10 | Evaluation | Experiments, benchmarks, metrics |
| Phase 6 | Day 10–11 | Documentation | All docs finalized |
| Phase 7 | Day 11–12 | Submission | Final run, archive, tag |

---

## 8. Risk Mitigation

| Risk | Strategy |
|------|----------|
| LLM hallucinations | Multi-layer detection; fact-check agent; citation cross-reference |
| LaTeX compilation errors | Iterative fixing (5 retries); log parsing; error diagnosis |
| API rate limits | Exponential backoff; local caching; configurable delays |
| Cost overrun | Token tracking; `--fast` mode with GPT-3.5-Turbo for non-critical agents |
| Pipeline timeout | Per-stage timeouts; parallelizable where possible |
| CrewAI breaking changes | Pin exact version; abstract via wrapper classes |
| Poor content quality | Multi-pass editorial loop (Writer → Editor → Reviewer); readability gates |

---

## 9. Decision Log (Architecture Decision Records)

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| ADR-01 | Sequential main pipeline with hierarchical sub-crews | Accepted | 2026-06-05 |
| ADR-02 | Ten agents with distinct roles | Accepted | 2026-06-05 |
| ADR-03 | Typed Pydantic output models for all agents | Accepted | 2026-06-05 |
| ADR-04 | PipelineState as shared context mechanism | Accepted | 2026-06-05 |
| ADR-05 | Hatchling build system (no setup.py) | Accepted | 2026-06-05 |
| ADR-06 | Loguru for structured logging (not stdlib logging) | Accepted | 2026-06-05 |
| ADR-07 | Memoir LaTeX class for book format | Accepted | 2026-06-05 |
| ADR-08 | BibLaTeX + Biber (not natbib + bibtex) | Accepted | 2026-06-05 |
| ADR-09 | Ruff as unified linter and formatter (not black + isort + flake8) | Accepted | 2026-06-05 |
| ADR-10 | Typer for CLI (not argparse or click) | Accepted | 2026-06-05 |

### ADR-05: Hatchling Build System

**Context:** Need a build backend for `pyproject.toml`.
**Decision:** Use Hatchling (PEP 517 compliant, simple, well-supported).
**Rationale:** No `setup.py` needed; clean `pyproject.toml`-only configuration.

### ADR-06: Loguru for Structured Logging

**Context:** Need structured JSON logging with per-agent context.
**Decision:** Use Loguru instead of stdlib `logging`.
**Rationale:** Loguru provides structured JSON output, lazy formatting, context binding (agent name, task ID), and simpler API than stdlib. Single-line setup.

### ADR-07: Memoir LaTeX Class

**Context:** Need a LaTeX document class for book-format output.
**Decision:** Use `memoir` class.
**Rationale:** Most powerful book class; supports chapter styles, custom headers, marginal notes, indices, glossaries. More flexible than `book` or `scrbook`.

### ADR-08: BibLaTeX + Biber

**Context:** Need bibliography management in LaTeX.
**Decision:** Use BibLaTeX with Biber backend instead of natbib + BibTeX.
**Rationale:** BibLaTeX is the modern standard; full Unicode support; more citation styles; data model validation; cleaner error messages.

### ADR-09: Ruff as Unified Tool

**Context:** Need linting and formatting tools.
**Decision:** Use Ruff for both linting (replaces flake8, isort, pyupgrade) and formatting (replaces black).
**Rationale:** 10–100× faster than alternatives; single tool; consistent configuration in `pyproject.toml`.

### ADR-10: Typer for CLI

**Context:** Need a CLI framework.
**Decision:** Use Typer (built on Click) with Rich integration.
**Rationale:** Auto-generates `--help`; type annotations as CLI parameter definitions; Rich integration for colored output; simpler than raw Click or argparse.

---

*End of PLAN.md*
