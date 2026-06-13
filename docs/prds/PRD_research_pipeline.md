# PRD: Research Pipeline Mechanism

## 1. Background
To ensure the generated book is grounded in academic reality and has zero hallucinated citations, the Research Pipeline Mechanism orchestrates the discovery and verification of knowledge before any drafting begins.

## 2. Requirements
- **Tool Access**: The pipeline must provide agents with `arxiv_search` and `web_search` (Serper) tools.
- **Corpus Generation**: Must generate a structured Markdown corpus containing at least 15 verified academic sources.
- **Deduplication**: Must ensure no duplicate DOIs or identical papers are included in the corpus.
- **Fact Verification**: A dedicated `FactVerificationAgent` must cross-reference claims against multiple sources. If a claim cannot be verified, it must be flagged or discarded.
- **BibTeX Output**: A dedicated `CitationAgent` must convert the verified sources into a strictly formatted `.bib` file.

## 3. Quality Gates
The research pipeline is heavily guarded by Quality Gates:
- **QG-1 (Source Count)**: The final `.bib` file must contain $\ge 15$ entries.
- **QG-2 (Hallucinations)**: The `FactVerificationAgent` must report 0 unverified critical claims.

## 4. Test Scenarios
- **Missing DOI Resolution**: Provide the system with a broken or hallucinated DOI and verify that the `FactVerificationAgent` flags it and drops it from the corpus.
- **Duplicate Detection**: Provide two identical papers (one from ArXiv, one from a journal URL) and ensure the system consolidates them into a single `.bib` entry.
