"""Notebook Extractor Tool for parsing Jupyter notebooks and extracting text and images."""

import base64
import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class NotebookExtractorConfig(BaseModel):
    """Configuration for Notebook Extractor."""

    output_md_dir: Path = Field(default_factory=lambda: Path("sources"))
    output_img_dir: Path = Field(default_factory=lambda: Path("sources/extracted_figures"))


class NotebookExtractor:
    """Tool to parse Jupyter notebooks, extract markdown/code, and save images."""

    def __init__(self, config: NotebookExtractorConfig | None = None) -> None:
        """Initialize the extractor."""
        self.config = config or NotebookExtractorConfig()

    def extract(self, notebook_path: str | Path) -> Path | None:
        """Extract markdown/code and images from a notebook.

        Args:
            notebook_path: Path to the .ipynb file.

        Returns:
            Path to the generated markdown file, or None if extraction fails.
        """
        notebook_path = Path(notebook_path)
        if not notebook_path.exists():
            logger.error(f"Notebook not found: {notebook_path}")
            return None

        # Setup output directories
        self.config.output_md_dir.mkdir(parents=True, exist_ok=True)
        self.config.output_img_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(notebook_path, encoding="utf-8") as f:
                notebook_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse notebook JSON: {e}")
            return None

        md_content: list[str] = []
        image_counter = 1
        base_name = notebook_path.stem

        cells = notebook_data.get("cells", [])
        for cell in cells:
            cell_type = cell.get("cell_type")
            source = cell.get("source", [])

            # Normalize source to a single string
            source_text = "".join(source) if isinstance(source, list) else str(source)

            if cell_type == "markdown":
                md_content.append(source_text)
                md_content.append("\n")
            elif cell_type == "code":
                md_content.append("```python")
                md_content.append(source_text)
                md_content.append("```\n")

                # Extract outputs for code cells
                outputs = cell.get("outputs", [])
                for output in outputs:
                    data = output.get("data", {})

                    if "image/png" in data:
                        img_data = data["image/png"]
                        # Handle multi-line base64
                        if isinstance(img_data, list):
                            img_data = "".join(img_data)

                        # Save the image
                        img_filename = f"{base_name}_fig_{image_counter}.png"
                        img_path = self.config.output_img_dir / img_filename

                        try:
                            img_bytes = base64.b64decode(img_data)
                            with open(img_path, "wb") as img_file:
                                img_file.write(img_bytes)

                            # Add a reference in the markdown
                            md_content.append(
                                f"\n![Extracted Figure {image_counter}]({img_path.resolve()})\n"
                            )
                            image_counter += 1
                        except Exception as e:
                            logger.error(f"Failed to decode image in cell: {e}")

        # Write the combined markdown content
        md_output_path = self.config.output_md_dir / f"{base_name}_extracted.md"
        with open(md_output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))

        logger.info(f"Extracted notebook {notebook_path} to {md_output_path}")
        return md_output_path

    def extract_latex(self, notebook_path: str | Path, output_tex_path: str | Path) -> Path | None:
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
            "\\chapter{Notebook Code Appendix}",
            "This appendix contains selected code snippets and generated figures extracted directly from the author's VAE homework notebook.",
            "",
        ]

        image_counter = 1
        cells_processed = 0
        base_name = notebook_path.stem

        cells = notebook_data.get("cells", [])

        last_markdown_header = "Extracted Code Snippet"
        
        # We want to select interesting cells (with images or long code).
        for cell in cells:
            cell_type = cell.get("cell_type")
            source = cell.get("source", [])
            source_text = "".join(source) if isinstance(source, list) else str(source)

            if cell_type == "markdown" and source_text.strip():
                lines = source_text.strip().splitlines()
                if lines:
                    # Clean up the markdown header for LaTeX safety (escape _ and &)
                    header = lines[0].lstrip('#').strip().replace('_', '\\_').replace('&', '\\&')
                    if header:
                        last_markdown_header = header

            if cell_type == "code" and source_text.strip():
                # Check if it has an image output
                has_image = False
                outputs = cell.get("outputs", [])
                for output in outputs:
                    data = output.get("data", {})
                    if "image/png" in data or "application/pdf" in data:
                        has_image = True
                        break

                # Only include cells that are either substantial or have images
                if len(source_text.splitlines()) > 5 or has_image:
                    cells_processed += 1
                    tex_content.append(f"\\section*{{{last_markdown_header}}}")
                    tex_content.append("\\begin{lstlisting}[language=Python]")
                    
                    code_lines = source_text.strip().splitlines()
                    if len(code_lines) > 15:
                        truncated_code = "\n".join(code_lines[:15]) + "\n\n# ... (Code truncated for brevity)"
                    else:
                        truncated_code = "\n".join(code_lines)
                        
                    tex_content.append(truncated_code)
                    tex_content.append("\\end{lstlisting}")

                    for output in outputs:
                        data = output.get("data", {})
                        if "image/png" in data or "application/pdf" in data:
                            img_ext = "pdf" if "application/pdf" in data else "png"
                            img_data = data.get("application/pdf") or data.get("image/png")
                            if isinstance(img_data, list):
                                img_data = "".join(img_data)

                            img_filename = f"{base_name}_fig_{image_counter}.{img_ext}"
                            img_path = img_dir / img_filename

                            try:
                                img_bytes = base64.b64decode(img_data)
                                with open(img_path, "wb") as img_file:
                                    img_file.write(img_bytes)

                                tex_content.append("\\begin{figure}[h]")
                                tex_content.append("\\centering")
                                tex_content.append(
                                    f"\\includegraphics[width=0.8\\textwidth]{{figures/{img_filename}}}"
                                )
                                tex_content.append(
                                    f"\\caption{{Extracted Figure {image_counter}}}"
                                )
                                tex_content.append("\\end{figure}")
                                tex_content.append("")
                                image_counter += 1
                            except Exception as e:
                                logger.error(f"Failed to decode image in cell: {e}")

        with open(output_tex_path, "w", encoding="utf-8") as f:
            f.write("\n".join(tex_content))

        logger.info(f"Extracted notebook to LaTeX: {output_tex_path}")
        return output_tex_path
