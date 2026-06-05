# Product Requirements Document (PRD)

## CrewAI Multi-Agent LaTeX Book/Article Generator

**Version:** 1.0.0
**Status:** Approved
**Last Updated:** 2026-06-05
**Owner:** Yanal Serhan

---

## 1. Executive Summary

This project delivers a **production-grade multi-agent AI system** powered by **CrewAI** that autonomously generates a professional, publication-quality book on a selected technical topic. The system orchestrates 10 specialized AI agents — researchers, writers, editors, fact-checkers, and formatters — that collaborate through a structured pipeline to produce a fully formatted **PDF document** compiled from **LaTeX** source, backed by verified citations, multi-pass editorial review, and a reproducible software pipeline.

The result is a complete, reader-ready book that demonstrates sophisticated agent collaboration, rigorous research methodology, and professional-grade typesetting.

---

## 2. Problem Statement

Creating high-quality technical publications is a labor-intensive process requiring multiple specialized skills: research, writing, editing, fact-checking, citation management, and typesetting. Each discipline requires deep domain expertise, and the coordination between them introduces additional complexity.

Current AI writing tools produce content through monolithic single-prompt generation, resulting in:
- Shallow treatment of complex topics
- Hallucinated citations and unverified claims
- Inconsistent voice, terminology, and quality across sections
- No editorial review or quality assurance
- Raw text output without professional formatting

This project solves these problems by decomposing the publication process into specialized agent roles that mirror a real publishing team, connected by quality gates that enforce standards at every stage.

---

## 3. Goals and Non-Goals

### 3.1 Goals

| ID | Goal |
|----|------|
| G-01 | Demonstrate sophisticated multi-agent collaboration using CrewAI |
| G-02 | Produce a ≥20-page professionally typeset PDF book on a technical topic |
| G-03 | Achieve zero hallucinated citations through systematic fact-checking |
| G-04 | Build a reproducible, well-tested, well-documented pipeline |
| G-05 | Exceed all homework requirements and engineering guidelines |
| G-06 | Produce content that is genuinely educational and valuable to readers |

### 3.2 Non-Goals

| ID | Non-Goal | Rationale |
|----|----------|-----------|
| NG-01 | Real-time / interactive generation | Pipeline is batch-oriented; interactive mode adds complexity without value |
| NG-02 | Support for non-English languages | English-only simplifies quality metrics and LaTeX handling |
| NG-03 | GUI or web interface | CLI is sufficient; UI is out of scope |
| NG-04 | Training or fine-tuning models | We use pre-trained LLMs via API |
| NG-05 | Arbitrary topic generation without research | Quality requires verified research for every topic |

---

## 4. Target Users

### Primary: Course Instructors and Reviewers
- Evaluating multi-agent system design and implementation quality
- Assessing software engineering practices and documentation
- Examining the quality of the generated PDF artifact

### Secondary: Developers and AI Practitioners
- Learning multi-agent orchestration patterns with CrewAI
- Understanding LaTeX automation pipelines
- Studying quality assurance in AI-generated content

### Tertiary: Readers of the Generated Book
- Educated non-specialists interested in the selected topic
- Graduate-level technical readers
- Expected reading level: Flesch-Kincaid grade 12–14

---

## 5. Functional Requirements

All functional requirements are defined in `docs/TODO.md`, Section 2.1 (FR-01 through FR-15).

**Critical path requirements:**

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR-01 | Use CrewAI framework | `crewai` in dependencies; agents use CrewAI API |
| FR-02 | Multiple distinct agents | ≥10 agents with unique roles |
| FR-03 | Agent collaboration | Context passing verified in integration tests |
| FR-04 | Professional book output | ≥20 pages, chapters, bibliography, index |
| FR-05 | LaTeX source | `.tex` files compile with `pdflatex`/`latexmk` |
| FR-06 | PDF output | Readable, professional, all elements render |

---

## 6. Non-Functional Requirements

All non-functional requirements are defined in `docs/TODO.md`, Section 2.2 (NFR-01 through NFR-15).

**Key engineering requirements:**

