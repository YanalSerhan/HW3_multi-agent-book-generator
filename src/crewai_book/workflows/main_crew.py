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
    figure_agent = create_figure_agent(output_dir=output_dir)
    latex_agent = create_latex_agent()
    pdf_agent = create_pdf_agent()
    qa_agent = create_qa_agent()

    from ..config.settings import config_manager

    setup_config = config_manager.get_setup()
    book_length = setup_config.get("book_length", {})
    chapter_count = book_length.get("chapter_count", 8)
    words_per_section = book_length.get("words_per_section", 200)

    outline_task = Task(
        description=(
            f"Create a detailed book outline for '{topic}' with "
            f"{chapter_count} chapters, each having 3-4 sections. Include a chapter "
            f"summary and target word count ({words_per_section} words) for each section. "
            "CRITICAL REQUIRED CHAPTER: You MUST include exactly ONE chapter titled 'פרק בעברית: האינטואיציה ממודלי VAE למודלי דיפוזיה (Hebrew Chapter)' "
            "— this chapter will be WRITTEN IN THE HEBREW LANGUAGE (עברית), not in English. It is NOT a metaphor or style. "
            "Its sections cover: ELBO and the reparameterization trick as the VAE foundation; diffusion as a hierarchical VAE; the role of the noise schedule. "
            "Explicitly include LaTeX tables (using \\begin{table}...\\end{table}) for comparative analysis "
            "in at least one chapter. Do NOT use markdown tables or image files for tables."
        ),
        expected_output="Hierarchical outline with chapters, sections, and table markers.",
        output_file=str(output_dir / "outline.md"),
        agent=outline_agent,
    )

    writing_task = Task(
        description=(
            "Write the complete manuscript following the outline. "
            f"Each section should be ~{words_per_section} words to hit the target length. "
            "Dive deep into the technical details, providing comprehensive explanations, "
            "examples, and edge cases to significantly increase the word count per section. "
            "CRITICAL BIDI REQUIREMENT: The chapter covering 'פרק בעברית: האינטואיציה ממודלי VAE למודלי דיפוזיה (Hebrew Chapter)' MUST be written entirely in Hebrew prose "
            "(using inline English technical terms where appropriate). You MUST NOT use \\begin{hebrew} in your output. Just write raw markdown. "
            "The Hebrew chapter explains the intuition bridge from VAEs to diffusion models: ELBO and the reparameterization trick as the VAE foundation, why diffusion can be seen as a hierarchical VAE, and the role of the noise schedule. Content must be specific to these concepts — generic AI/LLM filler text is a failure. "
            "The Hebrew must be grammatically correct, natural academic Hebrew, as written by a native speaker. Ensure letters are written in their natural logical order, do NOT reverse them. "
            "You MAY include an OPTIONAL simple two-column English-Hebrew glossary table inside the Hebrew chapter.\n"
            "At least one LaTeX table must appear somewhere in the book (using \\begin{table}...\\end{table}) for data presentation instead of markdown tables. "
            "Actively embed citations matching the bibliography. "
            "Ensure extremely high readability by using very short sentences, simple vocabulary, "
            "and active voice."
        ),
        expected_output="Complete manuscript text for all chapters with tables and citations.",
        output_file=str(output_dir / "manuscript_draft.md"),
        agent=writer_agent,
    )

    provenance_task = Task(
        description=(
            "Review the drafted manuscript and inject PROVENANCE markers for major factual claims. "
            "You MUST add ~1-2 of these markers per page for key technical claims using EXACTLY this syntax: "
            "[PROVENANCE: bib_key | short quote < 15 words | confidence_score]\n"
            "Example: [PROVENANCE: ho2020denoising | diffusion models generate high quality images | 0.95]\n"
            "Every footnoted bib_key MUST exist in the bibliography."
        ),
        expected_output="Final manuscript text with provenance markers injected.",
        output_file=str(output_dir / "manuscript.md"),
        agent=writer_agent,
    )

    figure_task = Task(
        description=(
            "Read the manuscript and identify 2-3 key concepts or architectures that "
            "would benefit from visualization. Generate 2-3 professional figures "
            "(e.g., bar charts, line plots, or block diagrams) using the figure generator tool. "
            "CRITICAL: You MUST use the figure generator tool to create at least one topic-relevant matplotlib graph "
            "(e.g., comparing VAE and Diffusion latent spaces or noise schedules) specifically for the Hebrew intuition chapter. "
            "Save them as PNG or PDF files. Provide a summary of the generated figures "
            "including their filenames and suggested captions. "
            "CRITICAL: The suggested caption for any figure in the Hebrew chapter MUST be written entirely in Hebrew (עברית). Do NOT write English captions for the Hebrew chapter! "
            "CRITICAL: Do NOT generate tables as images. Tables must be natively formatted in text/LaTeX."
        ),
        expected_output="A list of generated figures with their filenames and captions.",
        output_file=str(output_dir / "figures_report.md"),
        agent=figure_agent,
    )

    latex_task = Task(
        description=(
            "Convert the manuscript and figures report into LaTeX source. "
            "The manuscript already contains raw LaTeX tables. Preserve them exactly. "
            "Embed EVERY figure from the figures report into the appropriate section using \\begin{figure}[H] and \\centering. "
            "This [H] placement is CRITICAL to prevent large empty spaces above figures. "
            "Ensure all in-text citations are mapped to \\cite{...} commands corresponding to the bibliography. "
            "CRITICAL: The manuscript contains a Hebrew chapter. You MUST wrap the entire Hebrew chapter content, INCLUDING the \\chapter{...} and \\section{...} commands, "
            "inside a \\begin{hebrew} ... \\end{hebrew} environment block. This is mandatory for RTL title formatting. "
            "CRITICAL: The manuscript contains custom tags like [PROVENANCE: ...]. You MUST preserve these tags exactly as they appear in the text. "
            "CRITICAL: Output ONLY the raw LaTeX source code for the chapters and sections. "
            "Do NOT output \\documentclass, \\begin{document}, or any preamble. Just output the \\chapter, \\section, and text content."
        ),
        expected_output="Raw LaTeX body code containing only chapters, sections, properly formatted tables, and preserved PROVENANCE tags.",
        output_file=str(output_dir / "latex" / "body.tex"),
        agent=latex_agent,
    )

    pdf_task = Task(
        description=(
            "Compile the LaTeX source into a final PDF. Verify the "
            "output has ≥15 pages and all elements render correctly. "
            f"CRITICAL: You MUST invoke the latex_compiler tool with "
            f"tex_file_path='{output_dir.resolve()}/latex/book.tex'."
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
        tasks=[
            outline_task,
            writing_task,
            provenance_task,
            figure_task,
            latex_task,
            pdf_task,
            qa_task,
        ],
        process=Process.sequential,
        verbose=True,
    )
