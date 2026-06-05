"""SDK layer — external service wrappers.

This package wraps all external services (LLM providers, search APIs,
LaTeX compiler) behind stable interfaces. No other layer may import
from external libraries directly; they must go through SDK abstractions.
"""