| ID | Requirement | Verification |
|----|-------------|--------------|
| NFR-01 | PEP 8 compliance | `ruff check` exits 0 |
| NFR-02 | Type annotations | `mypy --strict` passes |
| NFR-04 | No hardcoded secrets | `.env` pattern; `gitleaks` scan clean |
| NFR-06 | Clean virtualenv install | Fresh venv test passes |
| NFR-11 | ≥85% test coverage | `pytest --cov` report |

---

## 7. System Constraints

| Constraint | Description |
|------------|-------------|
| Python ≥3.11 | Required by type annotation features and dependencies |
| CrewAI ≥0.28 | Latest stable; defines agent/crew/task API |
| LaTeX distribution | TeX Live or MiKTeX must be installed for PDF compilation |
| OpenAI API access | GPT-4o or equivalent required for agent LLM calls |
| Network access | Required for research (web search, ArXiv queries) |
| Runtime budget | Full pipeline must complete within 30 minutes |
| Cost budget | Estimated $5–15 per full pipeline run |

---

## 8. Topic Selection

### 8.1 Evaluation Methodology

Each candidate topic was scored on six axes using a 1–5 scale with the following weights:

| Axis | Weight | Description |
|------|--------|-------------|
| Originality | 20% | Avoids overused topics; offers a fresh angle |
| Educational Value | 20% | Genuinely teaches something valuable |
| Research Depth | 20% | Sufficient academic literature exists |
| Visual/Structural Appeal | 15% | Lends itself to figures, tables, diagrams |
| Multi-Agent Showcase | 15% | Requires diverse expertise to cover |
| Impressiveness | 10% | Will impress technically sophisticated reviewers |

### 8.2 Candidate Evaluation

| # | Topic | Orig | Edu | Res | Vis | MAS | Imp | **Weighted** |
|---|-------|------|-----|-----|-----|-----|-----|-------------|
| 1 | Architecture of Trust: AI Safety | 3.5 | 4.0 | 4.0 | 3.0 | 3.5 | 4.0 | **3.67** |
| 2 | Emergent Capabilities in LLMs | 4.0 | 4.5 | 4.5 | 3.0 | 3.0 | 4.5 | **3.93** |
| 3 | Mathematics of Diffusion Models | 4.0 | 4.0 | 4.0 | 4.5 | 3.0 | 4.5 | **3.95** |
| 4 | **Multi-Agent Systems in AI** | **4.5** | **4.5** | **4.5** | **4.0** | **5.0** | **4.5** | **4.50** |
| 5 | History of Symbolic and Neural AI | 3.5 | 4.0 | 4.0 | 3.5 | 3.0 | 3.5 | **3.60** |
| 6 | Causal Inference in ML | 4.0 | 4.5 | 4.5 | 3.5 | 3.0 | 4.5 | **3.98** |

### 8.3 Selected Topic

**"Multi-Agent Systems in AI: Theoretical Foundations and Modern Applications"**

**Score: 4.50/5.00** (highest among all candidates)

### 8.4 Selection Rationale

1. **Meta-relevance**: The book's topic is directly related to the system that generates it. This creates a compelling narrative where the artifact explains its own architecture paradigm.

2. **Research depth**: Multi-agent systems have a rich academic history spanning game theory, distributed AI, reinforcement learning, and the recent wave of LLM-based agent frameworks. Hundreds of peer-reviewed papers are available.

3. **Multi-agent showcase**: This topic inherently requires expertise across multiple domains (theoretical CS, game theory, RL, NLP, software engineering), naturally exercising all 10 agents.

4. **Structural appeal**: The topic naturally decomposes into chapters covering theory, architectures, communication protocols, modern frameworks, applications, and future directions — with opportunities for diagrams, comparison tables, and algorithm pseudocode.

5. **Impressiveness**: A book about multi-agent systems generated by a multi-agent system demonstrates sophisticated understanding and creates a memorable, recursive narrative.

### 8.5 Key Research Questions

The book must address these core questions:

