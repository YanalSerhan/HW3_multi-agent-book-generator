"""LaTeX extractor for Jupyter notebooks."""

import json
import logging
from pathlib import Path

from .nb_image_decoder import decode_and_save_image

logger = logging.getLogger(__name__)


def extract_notebook_to_latex(
    notebook_path: str | Path, output_tex_path: str | Path
) -> Path | None:
    """Extract code and images to a LaTeX appendix file.

    Args:
        notebook_path: Path to the .ipynb file.
        output_tex_path: Path where the .tex file should be saved.

    Returns:
        Path to the generated .tex file, or None if extraction fails.
    """
    notebook_path = Path(notebook_path)
    output_tex_path = Path(output_tex_path)
    if not notebook_path.exists():
        logger.error(f"Notebook not found: {notebook_path}")
        return None

    # Setup output directories for images relative to the tex file
    tex_dir = output_tex_path.parent
    img_dir = tex_dir / "figures"
    img_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(notebook_path, encoding="utf-8") as f:
            notebook_data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse notebook JSON: {e}")
        return None

    tex_content: list[str] = [
        "\\chapter{Practical Implementation and Code Examples}",
        "This chapter contains selected code snippets and generated figures demonstrating the practical implementation of VAE and diffusion models.",
        "",
    ]

    image_counter = 1
    cells_processed = 0
    base_name = notebook_path.stem
    cells = notebook_data.get("cells", [])

    for cell in cells:
        cell_type = cell.get("cell_type")
        source = cell.get("source", [])
        source_text = "".join(source) if isinstance(source, list) else str(source)

        if cell_type == "markdown" and source_text.strip():
            # Skip the submission info/instructions cell
            if (
                "Submission date" in source_text
                or "Submitted by" in source_text
                or "Exercise 5:" in source_text
            ):
                continue

            from ..latex.renderer import _latex_escape

            for line in source_text.splitlines():
                if line.startswith("## "):
                    title = line.lstrip("# ").strip()
                    import re

                    title = re.sub(
                        r"^(?:Question \d+|Q\d+)\s*[:\-]?\s*", "", title, flags=re.IGNORECASE
                    )
                    tex_content.append(f"\\section{{{_latex_escape(title)}}}")
                elif line.startswith("### "):
                    title = line.lstrip("# ").strip()
                    tex_content.append(f"\\subsection{{{_latex_escape(title)}}}")
                elif line.strip() and not line.startswith("#"):
                    tex_content.append(_latex_escape(line.strip()))
            tex_content.append("")

        elif cell_type == "code" and source_text.strip():
            has_image = False
            outputs = cell.get("outputs", [])
            for output in outputs:
                data = output.get("data", {})
                if "image/png" in data or "application/pdf" in data:
                    has_image = True
                    break

            if len(source_text.splitlines()) > 5 or has_image:
                cells_processed += 1
                tex_content.append(f"\\section*{{Implementation Step {cells_processed}}}")
                tex_content.append("\\begin{lstlisting}[language=Python]")

                code_lines = source_text.strip().splitlines()
                if len(code_lines) > 15:
                    truncated_code = (
                        "\n".join(code_lines[:15]) + "\n\n# ... (Code truncated for brevity)"
                    )
                else:
                    truncated_code = "\n".join(code_lines)

                tex_content.append(truncated_code)
                tex_content.append("\\end{lstlisting}")

                for output in outputs:
                    data = output.get("data", {})
                    success, _img_ext, img_path = decode_and_save_image(
                        data, img_dir, base_name, image_counter
                    )
                    if success and img_path:
                        tex_content.append("\\begin{figure}[h]")
                        tex_content.append("\\centering")
                        tex_content.append(
                            f"\\includegraphics[width=0.8\\textwidth,height=0.35\\textheight,keepaspectratio]{{figures/{img_path.name}}}"
                        )
                        tex_content.append(f"\\caption{{Extracted Figure {image_counter}}}")
                        tex_content.append("\\end{figure}")
                        tex_content.append("")
                        image_counter += 1

    with open(output_tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_content))

    logger.info(f"Extracted notebook to LaTeX: {output_tex_path}")
    return output_tex_path
