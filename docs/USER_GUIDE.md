# User Guide: CrewAI Autonomous Academic Publisher

Welcome to the CrewAI Autonomous Academic Publisher. This system autonomously researches, writes, fact-checks, and typesets complete academic books using a multi-agent AI architecture.

## Getting Started

### 1. Installation
Ensure you have Python 3.11+ and the `uv` package manager installed. You also need a working LaTeX distribution (TeX Live or MacTeX) that provides `xelatex` and `biber`.

Clone the repository and install dependencies:
```bash
git clone https://github.com/YanalSerhan/HW3_multi-agent-book-generator.git
cd HW3_multi-agent-book-generator
uv sync
```

### 2. Configuration
Create a `.env` file in the root directory to provide your LLM API keys:
```env
OPENAI_API_KEY=sk-your-key-here
```
You can also adjust the book length and defaults in `config/settings.json`.

### 3. Generating a Book
To run the full pipeline, use the provided Typer CLI interface. You can specify the topic and output directory:

```bash
uv run python -m crewai_book run --topic "Generative AI: Variational Autoencoders and Diffusion Models" --output-dir "final_submission"
```

## Typical User Workflow
1. **Initialization**: The CLI kicks off the pipeline, initializing the 11 agents.
2. **Research Phase**: The Research Crew queries the ArXiv API and web search to gather sources and verify facts. You will see console output detailing the hallucination checks.
3. **Drafting Phase**: The Writer Crew drafts chapters based on the Information Architect's outline.
4. **Editorial Phase**: The Editorial Crew reviews the manuscript, running Flesch readability checks.
5. **Typesetting & Compilation**: The Typesetting Specialist formats the text, extracts the Jupyter notebook, and runs the BiDi LaTeX post-processor.
6. **Completion**: The final `book.pdf` is saved to your specified output directory.

## Command Line Options
- `-t, --topic TEXT`: The subject of the book.
- `-o, --output-dir TEXT`: Directory to store the output PDF and intermediate LaTeX/Markdown files.
- `--fast`: Use an optimized, cheaper model configuration (e.g., GPT-4o-mini) for rapid testing.

## Troubleshooting & FAQ

**Q: The compilation failed with a LaTeX error.**
A: Check the logs in the output directory. LaTeX errors are often caused by unescaped special characters. The system has 5 automatic retry attempts, but if it fails completely, you can manually fix the `.tex` file in the output directory and run `xelatex book.tex`.

**Q: The TOC page numbers are on the left instead of the right.**
A: This means the BiDi post-processor did not run correctly. Ensure you are running the entire pipeline, which automatically executes `aux_processor.py` between XeLaTeX passes.

**Q: I hit an API rate limit.**
A: The system uses an `ApiGatekeeper` that will automatically pause and retry with exponential backoff. Do not interrupt the process; it will recover on its own.
