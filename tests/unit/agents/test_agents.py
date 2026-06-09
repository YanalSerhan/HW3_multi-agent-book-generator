"""Unit tests for all 11 CrewAI agent factory functions."""

from crewai import Agent

from crewai_book.agents.citation_agent import create_citation_agent
from crewai_book.agents.editor_agent import create_editor_agent
from crewai_book.agents.fact_verification_agent import create_fact_verification_agent
from crewai_book.agents.figure_agent import create_figure_agent
from crewai_book.agents.latex_agent import create_latex_agent
from crewai_book.agents.outline_agent import create_outline_agent
from crewai_book.agents.pdf_agent import create_pdf_agent
from crewai_book.agents.qa_agent import create_qa_agent
from crewai_book.agents.research_agent import create_research_agent
from crewai_book.agents.reviewer_agent import create_reviewer_agent
from crewai_book.agents.writer_agent import create_writer_agent
from crewai_book.config.agent_configs import AGENT_CONFIGS


def test_research_agent_creation() -> None:
    """Research agent should have WebSearch, ArXiv, CitationValidator, Readability tools."""
    agent = create_research_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["research_agent"].role
    assert len(agent.tools or []) == 4


def test_fact_verification_agent_creation() -> None:
    """Fact verification agent should have WebSearch, CitationValidator, FactCheck tools."""
    agent = create_fact_verification_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["fact_verification_agent"].role
    assert len(agent.tools or []) == 3


def test_outline_agent_creation() -> None:
    """Outline agent should have no tools (pure reasoning)."""
    agent = create_outline_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["outline_architect_agent"].role
    assert len(agent.tools or []) == 0


def test_writer_agent_creation() -> None:
    """Writer agent should have ReadabilityScoreTool and memory enabled."""
    agent = create_writer_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["writer_agent"].role
    assert len(agent.tools or []) == 1


def test_editor_agent_creation() -> None:
    """Editor agent should have readability tool."""
    agent = create_editor_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["editor_agent"].role
    assert len(agent.tools or []) == 1


def test_reviewer_agent_creation() -> None:
    """Reviewer agent should have CitationValidator and FactCheck tools."""
    agent = create_reviewer_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["reviewer_agent"].role
    assert len(agent.tools or []) == 2


def test_citation_agent_creation() -> None:
    """Citation agent should have CitationValidator, WebSearch, and ArXiv tools."""
    agent = create_citation_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["citation_agent"].role
    assert len(agent.tools or []) == 3


def test_latex_agent_creation() -> None:
    """LaTeX agent should have compiler tool."""
    agent = create_latex_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["latex_formatter_agent"].role
    assert len(agent.tools or []) == 1


def test_pdf_agent_creation() -> None:
    """PDF agent should have compiler tool."""
    agent = create_pdf_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["pdf_production_agent"].role
    assert len(agent.tools or []) == 1


def test_qa_agent_creation() -> None:
    """QA agent should have ReadabilityScore and CitationValidator tools."""
    agent = create_qa_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["qa_agent"].role
    assert len(agent.tools or []) == 2


def test_figure_agent_creation() -> None:
    """Figure agent should have figure generator tool and use AGENT_CONFIGS."""
    agent = create_figure_agent()
    assert isinstance(agent, Agent)
    assert agent.role == AGENT_CONFIGS["figure_agent"].role
    assert len(agent.tools or []) == 1
