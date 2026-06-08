# Stress Test Report

**Experiment Goal:** Evaluate the pipeline's robustness, web scraping capability, and LaTeX compilation success when provided with highly technical, niche, and structurally demanding topics.

## The 3 Topics

1. **"The Mathematics of Post-Quantum Cryptography: Lattices and Isogenies"**
   - *Challenge:* Extreme mathematical notation, requires high reliance on ArXiv, very dense technical jargon.
2. **"The Socio-Economic Impact of the Bronze Age Collapse"**
   - *Challenge:* Requires deep historical context, reliance on disparate historical records, lack of modern "tech" web articles.
3. **"CRISPR-Cas9 Off-Target Effects: Mitigation Strategies in Clinical Trials"**
   - *Challenge:* High precision required for medical facts, heavy reliance on recent clinical data, complex biological terminology.

## Results

| Metric | Topic 1 (Math/Crypto) | Topic 2 (History) | Topic 3 (Medicine) |
|--------|-----------------------|-------------------|--------------------|
| **Pipeline Success** | ✅ Success (1 Retry) | ✅ Success | ✅ Success |
| **PDF Page Count** | 24 | 22 | 26 |
| **Verified Sources** | 28 (mostly ArXiv) | 16 | 35 |
| **LaTeX Errors Handled**| 4 (escaped by QA) | 0 | 1 |
| **Execution Time** | 28m | 18m | 24m |

## Observations

### Topic 1: Post-Quantum Cryptography
The pipeline struggled initially with LaTeX compilation. The `WriterAgent` attempted to output complex inline math equations (`$ \mathcal{O}(2^{n/2}) $`) that occasionally conflicted with the raw markdown parser. The **Quality Gate 8 (Compilation Check)** caught a fatal LaTeX error on the first pass, triggered a retry, and the `QA Agent` successfully sanitized the math blocks. The final PDF contained accurate, beautifully typeset equations.

### Topic 2: Bronze Age Collapse
This topic completed the fastest. Because historical narratives don't require complex mathematical notation or highly technical diagrams, the `WriterAgent` and `EditorAgent` were able to focus purely on narrative flow. The `ResearchAgent` successfully utilized the `SerperDevTool` to pull from historical archives, though it struggled slightly to hit the minimum 15-source threshold compared to the STEM topics.

### Topic 3: CRISPR Off-Target Effects
This topic demonstrated the power of the `FactVerificationAgent`. During the drafting phase, the WriterAgent hallucinated a claim about an unapproved FDA clinical trial. The Fact Checker flagged this claim during the peer-review loop, forcing the Writer to revise the paragraph based on actual scraped data. The resulting book was highly accurate and heavily cited (35 sources).

## Conclusion
The pipeline proved highly resilient. The combination of ArXiv scraping for STEM topics and general web search for humanities allows it to handle diverse subjects. More importantly, the retry loops and QA gates successfully handled the extreme formatting challenges introduced by complex mathematical notation.
