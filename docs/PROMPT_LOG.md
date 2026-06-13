# Prompt Engineering Log

This log details the iterative prompt engineering process used to refine the multi-agent pipeline and achieve consistent, high-quality output without hallucinations or LaTeX formatting errors.

## Iteration 1: The Monolithic Baseline
- **Initial Prompt**: `Write a 15-page academic book on Generative AI, specifically VAEs and Diffusion Models, including LaTeX formatting, mathematical formulas, and a bibliography.`
- **Context**: Zero-shot prompt to GPT-4o.
- **Expected Output**: A fully-fledged book with code, figures, math, and real citations.
- **Result**: FAILED. The output was roughly 4,500 words. It hallucinated references. The mathematical formulas were poorly aligned and occasionally syntactically invalid for LaTeX compilation. It completely failed to provide correct BibTeX format.

## Iteration 2: Breaking Down Tasks (CrewAI Setup)
- **Prompt (Research Agent)**: `Find academic papers on VAEs and Diffusion models. Extract key facts.`
- **Result**: Improved research, but the Writer Agent still hallucinated when integrating the facts.
- **Improvement**: Implemented a dedicated **Fact Verification Agent**.
- **Prompt (Fact Verification Agent)**: `Review the research sources. Verify factual claims by cross-referencing against at least 2 independent sources using your tools. Output a structured verification report.`
- **Result**: Hallucinations plummeted. However, citations in the text didn't map perfectly to the bibliography.

## Iteration 3: Standardizing Citations and Mathematics
- **Problem**: The Writer Agent used plain text for math (e.g. `loss = ELBO`) instead of proper LaTeX (`$\mathcal{L} = \text{ELBO}$`).
- **Prompt Update (Writer Agent)**: 
  > "You are an Expert Technical Writer. You must use precise LaTeX mathematical notation for all formulas. Always wrap inline math in `\(` and `\)` and block math in `\[` and `\]` or `\begin{equation}`. When citing, use `\cite{author_year}` format exactly matching the bibliography list."
- **Result**: LaTeX compilation succeeded much more frequently.

## Iteration 4: The BiDi (Hebrew/English) Challenge
- **Problem**: When instructing the Writer Agent to write a chapter in Hebrew about the intuition of VAEs, the RTL/LTR mixing broke XeLaTeX compilation, especially around English acronyms and math mode variables.
- **Prompt Update (Information Architect)**: 
  > "Design Chapter 7 to be an intuitive explanation written natively in Hebrew. Ensure the structural flow works for an RTL audience."
- **Prompt Update (Typesetting Agent)**:
  > "Do NOT attempt to use `\LRE{}` on math blocks. Only use it for English acronyms."
- **Result**: The Typesetting Agent struggled to consistently apply the regex rules.
- **Pivot/Best Practice**: Move complex regex protection out of the LLM prompt and into a deterministic Python post-processing script (`aux_processor.py`). LLMs are bad at precise regex applications.

## Iteration 5: Quality Gate Rigidity
- **Problem**: Agents would sometimes output conversational text ("Here is your BibTeX file:").
- **Prompt Update (Citation Agent)**: 
  > "CRITICAL OUTPUT FORMAT RULES: Output ONLY raw BibTeX entries. Do NOT include any markdown, explanations, backticks, or commentary."
- **Result**: Perfect BibTeX files. This strict negative prompting is essential for generation tasks that feed directly into a compiler.

## Key Learnings & Best Practices
1. **Negative Prompting is Critical**: For compiler-bound outputs, telling the LLM exactly what *not* to do (e.g., "no conversational filler") is as important as telling it what to do.
2. **Deterministic Scripts > LLM Formatting**: Do not use the LLM to format TOC dots or protect math with BiDi tags. Use Python scripts for strict formatting operations on the LLM's generated content.
3. **Fact-Checking Requires Isolation**: The Fact Verification Agent performs best when it is NOT the one writing the content. Separation of concerns prevents "confirmation bias" in the LLM.
