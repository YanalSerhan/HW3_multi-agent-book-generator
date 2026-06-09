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
