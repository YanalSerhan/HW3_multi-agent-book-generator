# CrewAI Multi-Agent Book Generator
A production-grade multi-agent AI system powered by CrewAI that autonomously generates professional PDF books compiled from LaTeX source.

## Installation
1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh
2. Run `make install` or `uv sync`

## Usage
1. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.
2. Run the pipeline: `make run` or `uv run crewai-book run --topic "Your Topic"`

## macOS Setup
To run this project natively on macOS, ensure you have the following dependencies installed:
1. **MacTeX**: Install via Homebrew: `brew install --cask mactex-no-gui`
2. **Verify TeX**: Ensure `xelatex` and `biber` are on your PATH.
3. **uv**: Install the python package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
4. **Environment**: Copy `.env.example` to `.env` and configure both `OPENAI_API_KEY` and `SERPER_API_KEY`.
5. **Fonts**: Note that `preamble.tex` relies on the standard `Arial` font to render Hebrew text correctly.

## Configuration
All configuration parameters are driven by the `.env` file and `config/settings.json`.

## Contribution
Check the `docs/DEVELOPER_GUIDE.md` for detailed instructions on contributing to this project.

## License
MIT License.