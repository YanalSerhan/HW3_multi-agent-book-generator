# Agents Documentation

This directory contains documentation for the distinct, non-overlapping AI agents employed by the CrewAI Book Generator. Each agent focuses on a specific aspect of the book generation pipeline, communicating through well-defined tasks.

## Agent Roles

### Research Crew
- **Research Agent (`research_agent.py`)**: Responsible for gathering verifiable academic and professional sources. Uses the `ArxivTool` and `WebSearchTool` to locate relevant material.
- **Fact Verification Agent (`fact_verification_agent.py`)**: Audits research to ensure no hallucinated citations or claims are present.
- **Citation Agent (`citation_agent.py`)**: Formats collected references into properly structured BibTeX formats.

### Main Content Crew
- **Outline Agent (`outline_agent.py`)**: Plans the structure of the document, determining chapters and sections based on the research.
- **Writer Agent (`writer_agent.py`)**: Generates the main text content iteratively for each section defined by the outline.
- **Figure Agent (`figure_agent.py`)**: Generates python scripts and visual assets needed for the document.
- **LaTeX Agent (`latex_agent.py`)**: Formats the written text and figures into raw LaTeX source code.

### Editorial Crew
- **Reviewer Agent (`reviewer_agent.py`)**: Reviews the final LaTeX output to ensure stylistic consistency and ISO/IEC 25010 compliance (Usability, Reliability).
- **Editor Agent (`editor_agent.py`)**: Makes the final stylistic tweaks and grammatical corrections.
- **QA Agent (`qa_agent.py`)**: Performs readability checks and ensures all requirements (such as page count, correct tables, equations) are met.
- **PDF Agent (`pdf_agent.py`)**: Coordinates the compilation of the LaTeX source into a polished PDF document.
