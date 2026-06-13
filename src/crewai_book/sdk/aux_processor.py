"""Helper function to post-process LaTeX auxiliary files (.toc, .lof, .lot)."""

import re
from pathlib import Path
from typing import Any


def post_process_aux_files(tex_file: Path, logger: Any | None = None) -> None:
    """Post-process TOC, LOF, LOT files to ensure Hebrew titles align with English page numbers."""
    latex_dir = tex_file.parent
    for ext in [".toc", ".lof", ".lot"]:
        aux_file = latex_dir / f"{tex_file.stem}{ext}"
        if aux_file.exists():
            try:
                content = aux_file.read_text(encoding="utf-8")
                # 1. Strip language switches
                content = re.sub(r"\\select@language\{hebrew\}", "", content)
                content = re.sub(r"\\select@language\{english\}", "", content)
                content = re.sub(r"\\xpg@aux\s*\{.*?\}\{hebrew\}", "", content)
                content = re.sub(r"\\xpg@aux\s*\{.*?\}\{english\}", "", content)

                # 2. Wrap Hebrew titles in \texthebrew
                def repl(match: re.Match[str]) -> str:
                    cat = match.group(1)
                    num_line = match.group(2)
                    title = match.group(3)
                    page = match.group(4)
                    anchor = match.group(5)

                    if re.search(r"[\u0590-\u05FF]", title) and "\\texthebrew" not in title:
                        title = f"\\texthebrew{{{title}}}"
                    return f"\\contentsline {{{cat}}}{{{num_line}{title}}}{{{page}}}{{{anchor}}}"

                pattern = (
                    r"\\contentsline\s*\{([^{}]+)\}\s*\{"
                    r"((?:\\(?:chapter|section)?numberline\s*\{[^{}]+\})?)"
                    r"(.*?)\}\s*\{([^{}]+)\}\s*\{([^{}]+)\}"
                )
                content = re.sub(pattern, repl, content)
                aux_file.write_text(content, encoding="utf-8")
            except Exception as e:
                if logger:
                    logger.warning(
                        f"Failed to post-process auxiliary file {aux_file}: {e}"
                    )
