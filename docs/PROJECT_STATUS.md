# Project Status

## 1. WHERE WE ARE

### Recent Commits (origin/main)

| Hash | Author | Message |
|------|--------|---------|
| `c2f53b2` | Nell Khoury | test: offline validation of rendering pipeline — provenance, telemetry, BiDi compile |
| `7347592` | Nell Khoury | feat: add production telemetry appendix and execution metrics logging |
| `07a1d08` | Nell Khoury | feat: source provenance footnotes — in-line claim auditing |
| `40f7f43` | Nell Khoury | feat: content spec compliance — configurable length and topic-specific Hebrew BiDi chapter |
| `935e1d7` | Nell Khoury | feat: sandbox figure-generation tool — import allowlist, timeout, isolated execution |
| `9b02d13` | Nell Khoury | fix: stabilize pipeline — CI repair, LaTeX metadata via config with proper escaping |
| `1c39e3a` | Nell Khoury | feat: add macOS support and repository hygiene |
| `d69922f` | YanalSerhan | feat: implement multi-agent book generation pipeline with automated LaTeX rendering and quality assurance workflows |
| `d1d9858` | YanalSerhan | feat: implement multi-agent book generation system with workflows, quality gates, and agent orchestration |
| `0459087` | YanalSerhan | feat: initialize multi-agent book generator system with agent framework, workflows, and CLI support |

### What Works Today
- **Green CI:** The test suite and linting are strictly enforced and currently fully passing.
- **Sandboxed Figure Execution:** Python code execution for matplotlib graph generation is isolated and secured against arbitrary execution.
- **Config-Driven Features:** Book metadata, length, Hebrew-chapter injection, provenance footnotes, and telemetry are all centrally controlled.
- **Offline-Validated Rendering Chain:** The complete XeLaTeX + biber + BiDi compilation sequence has been verified locally using fixture data, including fixing a complex `hyperref`/`bidi`/`polyglossia` preamble loading-order conflict.
- **Runbook Exists:** `docs/RUN_INSTRUCTIONS.md` clearly outlines how to execute smoke tests and full runs.

---

## 2. ASSIGNMENT COMPLIANCE MAP

| Requirement | Status | Implementation Reference |
|-------------|--------|--------------------------|
| ~15 pages | **WIRED-AWAITING-RUN** | `config/settings.json` (chapter count & words/section) |
| Cover page | **DONE** | `src/crewai_book/latex/templates/book.tex.j2` (`\maketitle`) |
| TOC + headers/footers | **DONE** | `src/crewai_book/latex/templates/preamble.tex` & `book.tex.j2` |
| Image | **WIRED-AWAITING-RUN** | `FigureAgent` prompted to generate and save PNGs |
| Python-generated graph | **WIRED-AWAITING-RUN** | Sandboxed tool (`src/crewai_book/tools/figure_generator_tool.py`) |
| Table | **WIRED-AWAITING-RUN** | Added to `WriterAgent` prompt instructions |
| Math formula | **WIRED-AWAITING-RUN** | Handled natively by LaTeX + writer instructions |
| Hebrew-English BiDi chapter | **WIRED-AWAITING-RUN** | Injected via `EditorialCrew` prompt specifically for VAE → Diffusion |
| Linked bibliography | **DONE** | Provenance footnote extraction to `biblatex` in `renderer.py` |

*Note: Items marked **WIRED-AWAITING-RUN** are fully implemented in the pipeline's logic and prompts, but require an active LLM run to produce the final artifacts.*

---

## 3. WHAT'S LEFT

- [ ] Smoke run (~$0.25, 5 min) — human-triggered, see `docs/RUN_INSTRUCTIONS.md`
- [ ] QA smoke PDF against compliance map (10 min)
- [ ] Full run (~$3, 15 min) — human-triggered
- [ ] QA final PDF: page count, Hebrew content quality, click every citation, no raw PROVENANCE markers, telemetry appendix renders (20 min)
- [ ] Commit final book artifacts (output_final PDF + tex + bib)
- [ ] Final docs: spec sheet with REAL run numbers (tokens/cost/runtime from telemetry), README polish (20 min)
- [ ] Submission sanity check with Yanal
