# pyrefly: ignore [missing-import]
from crewai_book.latex.post_processor import post_process_latex


def test_nested_lre_in_math():
    """Test that strip_lre_from_math removes \\LRE{} inside math blocks."""
    # Test line 45-62 (strip_lre_from_math)
    latex = r"Some math $\alpha + \LRE{English} = \beta$."
    processed = post_process_latex(latex)
    assert r"$\alpha + English = \beta$" in processed

def test_unmatched_end_hebrew():
    """Test unmatched end{hebrew} is stripped."""
    # Test lines 88-90
    latex = r"Hello \end{hebrew} World"
    processed = post_process_latex(latex)
    assert r"\end{hebrew}" not in processed
    assert r"% stripped unmatched end{hebrew}" in processed

def test_caption_with_hebrew():
    """Test caption containing Hebrew is wrapped in texthebrew."""
    # Test lines 96-102
    latex = r"\caption{שלום}"
    processed = post_process_latex(latex)
    assert r"\caption{\texthebrew{שלום}}" in processed

    # Ensure no double wrapping
    latex_wrapped = r"\caption{\texthebrew{שלום}}"
    processed_wrapped = post_process_latex(latex_wrapped)
    assert r"\caption{\texthebrew{שלום}}" in processed_wrapped

def test_unclosed_begin_hebrew_before_end_document():
    """Test unclosed begin{hebrew} gets closed before end{document}."""
    # Test line 121
    latex = r"\begin{hebrew} text \end{document}"
    processed = post_process_latex(latex)
    assert r"\end{hebrew}" + "\n" + r"\end{document}" in processed

def test_nested_wrappers():
    """Test cleanup of nested \\LRE and \\texthebrew wrappers."""
    # Test line 134
    latex = r"\LRE{\LRE{nested}} and \texthebrew{\texthebrew{nested_heb}}"
    processed = post_process_latex(latex)
    assert r"\LRE{nested}" in processed
    assert r"\texthebrew{nested_heb}" in processed
    assert r"\LRE{\LRE" not in processed

def test_multiple_braces_in_math_lre():
    """Test math block stripping with multiple braces."""
    # Covers deeper loop in strip_lre_from_math
    latex = r"$\LRE{text \textbf{bold}} + 1$"
    processed = post_process_latex(latex)
    assert r"$text \textbf{bold} + 1$" in processed
