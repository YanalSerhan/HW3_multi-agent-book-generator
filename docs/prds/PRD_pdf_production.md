# PRD: PDF Production Mechanism

## 1. Background
Once the LaTeX `.tex` files are generated, the system must autonomously invoke the local LaTeX distribution (XeLaTeX) to compile the source into a `.pdf` file. This process is error-prone and requires multiple passes.

## 2. Requirements
- **XeLaTeX Engine**: Must use `xelatex` because of its native UTF-8 and `polyglossia` support for bidirectional text.
- **Multi-Pass Compilation**: Must run at least 3 passes to ensure Table of Contents, Lists of Figures, and Cross-References resolve correctly.
- **Biber Integration**: Must run `biber` between the first and second XeLaTeX passes to generate the bibliography.
- **Subprocess Isolation**: The compiler must run in a secure Python `subprocess` with captured `stdout` and `stderr`.
- **Timeout & Retries**: Compilation must timeout after 60 seconds to prevent infinite loops (e.g., waiting for user input on error). If an error occurs, the system should retry up to 3 times before failing.

## 3. Workflow
1. `xelatex -interaction=nonstopmode book.tex`
2. `biber book`
3. Run `aux_processor.py` (fixes BiDi TOC issues)
4. `xelatex -interaction=nonstopmode book.tex`
5. `xelatex -interaction=nonstopmode book.tex`

## 4. Test Scenarios
- **Compilation Timeout Test**: Pass a LaTeX file containing `\read\temp` (which normally halts and waits for input) and ensure the subprocess times out and recovers.
- **Syntax Error Trace Extraction**: Pass an invalid LaTeX file and ensure the error message is correctly parsed from the `.log` file and returned to the pipeline for the Quality Control agent to analyze.
