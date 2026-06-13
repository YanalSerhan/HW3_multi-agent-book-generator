#!/usr/bin/env python3
"""Validate LaTeX syntax and structure."""

import argparse
import re
import sys
from pathlib import Path

from rich.console import Console

console = Console()


def validate_latex(tex_path: Path) -> int:
    """Validate LaTeX structure: braces and environments."""
    if not tex_path.exists():
        console.print(f"[red]Error:[/red] LaTeX file not found at {tex_path}")
        return 1

    console.print(f"Validating LaTeX file: {tex_path}")

    with open(tex_path, encoding="utf-8") as f:
        content = f.read()

    issues = []

    # Check brace balancing
    brace_count = 0
    for i, char in enumerate(content):
        # Ignore escaped braces
        if char == "{" and (i == 0 or content[i-1] != "\\"):
            brace_count += 1
        elif char == "}" and (i == 0 or content[i-1] != "\\"):
            brace_count -= 1
            if brace_count < 0:
                issues.append(f"Unmatched closing brace '}}' around character {i}")
                brace_count = 0  # reset to catch more

    if brace_count > 0:
        issues.append(f"Unmatched opening brace '{{' (Count: {brace_count})")

    # Check environment balancing
    re.compile(r"\\begin\{([^}]+)\}")
    re.compile(r"\\end\{([^}]+)\}")

    environments = []

    for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", content):
        tag_type = match.group(1)
        env_name = match.group(2)

        if tag_type == "begin":
            environments.append(env_name)
        elif tag_type == "end":
            if not environments:
                issues.append(f"\\end{{{env_name}}} found without matching \\begin")
            else:
                last_env = environments.pop()
                if last_env != env_name:
                    issues.append(f"Environment mismatch: expected \\end{{{last_env}}}, got \\end{{{env_name}}}")

    if environments:
        for env in environments:
            issues.append(f"Unclosed environment: \\begin{{{env}}}")

    if issues:
        console.print("[bold red]Validation failed with the following issues:[/bold red]")
        for issue in issues:
            console.print(f" - [red]{issue}[/red]")
        return 1

    console.print("[bold green]LaTeX structure appears valid![/bold green]")
    return 0


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate LaTeX syntax.")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("output/latex/book.tex"),
        help="Path to the .tex file"
    )
    args = parser.parse_args()

    sys.exit(validate_latex(args.file))


if __name__ == "__main__":
    main()
