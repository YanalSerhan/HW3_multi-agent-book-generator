"""Security utilities for input sanitization."""

import re


def sanitize_latex(text: str) -> str:
    r"""Escape special LaTeX characters from untrusted input to prevent injection.

    Escapes: &, %, $, #, _, {, }, ~, ^, \
    """
    if not text:
        return text

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    # Use a single regex pass to avoid replacing already-replaced parts
    pattern = re.compile("|".join(re.escape(k) for k in replacements))
    return pattern.sub(lambda m: replacements[m.group(0)], text)
