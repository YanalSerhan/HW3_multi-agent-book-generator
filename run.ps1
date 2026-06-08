# Equivalent to 'make run'
New-Item -ItemType Directory -Force -Path output\latex\figures | Out-Null
uv run python scripts\generate_graph.py
uv run python -m crewai_book run
uv run python scripts\clean_tex.py output\latex\book.tex
