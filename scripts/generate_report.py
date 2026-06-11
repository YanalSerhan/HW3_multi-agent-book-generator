#!/usr/bin/env python3
"""Generate post-run evaluation report."""

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def generate_report(log_dir: Path) -> int:
    """Generate a summary report from the latest run logs."""
    if not log_dir.exists():
        console.print(f"[red]Error:[/red] Log directory not found at {log_dir}")
        return 1

    # Find the most recent log file
    log_files = list(log_dir.glob("*.jsonl"))
    if not log_files:
        console.print(f"[yellow]No log files found in {log_dir}. Assuming dry run.[/yellow]")
        _print_mock_report()
        return 0

    latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
    console.print(f"Analyzing log file: {latest_log}")

    errors = 0
    warnings = 0
    total_tokens = 0
    agents_used = set()

    with open(latest_log, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                level = entry.get("record", {}).get("level", {}).get("name", "")
                if level == "ERROR":
                    errors += 1
                elif level == "WARNING":
                    warnings += 1

                # Extract any custom metrics if available
                extra = entry.get("record", {}).get("extra", {})
                if "tokens" in extra:
                    total_tokens += extra["tokens"]
                if "agent" in extra:
                    agents_used.add(extra["agent"])
            except json.JSONDecodeError:
                pass

    _print_summary(latest_log.name, len(agents_used), total_tokens, errors, warnings)
    return 0


def _print_mock_report() -> None:
    """Print a placeholder report for demonstration when no logs exist."""
    _print_summary("run_mock_123.jsonl", 10, 150420, 0, 2)


def _print_summary(run_id: str, agents: int, tokens: int, errors: int, warnings: int) -> None:
    """Print the formatted summary report."""
    table = Table(title="Pipeline Execution Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Run ID", run_id)
    table.add_row("Agents Utilized", str(agents))
    table.add_row("Total Tokens Used", f"{tokens:,}")
    table.add_row("Errors Encountered", f"[red]{errors}[/red]" if errors > 0 else "[green]0[/green]")
    table.add_row("Warnings", f"[yellow]{warnings}[/yellow]" if warnings > 0 else "0")

    estimated_cost = (tokens / 1_000_000) * 5.00  # Assumes $5.00 per 1M tokens approx
    table.add_row("Estimated Cost", f"${estimated_cost:.4f}")

    console.print(Panel(table, title="Evaluation Report", expand=False))


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate pipeline report.")
    parser.add_argument(
        "--logs",
        type=Path,
        default=Path("output/logs"),
        help="Path to the logs directory"
    )
    args = parser.parse_args()

    sys.exit(generate_report(args.logs))


if __name__ == "__main__":
    main()
