# Developer Guide

Welcome to the CrewAI Book Generator! This guide will help you understand the architecture, environment setup, and extension points of the system.

## Architecture Overview
The system is built on top of `CrewAI` and orchestrates 11 specialized agents. The source code is organized into distinct domains:
- **`agents/`**: Defines the `Agent` classes and their roles/backstories.
- **`workflows/`**: Connects agents into `Crew` pipelines (e.g., `research_crew.py`, `editorial_crew.py`).
- **`tools/`**: Custom tools (e.g., notebook extractors, arxiv searchers).
- **`latex/`**: The core LaTeX rendering engine and the BiDi post-processor.
- **`shared/`**: Utilities like the `gatekeeper.py` for API rate-limiting.

## Local Environment Setup
We strictly use `uv` for dependency management.

1. Install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Sync dependencies:
```bash
uv sync
```

3. Setup environment variables:
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Add your `OPENAI_API_KEY`.

4. Run the test suite:
```bash
uv run pytest
```

## Adding a New Agent
1. Create a new file in `src/crewai_book/agents/` (e.g., `translation_agent.py`).
2. Define the agent's role, goal, and backstory. Give it specific tools if necessary.
3. Integrate the agent into a workflow in `src/crewai_book/workflows/`. Assign it a `Task` and connect the context from previous tasks.

## Modifying the LaTeX Template
The system uses the `memoir` class for book typesetting. If you need to change margins, fonts, or TOC behavior, modify the template strings inside `src/crewai_book/latex/` or the Jinja templates if applicable.
Note: Any changes to RTL/LTR handling must be tested against the `aux_processor.py` to ensure TOC dot leaders don't break.

## Quality Gates
The pipeline enforces 10 Quality Gates located in `src/crewai_book/workflows/quality_gates.py`. If you change the target word count or citation requirements, update `config/settings.json` and ensure the quality gates reflect the new thresholds.
