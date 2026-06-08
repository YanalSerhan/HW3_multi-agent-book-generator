"""CLI entry point for the CrewAI Multi-Agent Book Generator.

This module provides the command-line interface using Typer.
Run with: python -m crewai_book --help
"""

from __future__ import annotations

import typer
from dotenv import load_dotenv
from rich.console import Console

from crewai_book.version import __version__

# Load environment variables from .env file so CrewAI can find OPENAI_API_KEY
load_dotenv()

app = typer.Typer(
    name="crewai-book",
    help="CrewAI Multi-Agent Book Generator — Generate professional PDF books using AI agents.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"crewai-book-generator v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """CrewAI Multi-Agent Book Generator.

    A production-grade multi-agent AI system that autonomously generates
    professional, publication-quality books compiled from LaTeX source.
    """


@app.command()
def run(
    topic: str | None = typer.Option(
        None,
        "--topic",
        "-t",
        help="Override the topic from .env configuration.",
    ),
    document_type: str = typer.Option(
        "book",
        "--type",
        help="Document type: 'book' or 'article'.",
    ),
    output_dir: str = typer.Option(
        "output",
        "--output",
        "-o",
        help="Output directory for generated artifacts.",
    ),
) -> None:
    """Run the full book generation pipeline."""
    from crewai_book.workflows.main_crew import run_pipeline

    final_topic = topic or "Multi-Agent Systems in AI"

    console.print(f"[bold green]CrewAI Book Generator v{__version__}[/bold green]")
    console.print(f"  Topic: {final_topic}")
    console.print(f"  Type:  {document_type}")
    console.print(f"  Output: {output_dir}")
    console.print()

    try:
        from pathlib import Path
        state = run_pipeline(final_topic, Path(output_dir))
        console.print(f"[bold green]Pipeline completed![/bold green] Run ID: {state.run_id}")
    except Exception as e:
        console.print(f"[bold red]Pipeline failed:[/bold red] {e}")
        raise typer.Exit(code=1) from e


@app.command()
def info() -> None:
    """Display system information and configuration status."""
    console.print(f"[bold]CrewAI Book Generator v{__version__}[/bold]")
    console.print()
    console.print("[dim]Configuration:[/dim]")
    console.print("  .env file: [yellow]check .env.example[/yellow]")
    console.print("  Pipeline:  [green]implemented[/green]")


if __name__ == "__main__":
    app()
