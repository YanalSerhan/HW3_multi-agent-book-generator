#!/usr/bin/env python3
"""Check that all citations resolve properly."""

import argparse
import sys
from pathlib import Path

import bibtexparser
from rich.console import Console
from rich.table import Table

console = Console()


def check_citations(bib_path: Path) -> int:
    """Check citations in a BibTeX file."""
    if not bib_path.exists():
        console.print(f"[red]Error:[/red] BibTeX file not found at {bib_path}")
        return 1

    console.print(f"Loading BibTeX file: {bib_path}")

    with open(bib_path, encoding="utf-8") as f:
        bib_database = bibtexparser.load(f)

    if not bib_database.entries:
        console.print("[yellow]Warning:[/yellow] No entries found in the BibTeX file.")
        return 0

    table = Table(title="Citation Validation Report")
    table.add_column("Key", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Issues", style="red")

    issues_count = 0

    for entry in bib_database.entries:
        key = entry.get("ID", "UNKNOWN")
        entry_type = entry.get("ENTRYTYPE", "unknown")

        issues = []
        if "title" not in entry:
            issues.append("Missing title")
        if "author" not in entry:
            issues.append("Missing author")
        if "year" not in entry and "date" not in entry:
            issues.append("Missing year/date")

        # Optional: warn if no URL or DOI for checking resolving
        if "doi" not in entry and "url" not in entry:
            issues.append("No DOI/URL")

        status = "[green]OK[/green]" if not issues else "[red]Issues Found[/red]"
        table.add_row(key, entry_type, status, ", ".join(issues))

        if issues:
            issues_count += 1

    console.print(table)

    if issues_count > 0:
        console.print(f"[bold red]Found {issues_count} entries with issues.[/bold red]")
        return 1
    else:
        console.print("[bold green]All citations look good![/bold green]")
        return 0


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate BibTeX citations.")
    parser.add_argument(
        "--bib",
        type=Path,
        default=Path("output/references.bib"),
        help="Path to the BibTeX file"
    )
    args = parser.parse_args()

    sys.exit(check_citations(args.bib))


if __name__ == "__main__":
    main()
