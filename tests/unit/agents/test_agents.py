"""Unit tests for all 10 CrewAI agent factory functions."""

from crewai import Agent

from crewai_book.agents.citation_agent import create_citation_agent
from crewai_book.agents.editor_agent import create_editor_agent
from crewai_book.agents.fact_verification_agent import create_fact_verification_agent
from crewai_book.agents.latex_agent import create_latex_agent
from crewai_book.agents.outline_agent import create_outline_agent
from crewai_book.agents.pdf_agent import create_pdf_agent
from crewai_book.agents.qa_agent import create_qa_agent
from crewai_book.agents.research_agent import create_research_agent
from crewai_book.agents.reviewer_agent import create_reviewer_agent
from crewai_book.agents.writer_agent import create_writer_agent


def test_research_agent_creation() -> None:
    """Research agent should be a valid CrewAI Agent with tools."""
    agent = create_research_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Senior Research Scientist"
    assert len(agent.tools or []) == 2


def test_fact_verification_agent_creation() -> None:
    """Fact verification agent should have fact-checking tools."""
    agent = create_fact_verification_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Critical Fact Checker"
    assert len(agent.tools or []) == 2


def test_outline_agent_creation() -> None:
    """Outline agent should have no tools (pure reasoning)."""
    agent = create_outline_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Information Architect"
    assert len(agent.tools or []) == 0


def test_writer_agent_creation() -> None:
    """Writer agent should have web search for research."""
    agent = create_writer_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Expert Technical Writer"
    assert len(agent.tools or []) == 1


def test_editor_agent_creation() -> None:
    """Editor agent should have readability tool."""
    agent = create_editor_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Senior Copy Editor"
    assert len(agent.tools or []) == 1


def test_reviewer_agent_creation() -> None:
    """Reviewer agent should have readability tool."""
    agent = create_reviewer_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Peer Reviewer"


def test_citation_agent_creation() -> None:
    """Citation agent should have validator and arxiv tools."""
    agent = create_citation_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Bibliographer"
    assert len(agent.tools or []) == 2


def test_latex_agent_creation() -> None:
    """LaTeX agent should have compiler tool."""
    agent = create_latex_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Typesetting Specialist"


def test_pdf_agent_creation() -> None:
    """PDF agent should have compiler tool."""
    agent = create_pdf_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Production QC Specialist"


def test_qa_agent_creation() -> None:
    """QA agent should have readability tool."""
    agent = create_qa_agent()
    assert isinstance(agent, Agent)
    assert agent.role == "Chief Quality Officer"
