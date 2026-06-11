"""Unit tests for the notebook extractor."""

from pathlib import Path

from crewai_book.tools.nb_extractor import NotebookExtractor, NotebookExtractorConfig


def test_notebook_extractor_success(tmp_path: Path) -> None:
    """Test extracting markdown and images from a notebook."""
    config = NotebookExtractorConfig(
        output_md_dir=tmp_path / "md",
        output_img_dir=tmp_path / "img",
    )
    extractor = NotebookExtractor(config)

    nb_path = Path("tests/fixtures/tiny_notebook.ipynb")
    md_path = extractor.extract(nb_path)

    assert md_path is not None
    assert md_path.exists()
    assert md_path.name == "tiny_notebook_extracted.md"

    # Check markdown content
    content = md_path.read_text(encoding="utf-8")
    assert "# VAE Homework" in content
    assert "import matplotlib.pyplot as plt" in content
    assert "![Extracted Figure 1]" in content
    assert "tiny_notebook_fig_1.png" in content

    # Check image was extracted
    img_path = tmp_path / "img" / "tiny_notebook_fig_1.png"
    assert img_path.exists()
    # verify it's a valid png (magic number)
    with open(img_path, "rb") as f:
        header = f.read(8)
        assert header == b"\x89PNG\r\n\x1a\n"


def test_notebook_extractor_not_found(tmp_path: Path) -> None:
    """Test extracting a non-existent notebook."""
    config = NotebookExtractorConfig(
        output_md_dir=tmp_path / "md",
        output_img_dir=tmp_path / "img",
    )
    extractor = NotebookExtractor(config)
    assert extractor.extract("non_existent.ipynb") is None
