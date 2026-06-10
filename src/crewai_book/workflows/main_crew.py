"""Main crew orchestrating the full book generation pipeline.

Coordinates all 10 agents through the sequential pipeline stages:
research → outline → writing → editorial → citation → LaTeX → PDF → QA.
"""

from pathlib import Path

from crewai import Crew, Process, Task

from ..agents.figure_agent import create_figure_agent
from ..agents.latex_agent import create_latex_agent
from ..agents.outline_agent import create_outline_agent
from ..agents.pdf_agent import create_pdf_agent
from ..agents.qa_agent import create_qa_agent
from ..agents.writer_agent import create_writer_agent
from ..observability.logger import get_logger

logger = get_logger("workflows.main_crew")


def create_main_crew(topic: str, output_dir: Path) -> Crew:
    """Build the main sequential pipeline crew.

    Orchestrates the full pipeline from research through QA,
    coordinating sub-crews and individual agents in dependency order.
    """
    logger.info(f"Building main pipeline for topic: {topic}")

    outline_agent = create_outline_agent()
    writer_agent = create_writer_agent()
    figure_agent = create_figure_agent()
    latex_agent = create_latex_agent()
    pdf_agent = create_pdf_agent()
    qa_agent = create_qa_agent()

    outline_task = Task(
        description=(
            f"Create a detailed book outline for '{topic}' with "
            "8-10 chapters, each having 3-4 sections. Include a chapter "
            "summary and target word count (200-300 words) for each section. "
            "Explicitly include LaTeX tables (using \\begin{table}...\\end{table}) for comparative analysis "
            "in at least half of the chapters. Do NOT use markdown tables or image files for tables."
        ),
        expected_output="Hierarchical outline with chapters, sections, and table markers.",
        output_file=str(output_dir / "outline.md"),
        agent=outline_agent,
    )

    writing_task = Task(
        description=(
            "Write the complete manuscript following the outline. "
            "Each section should be 200-250 words to hit a total of 7000-8000 words. "
            "Dive deep into the technical details, providing comprehensive explanations, "
            "examples, and edge cases to significantly increase the word count per section. "
            "Actively embed LaTeX tables (using \\begin{table}...\\end{table}) for data presentation instead of markdown tables. "
            "Do NOT use image files for tables. "
            "Actively embed citations matching the bibliography. "
            "Ensure extremely high readability by using very short sentences, simple vocabulary, "
            "and active voice to achieve a high readability score."
        ),
        expected_output="Complete manuscript text for all chapters with tables and citations.",
        output_file=str(output_dir / "manuscript.md"),
        agent=writer_agent,
    )

    figure_task = Task(
        description=(
            "Read the manuscript and identify 2-3 key concepts or architectures that "
            "would benefit from visualization. Generate 2-3 professional figures "
            "(e.g., bar charts, line plots, or block diagrams) using the figure generator tool. "
            "Save them as PNG or PDF files. Provide a summary of the generated figures "
            "including their filenames and suggested captions. "
            "CRITICAL: Do NOT generate tables as images. Tables must be natively formatted in text/LaTeX."
        ),
        expected_output="A list of generated figures with their filenames and captions.",
        output_file=str(output_dir / "figures_report.md"),
        agent=figure_agent,
    )

    latex_task = Task(
        description=(
            "Convert the manuscript and figures report into LaTeX source. "
            "The manuscript already contains raw LaTeX tables. Preserve them exactly. To prevent table overflow, you MAY add \\resizebox{\\textwidth}{!}{...} around tabular environments if necessary. "  # noqa: E501
            "Embed EVERY figure from the figures report into the appropriate section using \\begin{figure}. "  # noqa: E501
            "Ensure all in-text citations are mapped to \\cite{...} commands corresponding to the bibliography. "  # noqa: E501
            "CRITICAL: Output ONLY the raw LaTeX source code for the chapters and sections. "
            "Do NOT output \\documentclass, \\begin{document}, or any preamble. Just output the \\chapter, \\section, and text content. "  # noqa: E501
            "Do NOT enclose your output in markdown code blocks."
        ),
        expected_output="Raw LaTeX body code containing only chapters, sections, and properly formatted tables.",  # noqa: E501
        output_file=str(output_dir / "latex" / "body.tex"),
        agent=latex_agent,
    )

    pdf_task = Task(
        description=(
            "Compile the LaTeX source into a final PDF. Verify the "
            "output has ≥15 pages and all elements render correctly."
        ),
        expected_output="Compiled PDF with quality verification report.",
        output_file=str(output_dir / "latex" / "pdf_report.md"),
        agent=pdf_agent,
    )

    qa_task = Task(
        description=(
            "Perform final quality certification. Run all quality gates "
            "and produce a comprehensive QA report confirming the "
            "manuscript meets all publication standards."
        ),
        expected_output="QA certification report with gate results.",
        output_file=str(output_dir / "qa_report.md"),
        agent=qa_agent,
    )

    return Crew(
        agents=[outline_agent, writer_agent, figure_agent, latex_agent, pdf_agent, qa_agent],
        tasks=[outline_task, writing_task, figure_task, latex_task, pdf_task, qa_task],
        process=Process.sequential,
        verbose=True,
    )
