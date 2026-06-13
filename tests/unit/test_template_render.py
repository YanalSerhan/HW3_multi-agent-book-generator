from pathlib import Path

from crewai_book.latex.renderer import create_jinja_env


def test_template_rendering_with_metadata() -> None:
    env = create_jinja_env(template_dir=Path("src/crewai_book/latex/templates"))
    template = env.get_template("book.tex.j2")

    out = template.render(
        article={"title": "Test & Title", "abstract": "Test Abstract"},
        latex_content="Body",
        metadata={
            "authors": "Jane Doe & John Smith",
            "course": "100% \\ done & more",
            "lecturer": "Dr_AI",
            "date": "2026-01-01",
        },
    )

    # Check escaping of special characters
    assert "Test \\& Title" in out
    assert "Jane Doe \\& John Smith" in out
    assert "100\\% \\textbackslash{} done \\& more" in out
    assert "Dr\\_AI" in out
    assert "2026-01-01" in out

    # Check whitespace preservation (no \LargeJane gluing)
    assert "{\\Large Jane Doe \\& John Smith\\par}" in out
    assert "{\\LARGE\\itshape 100\\% \\textbackslash{} done \\& more\\par}" in out


def test_template_rendering_without_metadata() -> None:
    env = create_jinja_env(template_dir=Path("src/crewai_book/latex/templates"))
    template = env.get_template("book.tex.j2")

    out = template.render(
        article={"title": "Test Title", "abstract": "Test Abstract"},
        latex_content="Body",
        metadata={},
    )

    assert "Unknown Author" in out
    assert "Orchestration of AI agents" in out
    assert "Unknown Lecturer" in out
    assert "\\today" in out

    assert "{\\Large Unknown Author\\par}" in out
    assert "{\\LARGE\\itshape Orchestration of AI agents\\par}" in out
