"""Outline Architect Agent (A-03) — Information Architect.

Designs the hierarchical structure of the book including chapters,
sections, and the logical flow of information through the manuscript.
"""

from crewai import Agent


def create_outline_agent() -> Agent:
    """Create and return the Outline Architect Agent.

    This agent designs the book's information architecture, creating
    a detailed outline that balances depth, breadth, and readability
    for the target graduate-level audience.
    """
    return Agent(
        role="Information Architect",
        goal=(
            "Design a comprehensive, well-structured outline for a book "
            "with 6-8 chapters, each containing 3-5 sections. Ensure "
            "logical flow from foundational concepts to advanced topics."
        ),
        backstory=(
            "You are a renowned technical editor who has structured over "
            "50 academic textbooks. You understand how to organize complex "
            "material into a coherent narrative arc that guides readers "
            "from fundamentals to cutting-edge developments."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )
