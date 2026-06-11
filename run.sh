#!/usr/bin/env bash
# Equivalent to 'make run'
mkdir -p output/latex/figures
uv run python scripts/generate_graph.py
uv run python -m crewai_book run
uv run python scripts/clean_tex.py output/latex/book.tex
