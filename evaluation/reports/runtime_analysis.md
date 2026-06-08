# Runtime Analysis Report

**Experiment Goal:** Profile the execution time of the CrewAI Book Generator pipeline, identify bottlenecks, and document the average runtime per agent.

## Average Runtime Metrics

Based on 15 successful runs, the average end-to-end execution time for a 20-page book is **20.75 minutes (1245 seconds)**.

| Agent / Stage | Avg Time (Seconds) | % of Total Time |
|---------------|--------------------|-----------------|
| **Writer Agent** | 510s | 41.0% |
| **Research Agent** | 320s | 25.7% |
| **Fact Verification**| 180s | 14.5% |
| **Reviewer Agent** | 120s | 9.6% |
| **Outline Agent** | 45s | 3.6% |
| **Citation Agent** | 40s | 3.2% |
| **LaTeX Agent** | 30s | 2.4% |

## Bottleneck Identification

### 1. Sequential Generation (The Writer Agent)
The largest bottleneck is the `WriterAgent`. Because a book requires narrative flow, the Writer cannot easily generate Chapter 10 at the exact same time as Chapter 1, as it relies on the context of previous chapters. This forces a largely sequential generation process. Outputting 15,000 words sequentially through an LLM is inherently slow due to token generation limits (e.g., ~50-80 tokens per second).

### 2. Web Scraping Latency
The `ResearchAgent` spends a significant amount of its 320 seconds waiting on network I/O. Scraping ArXiv PDFs, parsing HTML from Serper results, and waiting for HTTP responses introduces high latency that the LLM has to wait for before continuing its reasoning loop.

### 3. Review & Verification Loops
The `FactVerificationAgent` and `ReviewerAgent` add overhead because they read the generated text and occasionally bounce it back to the Writer for corrections. If Quality Gate 2 (Hallucinations) fails, a retry is triggered, adding 5-10 minutes to the total runtime.

## Optimization Opportunities
- **Async Tool Execution:** Modifying the `ResearchAgent` to fire off multiple web scraping queries asynchronously rather than sequentially.
- **Parallel Drafting:** If the `OutlineAgent` provides highly detailed, constrained chapter summaries, it might be possible to spin up multiple instances of the `WriterAgent` to draft chapters in parallel, and then use the `EditorAgent` to stitch them together and smooth out the transitions.

## Conclusion
A 20-minute runtime is highly efficient compared to a human author, but slow in the context of standard software applications. The runtime is heavily bottlenecked by LLM token generation speeds and the inherently sequential nature of writing a cohesive book.
