# pyrefly: ignore [missing-import]
import json
from pathlib import Path

# pyrefly: ignore [missing-import]
from crewai_book.tools.nb_latex_extractor import extract_notebook_to_latex


def test_extract_notebook_to_latex_valid(tmp_path: Path) -> None:
    notebook_data = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["## A Valid Title\n", "Some normal markdown."]
            },
            {
                "cell_type": "markdown",
                "source": ["### A Subtitle\n"]
            },
            {
                "cell_type": "code",
                "source": "print('short')",
                "outputs": []
            },
            {
                "cell_type": "code",
                "source": "\n".join([f"line {i}" for i in range(20)]),
                "outputs": [
                    {
                        "data": {"image/png": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="}
                    }
                ]
            }
        ]
    }

    nb_file = tmp_path / "valid_nb.ipynb"
    nb_file.write_text(json.dumps(notebook_data), encoding="utf-8")

    tex_file = tmp_path / "out" / "valid_nb.tex"
    tex_file.parent.mkdir(parents=True)

    result = extract_notebook_to_latex(nb_file, tex_file)
    assert result is not None
    assert result.exists()

    content = result.read_text(encoding="utf-8")
    assert r"\section{A Valid Title}" in content
    assert r"\subsection{A Subtitle}" in content
    assert r"\section*{Implementation Step 1}" in content
    assert r"\begin{lstlisting}[language=Python]" in content
    assert r"\end{lstlisting}" in content
    assert "(Code truncated for brevity)" in content
    assert r"\includegraphics" in content

    img_dir = tex_file.parent / "figures"
    img_files = list(img_dir.glob("*.png"))
    assert len(img_files) == 1

def test_extract_notebook_to_latex_missing_file(tmp_path: Path) -> None:
    result = extract_notebook_to_latex(tmp_path / "does_not_exist.ipynb", tmp_path / "out.tex")
    assert result is None

def test_extract_notebook_to_latex_malformed(tmp_path: Path) -> None:
    nb_file = tmp_path / "invalid.ipynb"
    nb_file.write_text("This is not valid json", encoding="utf-8")

    result = extract_notebook_to_latex(nb_file, tmp_path / "out.tex")
    assert result is None

def test_extract_notebook_to_latex_skips_submission(tmp_path: Path) -> None:
    notebook_data = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["**Submission date**: 2026-06-13"]
            },
            {
                "cell_type": "markdown",
                "source": ["Exercise 5: Diffusion"]
            },
            {
                "cell_type": "markdown",
                "source": ["## Keep this\n", "This should stay."]
            }
        ]
    }
    nb_file = tmp_path / "sub_nb.ipynb"
    nb_file.write_text(json.dumps(notebook_data), encoding="utf-8")
    tex_file = tmp_path / "sub_nb.tex"

    result = extract_notebook_to_latex(nb_file, tex_file)
    assert result is not None
    content = result.read_text(encoding="utf-8")

    assert "Submission date" not in content
    assert "Exercise 5" not in content
    assert r"\section{Keep this}" in content
