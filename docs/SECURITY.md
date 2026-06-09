# Security Requirements & Practices

This document outlines the security architecture and requirements implemented in the CrewAI Multi-Agent Book Generator.

## 1. Secrets Management
- **Environment Isolation**: All configuration is driven through a `.env` file that is explicitly ignored in `.gitignore`.
- **Placeholder Example**: Developers should use `.env.example` to understand the required API keys. Real keys must never be committed.
- **Pydantic SecretStr**: Within the application runtime (`src/crewai_book/config/settings.py`), all sensitive strings (like `OPENAI_API_KEY` and `SERPER_API_KEY`) are stored as `pydantic.SecretStr`. This prevents accidental logging or `print()` exposure since it requires `.get_secret_value()` to extract the raw key.

## 2. Pre-Commit Verification
- **Gitleaks**: The project utilizes `gitleaks` as a pre-commit hook to scan all staged files for hardcoded secrets, passwords, or API keys before they can be committed to the repository.

## 3. Input Sanitization
- **LaTeX Escaping**: Untrusted agent outputs or user inputs that are injected directly into LaTeX templates are sanitized using the `sanitize_latex()` utility found in `src/crewai_book/utils/sanitize.py`. 
- This utility neutralizes potentially dangerous LaTeX macros by safely escaping `&`, `%`, `$`, `#`, `_`, `{`, `}`, `~`, `^`, and `\`.

## 4. API Request Safety
- **Timeouts**: All HTTP clients making outbound network requests are configured with strict timeouts to prevent unbounded requests or denial-of-service hangs.
- **Rate Limit Back-Pressure**: The `ApiGatekeeper` queue controls outbound volume to ensure we do not overwhelm downstream services or incur unexpected massive bills.

## 5. Security Scan Results

A static application security testing (SAST) scan was performed using `ruff` with the `flake8-bandit` (`S`) plugin (`uv run ruff check src --select S`). The scan identified 8 warnings, all of which have been reviewed and classified as **accepted risks/false positives** due to the specific nature of this application:

### Accepted Risks
1. **Jinja2 Autoescape False (S701)**: Found in `latex/renderer.py`, `services/latex_service.py`, and `workflows/pipeline.py`. 
   * **Rationale**: The Jinja2 templates are used to generate LaTeX (`.tex`) code, not HTML. Standard HTML autoescaping would break LaTeX syntax. Instead, we use a custom `sanitize_latex()` function to neutralize dangerous LaTeX macros before rendering.
2. **Subprocess Call (S603 & S607)**: Found in `sdk/latex_client.py` and `tools/figure_generator_tool.py`.
   * **Rationale**: The application legitimately needs to execute system processes (`pdflatex`, `biber`, and `python`) to compile the book and generate figures. The inputs to these commands are controlled (e.g., specific generated `.tex` files) and run with strict timeouts (`timeout=90.0`) to prevent hanging.

**Scan Conclusion**: The codebase is secure against our threat model. No critical vulnerabilities or exposed secrets were found.
