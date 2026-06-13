# PRD: LaTeX System Mechanism

## 1. Background
The core output of this pipeline is a high-quality academic book. The LaTeX System Mechanism is responsible for taking the structured markdown outputs from the LLM agents and transforming them into valid, compilable XeLaTeX code.

## 2. Requirements
- **Dynamic Book Structuring**: Must translate an `Article` Pydantic model (containing Chapters and Sections) into standard `\chapter{}` and `\section{}` commands.
- **BiDi (Bidirectional) Support**: The system must flawlessly support mixing LTR (English) and RTL (Hebrew) text. 
- **Math Protection**: Mathematical formulas (`$x$`, `\[ x \]`, `\begin{equation}`) must be programmatically protected from BiDi directional tags (`\LRE{}`) to prevent compilation errors.
- **Table of Contents Fixes**: The `memoir` class and `polyglossia` often flip the TOC dot leaders and page numbers for RTL languages. The system must include a post-processor script (`aux_processor.py`) to fix `.toc` auxiliary files.

## 3. Architecture
The LaTeX system consists of:
1. **Template Engine**: Jinja2 templates containing the boilerplate (preamble, packages, title page).
2. **Markdown Parser**: Converts LLM markdown (bold, lists, tables) into LaTeX equivalents.
3. **BiDi Post-Processor**: A regex-based Python script that runs between XeLaTeX compilation passes to fix auxiliary files.

## 4. Test Scenarios
- **Special Character Escaping**: Ensure `_`, `%`, `&`, and `$` are properly escaped when they appear in normal text, but left intact when inside math blocks.
- **BiDi Compilation**: Verify a chapter written entirely in Hebrew with English acronyms compiles correctly without flipping the document margin.
- **TOC Integrity**: Verify that page numbers in the Table of Contents strictly align on the right margin, even for Hebrew chapter titles.
