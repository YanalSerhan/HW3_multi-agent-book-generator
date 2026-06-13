"""Post-processing utilities for LaTeX rendering."""

import re


def post_process_latex(rendered: str) -> str:
    """Apply post-processing regexes to fix tables and Hebrew directionality."""
    # 1. Convert tabular to tabularx
    rendered = re.sub(
        r"\\begin\{tabular\}\{([^}]*)\}",
        lambda m: (
            r"\begin{tabularx}{\textwidth}{"
            + m.group(1).replace("l", "X").replace("c", "X").replace("r", "X")
            + "}"
        ),
        rendered,
    )
    rendered = rendered.replace(r"\end{tabular}", r"\end{tabularx}")

    # Fix empty chapter "hebrew"
    rendered = re.sub(r"\\chapter\*?\{hebrew\}", "", rendered, flags=re.IGNORECASE)

    # 2. Extract and clean math blocks to protect them from regex wrapping
    math_pattern = re.compile(
        r"("
        r"\\\(.*?\\\)"
        r"|\\\[.*?\\\]"
        r"|\$\$.*?\$\$"
        r"|\$[^\$\n]*?\$"
        r"|\\begin\{equation\*?\}.*?\\end\{equation\*?\}"
        r"|\\begin\{align\*?\}.*?\\end\{align\*?\}"
        r"|\\begin\{gather\*?\}.*?\\end\{gather\*?\}"
        r"|\\begin\{multline\*?\}.*?\\end\{multline\*?\}"
        r")",
        flags=re.DOTALL,
    )

    math_blocks: list[str] = []

    def strip_lre_from_math(math_text: str) -> str:
        while True:
            idx = math_text.find("\\LRE{")
            if idx == -1:
                break
            brace_count = 1
            close_idx = -1
            for i in range(idx + 5, len(math_text)):
                if math_text[i] == "{":
                    brace_count += 1
                elif math_text[i] == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        close_idx = i
                        break
            if close_idx != -1:
                math_text = (
                    math_text[:idx]
                    + math_text[idx + 5 : close_idx]
                    + math_text[close_idx + 1 :]
                )
            else:
                math_text = math_text[:idx] + math_text[idx + 5 :]
        return math_text

    def extract_math(match: re.Match[str]) -> str:
        block = match.group(0)
        cleaned_block = strip_lre_from_math(block)
        placeholder = f"%%MATH_BLOCK_{len(math_blocks)}%%"
        math_blocks.append(cleaned_block)
        return placeholder

    rendered = math_pattern.sub(extract_math, rendered)

    # 3. Balance Hebrew environments
    hebrew_count = 0

    def balance_hebrew(match: re.Match[str]) -> str:
        nonlocal hebrew_count
        tag = match.group(0)
        if "begin" in tag:
            hebrew_count += 1
            return tag
        elif "end" in tag:
            if hebrew_count > 0:
                hebrew_count -= 1
                return tag
            else:
                return "% stripped unmatched end{hebrew}"
        else:
            return ""

    rendered = re.sub(r"\\begin\{hebrew\}|\\end\{hebrew\}", balance_hebrew, rendered)

    # Wrap captions containing Hebrew in \texthebrew
    def fix_caption(match: re.Match[str]) -> str:
        content = match.group(1)
        # Avoid double wrapping if already wrapped in \texthebrew{...}
        if content.startswith(r"\texthebrew{") and content.endswith("}"):
            return match.group(0)
        if re.search(r"[\u0590-\u05FF]", content):
            return f"\\caption{{\\texthebrew{{{content}}}}}"
        return match.group(0)

    rendered = re.sub(r"\\caption\{(.*?)\}", fix_caption, rendered)

    # Wrap English phrases inside Hebrew environments in \LRE
    def wrap_english(match: re.Match[str]) -> str:
        content = match.group(1)
        # Avoid wrapping if already wrapped
        content = re.sub(r"(?<!\\LRE\{)(\([A-Za-z][A-Za-z0-9\s-]*\))", r"\\LRE{\1}", content)
        return "\\begin{hebrew}" + content + "\\end{hebrew}"

    rendered = re.sub(
        r"\\begin\{hebrew\}(.*?)\\end\{hebrew\}", wrap_english, rendered, flags=re.DOTALL
    )



    # Close any unclosed hebrew environments right before \end{document}
    if hebrew_count > 0:
        rendered = rendered.replace(
            "\\end{document}", ("\\end{hebrew}\n" * hebrew_count) + "\\end{document}"
        )

    # 4. Clean up any nested \LRE and \texthebrew wrappers
    # These might have been nested from prior runs or because of matching overlap
    while True:
        new_rendered = re.sub(r"\\LRE\{\s*\\LRE\{([^{}]*)\}\s*\}", r"\\LRE{\1}", rendered)
        new_rendered = re.sub(
            r"\\texthebrew\{\s*\\texthebrew\{([^{}]*)\}\s*\}", r"\\texthebrew{\1}", new_rendered
        )
        if new_rendered == rendered:
            break
        rendered = new_rendered

    # 5. Restore math blocks
    for i, block in enumerate(math_blocks):
        placeholder = f"%%MATH_BLOCK_{i}%%"
        rendered = rendered.replace(placeholder, block)

    return rendered
