# Run Instructions: CrewAI Book Generator

This runbook provides the exact steps to execute the pipeline locally, ensuring no unexpected costs and predictable behavior. You are in control of the API keys and the execution.

## 1. Environment Setup

Before running, ensure your environment is fully prepared:

```bash
# 1. Activate the python environment
uv sync
source .venv/bin/activate

# 2. Export your OpenAI API key (REQUIRED for any run)
export OPENAI_API_KEY="sk-..."
```

## 2. Configuration Toggles

The pipeline behavior is controlled by `config/settings.json`. To toggle between a smoke test and a real run, adjust the `book_params` block:

**Smoke Test Config (Fast, Cheap):**
```json
"book_params": {
    "topic": "From VAEs to Diffusion Models",
    "target_audience": "Graduate students in Computer Science",
    "chapter_count": 2,
    "words_per_section": 50
}
```

**Real Run Config (Full Quality):**
```json
"book_params": {
    "topic": "From VAEs to Diffusion Models",
    "target_audience": "Graduate students in Computer Science",
    "chapter_count": 8,
    "words_per_section": 300
}
```

*Note: Ensure `cover_metadata` matches your student ID and information.*

## 3. Execution Commands

### Phase A: Smoke Test
Always run this first to ensure the API key is valid and all agents compile successfully. Expected cost is < $0.25.

```bash
uv run -m crewai_book --output output_smoke
```
*Verify: Check `output_smoke/latex/book.pdf`. Ensure the Hebrew block renders and the telemetry appendix is present.*

### Phase B: The Real Run
Once the smoke test is green, update `settings.json` to the real config, then run:

```bash
uv run -m crewai_book --output output_final
```
*Note: This will take several minutes. Expected cost is ~$2-4.*

## 4. Monitoring the Run

While the pipeline is running, you can monitor its progress in two ways:
1. **Console Output**: Watch the agent thoughts and tool calls stream in real-time.
2. **Log File**: A detailed execution log is saved in `output_final/logs/pipeline.log`. You can tail this file in a separate terminal window:
   ```bash
   tail -f output_final/logs/pipeline.log
   ```

## 5. Artifact Submission Checklist

After `output_final` finishes successfully, submit the following files to Dr. Segal:

1. `output_final/latex/book.pdf` (The main deliverable with TOC, Hebrew chapter, Table, Mathematical formula, Bibliography, Telemetry Appendix, and Provenance Footnotes).
2. `output_final/manuscript.md` (The raw markdown for auditability).
3. `output_final/latex/figures/` (Ensure the matplotlib-generated figure PNG is included if submitting source files).
4. `config/settings.json` (Your specific pipeline configuration).
