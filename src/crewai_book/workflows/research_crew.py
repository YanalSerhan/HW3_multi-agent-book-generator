"""Research sub-crew for the book generation pipeline.

Orchestrates agents A-01 (Research), A-02 (Fact Verification),
and A-07 (Citation) in a hierarchical crew for the research phase.
"""

from pathlib import Path

from crewai import Crew, Process, Task

from ..agents.citation_agent import create_citation_agent
from ..agents.fact_verification_agent import create_fact_verification_agent
from ..agents.research_agent import create_research_agent
from ..observability.logger import get_logger

logger = get_logger("workflows.research_crew")


def create_research_crew(topic: str, output_dir: Path) -> Crew:
    """Build and return the research sub-crew.

    This crew uses hierarchical process where a manager LLM
    orchestrates the research, fact-checking, and citation agents
    to complete the research phase collaboratively.
    """
    research_agent = create_research_agent()
    fact_agent = create_fact_verification_agent()
    citation_agent = create_citation_agent()

    research_task = Task(
        description=(
            f"Conduct comprehensive research on '{topic}'. "
            "Find a LOT of high-quality sources (at least 15-20+) from academic papers "
            "and authoritative websites. You MUST ensure that you do not include ANY invalid "
            "or broken sources. Validate the URLs and DOIs carefully. Use the arxiv_search tool to find "
            "academic papers and the web_search tool for other sources. "
            "For each source include: title, authors, year, URL or DOI, "
            "and a one-sentence relevance note. Organize sources by subtopic."
        ),
        expected_output="A structured list of 10+ sources with metadata.",
        output_file=str(output_dir / "research" / "sources.md"),
        agent=research_agent,
    )

    verification_task = Task(
        description=(
            "Review the research sources provided in your context. "
            "For each source, verify the factual claims by cross-referencing "
            "against at least 2 independent sources using your tools. "
            "Use the citation_validator tool to check that DOIs and URLs resolve. "
            "Assign a confidence score (0.0-1.0) to each source. "
            "Flag any unverified claims. Do NOT attempt to delegate work to "
            "other agents — perform the verification yourself using your tools.\n\n"
            "Output a structured verification report with:\n"
            "- Each source listed with its confidence score\n"
            "- Any flagged claims with explanations\n"
            "- Summary: total sources verified, total hallucinations found (if any)\n"
            "- End with the line: '0 hallucinations found' if none were detected"
        ),
        expected_output=(
            "A verification report listing each source with a confidence score, "
            "flagged claims, and a summary line with hallucination count."
        ),
        output_file=str(output_dir / "research" / "verification_report.md"),
        agent=fact_agent,
        context=[research_task],
    )

    citation_task = Task(
        description=(
            "You are given a list of verified research sources in your context. "
            "For EACH source, create a valid BibTeX entry. Use the arxiv_search "
            "tool to look up proper metadata (authors, year, title, DOI) for each "
            "source. Use the citation_validator tool to verify each DOI or URL.\n\n"
            "Your output must contain AT LEAST 10 BibTeX entries.\n\n"
            "CRITICAL OUTPUT FORMAT RULES:\n"
            "- Output ONLY raw BibTeX entries, one after another.\n"
            "- Do NOT include any markdown, explanations, backticks, or commentary.\n"
            "- Do NOT ask questions or request clarification.\n"
            "- Each entry must start with @ and end with a closing }.\n"
            "- Use entry types: @article, @inproceedings, @book, or @misc.\n"
            "- Example of correct output format:\n\n"
            "@article{song2021scorebased,\n"
            "  title={Score-Based Generative Modeling through SDEs},\n"
            "  author={Yang Song and Jascha Sohl-Dickstein and others},\n"
            "  journal={arXiv preprint arXiv:2011.13456},\n"
            "  year={2021}\n"
            "}\n\n"
            "@article{ho2020denoising,\n"
            "  title={Denoising Diffusion Probabilistic Models},\n"
            "  author={Jonathan Ho and Ajay Jain and Pieter Abbeel},\n"
            "  journal={NeurIPS},\n"
            "  year={2020}\n"
            "}\n"
        ),
        expected_output=(
            "A plain text file containing 15+ valid BibTeX entries. "
            "No markdown, no explanations, no backticks. Only @type{key, ...} entries."
        ),
        output_file=str(output_dir / "latex" / "references.bib"),
        agent=citation_agent,
        context=[research_task, verification_task],
    )

    logger.info(f"Creating research crew for topic: {topic}")

    (output_dir / "research").mkdir(parents=True, exist_ok=True)
    (output_dir / "latex").mkdir(parents=True, exist_ok=True)

    return Crew(
        agents=[research_agent, fact_agent, citation_agent],
        tasks=[research_task, verification_task, citation_task],
        process=Process.sequential,
        verbose=True,
    )
