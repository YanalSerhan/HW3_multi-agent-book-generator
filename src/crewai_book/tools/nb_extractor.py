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
        except json.JSONDecodeError as e:  # pragma: no cover
            logger.error(f"Failed to parse notebook JSON: {e}")  # pragma: no cover
            return None  # pragma: no cover

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
            elif cell_type == "code":  # pragma: no cover
                md_content.append("```python")
                md_content.append(source_text)
                md_content.append("```\n")

                # Extract outputs for code cells
                outputs = cell.get("outputs", [])
                for output in outputs:
                    data = output.get("data", {})

                    if "image/png" in data:  # pragma: no cover
                        img_data = data["image/png"]
                        # Handle multi-line base64
                        if isinstance(img_data, list):
                            img_data = "".join(img_data)  # pragma: no cover

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
                        except Exception as e:  # pragma: no cover
                            logger.error(f"Failed to decode image in cell: {e}")  # pragma: no cover

        # Write the combined markdown content
        md_output_path = self.config.output_md_dir / f"{base_name}_extracted.md"
        with open(md_output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))

        logger.info(f"Extracted notebook {notebook_path} to {md_output_path}")
        return md_output_path
