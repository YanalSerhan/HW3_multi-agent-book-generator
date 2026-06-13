# pyrefly: ignore [missing-import]
import json
from pathlib import Path

# pyrefly: ignore [missing-import]
from crewai_book.tools.nb_extractor import NotebookExtractor, NotebookExtractorConfig


def test_extract_valid_notebook(tmp_path: Path) -> None:
    config = NotebookExtractorConfig(
        output_md_dir=tmp_path / "md_out",
        output_img_dir=tmp_path / "img_out",
    )
    extractor = NotebookExtractor(config)

    notebook_data = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["# Title\n", "Some markdown text."]
            },
            {
                "cell_type": "code",
                "source": "print('hello')",
                "outputs": [
                    {
                        "data": {"image/png": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="}
                    }
                ]
            }
        ]
    }
    nb_file = tmp_path / "test_nb.ipynb"
    nb_file.write_text(json.dumps(notebook_data), encoding="utf-8")

    result = extractor.extract(nb_file)

    assert result is not None
    assert result.exists()

    content = result.read_text(encoding="utf-8")
    assert "# Title" in content
    assert "Some markdown text." in content
    assert "```python" in content
    assert "print('hello')" in content
    assert "![Extracted Figure 1]" in content

    # Check if image was saved
    img_files = list(config.output_img_dir.glob("*.png"))
    assert len(img_files) == 1
    assert img_files[0].name == "test_nb_fig_1.png"

def test_extract_non_existent_file(tmp_path: Path) -> None:
    extractor = NotebookExtractor()
    result = extractor.extract(tmp_path / "does_not_exist.ipynb")
    assert result is None

def test_extract_invalid_json(tmp_path: Path) -> None:
    nb_file = tmp_path / "invalid.ipynb"
    nb_file.write_text("This is not valid json", encoding="utf-8")

    extractor = NotebookExtractor()
    result = extractor.extract(nb_file)
    assert result is None
