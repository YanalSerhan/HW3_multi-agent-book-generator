"""Writer Agent (A-04) — Expert Technical Writer.

Produces the full manuscript text following the outline, weaving in
research sources and maintaining consistent voice and quality.
"""

from crewai import Agent

from ..tools.web_search_tool import WebSearchTool


def create_writer_agent() -> Agent:
    """Create and return the Writer Agent.

    This agent transforms the outline and research corpus into
    polished prose, ensuring proper citation integration and
    maintaining a consistent, authoritative voice throughout.
    """
    return Agent(
        role="Expert Technical Writer",
        goal=(
            "Write the complete manuscript following the provided outline. "
            "Each section should be 500-800 words, well-cited, and written "
            "at a graduate reading level (Flesch 60-70)."
        ),
        backstory=(
            "You are a technical author with multiple published textbooks "
            "in computer science. You excel at explaining complex concepts "
            "clearly while maintaining academic rigor. You naturally weave "
            "citations into your prose and use concrete examples."
        ),
        tools=[WebSearchTool()],
        verbose=True,
        allow_delegation=False,
    )
