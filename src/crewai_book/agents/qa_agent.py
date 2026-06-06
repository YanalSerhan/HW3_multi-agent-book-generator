"""Quality Assurance Agent (A-10) — Chief Quality Officer.

Performs the final quality certification, verifying all quality
gates have passed and the manuscript meets every standard.
"""

from crewai import Agent

from ..tools.readability_tool import ReadabilityScoreTool


def create_qa_agent() -> Agent:
    """Create and return the Quality Assurance Agent.

    This agent serves as the final checkpoint, running all quality
    gate verifications and producing a certification report that
    confirms the manuscript is ready for publication.
    """
    return Agent(
        role="Chief Quality Officer",
        goal=(
            "Perform final quality certification. Verify all 10 quality "
            "gates pass: source count, hallucination check, outline "
            "completeness, word count, readability, review resolution, "
            "citation match, compilation, page count, and overall QA."
        ),
        backstory=(
            "You are the chief quality officer for a prestigious academic "
            "publisher. Nothing ships without your stamp of approval. "
            "You are thorough, systematic, and uncompromising in your "
            "standards. Your QA reports are legendary for their detail."
        ),
        tools=[ReadabilityScoreTool()],
        verbose=True,
        allow_delegation=False,
    )
