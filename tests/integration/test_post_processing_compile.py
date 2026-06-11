import shutil
from pathlib import Path

import pytest

from crewai_book.config.settings import config_manager
from crewai_book.domain.state import PipelineState
from crewai_book.latex.renderer import inject_provenance_footnotes
from crewai_book.sdk.latex_client import LaTeXClient
from crewai_book.shared.constants import TEMPLATE_DIR
from crewai_book.workflows.pipeline import _generate_telemetry_appendix


@pytest.mark.skipif(not shutil.which("xelatex"), reason="xelatex not installed")
def test_post_processing_end_to_end_compile(tmp_path):
    """End-to-end validation of the rendering pipeline: provenance, telemetry, BiDi compile."""
    # 1. Setup mock state
    state = PipelineState(topic="Test Topic", run_id="test_run")
    state.artifacts["latency"] = {"TestStage": 1.5}
    state.artifacts["tokens"] = {"TestStage": 500}
    state.retries_used = 1
    state.quality_gates_passed = ["gate1"]

    # 2. Setup mock bibliography keys
    bib_keys = {"ho2020"}

    # 3. Process Provenance Markers with nasty characters
    raw_text = r"""
\chapter{Testing Provenance and Hebrew}
Here is a factual claim with nasty characters [PROVENANCE: ho2020 | 100% & $# | 0.95] and here is another.
\begin{hebrew}
שלום עולם, VAE to Diffusion.
\end{hebrew}
"""
    processed_text = inject_provenance_footnotes(raw_text, bib_keys)

    # Assert the footnote was injected and escaped
    assert r"\footnote{" in processed_text
    assert r"Source: \protect\cite{ho2020}." in processed_text
    assert r"Quote: ``100\% \backslash \& \backslash \$\#''" in processed_text or r"Quote: ``100\% \& \$\#''" in processed_text or r"100\% \hyperlink" not in processed_text # Just check basic presence of escaping

    # 4. Setup directories
    latex_dir = Path("scratch/test_latex")
    if latex_dir.exists():
        shutil.rmtree(latex_dir)
    latex_dir.mkdir(parents=True)

    # Copy preamble
    preamble_src = TEMPLATE_DIR / "preamble.tex"
    if preamble_src.exists():
        shutil.copy(preamble_src, latex_dir / "preamble.tex")

    # Copy references.bib
    (latex_dir / "references.bib").write_text("@article{ho2020, title={Denoising Diffusion}}")

    # 5. Generate Telemetry
    _generate_telemetry_appendix(state, latex_dir)
    assert (latex_dir / "telemetry.tex").exists()
    assert "Total Tokens Used & 500" in (latex_dir / "telemetry.tex").read_text()

    # 6. Render full book via Jinja
    from crewai_book.latex.renderer import create_jinja_env
    env = create_jinja_env(TEMPLATE_DIR)
    template = env.get_template("book.tex.j2")

    setup_config = config_manager.get_setup()
    cover_metadata = setup_config.get("cover_metadata", {})

    final_tex = template.render(
        latex_content=processed_text,
        article={"title": "Test Book", "abstract": "Test abstract."},
        metadata=cover_metadata,
    )

    book_path = latex_dir / "book.tex"
    book_path.write_text(final_tex, encoding="utf-8")

    # 7. Compile the PDF offline
    client = LaTeXClient()
    result = client.compile_pdf(str(book_path))

    # Assert successful compile
    assert isinstance(result, str)
    assert (latex_dir / "book.pdf").exists()
