# Ablation Study

**Experiment Goal:** Determine the contribution of specific agents and quality gates to the final book quality by selectively disabling them.

## Experimental Setup

Topic: "The History of Artificial Intelligence"
Model: GPT-4o
Three variants of the pipeline were run:
1. **Full Pipeline** (Control)
2. **No Fact Verification Agent** (Fact-Checker removed)
3. **No Editorial Crew** (Editor and Reviewer removed, Writer goes straight to LaTeX)
4. **No Quality Gates** (Pipeline runs without intermediate checks and retries)

## Results

| Variant | Hallucination Rate | Readability Score | Flow & Cohesion | LaTeX Compile Rate |
|---------|--------------------|-------------------|-----------------|--------------------|
| **Full Pipeline** | 0.00% | 65.4 | Excellent | 100% |
| **No Fact-Checker** | 3.2% | 66.1 | Excellent | 100% |
| **No Editorial Crew** | 0.00% | 42.5 | Poor (Fragmented) | 80% (Syntax errors) |
| **No Quality Gates**| 1.5% | 58.2 | Moderate | 60% (Missing citations)|

## Observations

### Removing the Fact Verification Agent
When the `FactVerificationAgent` was removed, the `WriterAgent` occasionally invented dates or conflated distinct AI models (e.g., confusing aspects of GPT-2 and GPT-3). The hallucination rate jumped to 3.2%. While structurally fine, the academic integrity of the document was severely compromised.

### Removing the Editorial Crew
Without the `EditorAgent` and `ReviewerAgent`, the resulting book felt like a disjointed collection of Wikipedia articles. The `WriterAgent` generates sections individually, meaning transitions between chapters were abrupt. Additionally, without the Editor enforcing LaTeX macro constraints, the LaTeX compilation failed 20% of the time due to unescaped characters (`&`, `%`, `$`).

### Removing Quality Gates
The Quality Gates (implemented in `quality_gates.py`) act as critical safety nets. Without them, the pipeline does not retry failed stages. As a result, the pipeline occasionally produced books that were only 12 pages long (failing QG-9) or had missing bibliography entries (failing QG-7), which caused LaTeX compilation failures.

## Conclusion
Every specialized agent provides a non-overlapping benefit to the pipeline. The **Fact Verification Agent** is critical for academic integrity, the **Editorial Crew** is essential for narrative flow and syntax safety, and the **Quality Gates** are indispensable for reliability and autonomous self-correction.
