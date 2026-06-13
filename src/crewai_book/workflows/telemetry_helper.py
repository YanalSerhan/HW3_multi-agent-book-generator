"""Helper function to generate the telemetry appendix for the book compiler."""

from pathlib import Path

from ..domain.state import PipelineState
from ..observability.logger import get_logger

logger = get_logger("workflows.telemetry_helper")


def generate_telemetry_appendix(
    state: PipelineState, latex_dir: Path, run_notes: str = ""
) -> None:
    """Generate the telemetry appendix with charts and metrics."""
    try:
        tokens = (
            sum(state.artifacts.get("tokens", {}).values())
            if "tokens" in state.artifacts
            else "N/A"
        )
        cost = "0.00"
        retries = state.retries_used
        gates = len(state.quality_gates_passed)
        hallucinations = state.artifacts.get("hallucination_count", "N/A")
        latency = state.artifacts.get("latency", {})

        disclaimer = (
            "\\textit{Note: Token figures estimated from output sizes; per-call usage not captured in this run.}\\\\"
            if state.artifacts.get("tokens_estimated", False)
            else ""
        )

        fig_path = latex_dir / "figures" / "telemetry_chart.png"
        fig_path.parent.mkdir(parents=True, exist_ok=True)

        chart_latex = "% No latency data available to plot."
        if latency:
            try:
                import matplotlib

                matplotlib.use("Agg")
                import matplotlib.pyplot as plt

                stages = list(latency.keys())
                times = list(latency.values())
                plt.figure(figsize=(8, 4))
                plt.bar(stages, times, color="skyblue")
                plt.title("Pipeline Stage Latency (seconds)")
                plt.ylabel("Seconds")
                plt.tight_layout()
                plt.savefig(fig_path)
                plt.close()
                chart_latex = r"""
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{telemetry_chart.png}
    \caption{Pipeline Latency by Stage}
\end{figure}
"""
            except ImportError as e:
                logger.warning(f"Matplotlib not available, skipping chart: {e}")
                chart_latex = "% Matplotlib not installed, skipping chart."

        tex = f"""
\\chapter{{Pipeline Run Statistics}}
This appendix provides a snapshot of the multi-agent pipeline's telemetry and performance metrics.

\\section{{Execution Metrics}}
{disclaimer}
\\begin{{table}}[h]
\\centering
\\begin{{tabular}}{{|l|l|}}
\\hline
\\textbf{{Metric}} & \\textbf{{Value}} \\\\ \\hline
Total Tokens Used & {tokens} \\\\ \\hline
Estimated Cost (\\$) & {cost} \\\\ \\hline
Retries Invoked & {retries} \\\\ \\hline
Quality Gates Passed & {gates} \\\\ \\hline
Hallucinations Detected & {hallucinations} \\\\ \\hline
\\end{{tabular}}
\\caption{{Pipeline Execution Metrics}}
\\end{{table}}

\\section{{Performance Analysis}}
{chart_latex}
"""
        if run_notes:
            tex += f"\\section{{Run Notes}}\n{run_notes}\n"
        (latex_dir / "telemetry.tex").write_text(tex, encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to generate telemetry appendix: {e}")
        (latex_dir / "telemetry.tex").write_text(
            "\\chapter{Pipeline Run Statistics}\nFailed to generate metrics.", encoding="utf-8"
        )