1. What are the theoretical foundations of multi-agent systems, and how did the field evolve from distributed AI?
2. What communication and coordination protocols enable effective agent collaboration?
3. How do modern LLM-based agent frameworks (CrewAI, AutoGen, LangGraph) compare in architecture and capability?
4. What are the key challenges in multi-agent systems: alignment, scalability, emergence, and safety?
5. How are multi-agent systems being applied in practice across domains (software engineering, scientific discovery, creative tasks)?
6. What are the open problems and future directions for the field?

### 8.6 Target Audience Profile

- **Knowledge level**: Graduate students and professional developers with foundational AI/ML knowledge
- **Background**: Computer science, software engineering, or adjacent technical fields
- **Goals**: Understand multi-agent system design principles; evaluate modern frameworks; apply patterns to their own work
- **Reading level**: Flesch-Kincaid grade 12–14 (technical but accessible)

### 8.7 Scope Boundaries

**In scope:**
- Theoretical foundations (game theory, mechanism design, distributed computing)
- Agent architectures and taxonomies
- Communication and coordination protocols
- Modern LLM-based frameworks (CrewAI, AutoGen, LangGraph, MetaGPT)
- Applications across domains
- Evaluation methodologies
- Future directions and open problems

**Explicitly out of scope:**
- Detailed mathematical proofs (referenced but not reproduced)
- Implementation tutorials or code walkthroughs
- Comparison of specific LLM models (GPT-4 vs Claude vs Gemini)
- Robotics-specific multi-agent systems (physical embodiment)
- Economic market design (mentioned but not deeply covered)

---

## 9. Success Metrics

| ID | Metric | Target | Measurement |
|----|--------|--------|-------------|
| SM-01 | PDF page count | ≥20 | `pdfinfo` |
| SM-02 | Verified sources | ≥20 | Citation Agent report |
| SM-03 | Hallucination rate | 0% critical | Fact-check audit |
| SM-04 | Readability score | ≥60 Flesch | `textstat` |
| SM-05 | Citation match rate | 100% | Citation audit |
| SM-06 | Test coverage | ≥85% | `pytest --cov` |
| SM-07 | Lint errors | 0 | `ruff check` |
| SM-08 | Type errors | 0 | `mypy --strict` |
| SM-09 | Pipeline runtime | ≤30 min | Timer |
| SM-10 | Documentation completeness | 100% | Checklist |

---

## 10. Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM hallucinations in content | High | High | Multi-layer hallucination detection; Fact Verification Agent; citation cross-referencing |
| LaTeX compilation failures | Medium | Medium | Iterative compilation fixing (up to 5 retries); fallback to simpler template |
| API rate limiting | Medium | Low | Retry with exponential backoff; local caching of search results |
| Insufficient source material | Low | Medium | Broad search strategy; multiple search engines; citation snowballing |
| Pipeline timeout (>30 min) | Medium | Low | Per-stage timeouts; cost optimization mode (`--fast` flag) |
| Inconsistent writing quality | Medium | Medium | Multi-pass editorial review; readability quality gates; Writer→Editor→Reviewer loop |
| Cost overrun | Low | Low | Token usage tracking; cost estimates logged; `--fast` mode available |
| CrewAI API breaking changes | Low | High | Pin exact version; abstract via wrapper classes |

---

## 11. Open Questions

All resolved during Phase 0–1 planning:

| # | Question | Resolution |
|---|----------|------------|
| 1 | Which topic? | Multi-Agent Systems in AI (scored 4.50/5.00) |
| 2 | Book or article? | Book format (richer structure, more impressive) |
| 3 | Which LaTeX class? | `memoir` (most powerful for books) |
| 4 | Which citation style? | BibLaTeX with APA style via Biber backend |
| 5 | Sequential or hierarchical crews? | Both: sequential main pipeline, hierarchical sub-crews |
| 6 | Which LLM model? | GPT-4o (configurable via `.env`) |

---

## Appendix: Requirements Traceability Matrix

See `docs/TODO.md`, Appendix A for the full traceability matrix mapping every requirement to its implementation phase, task, test, and documentation.

---

*End of PRD.md*
