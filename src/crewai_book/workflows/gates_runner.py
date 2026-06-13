"""Quality gates runner for the book generation pipeline."""

from ..domain.state import PipelineState
from ..observability.logger import get_logger
from . import quality_gates as qg
from .gate_models import PipelineStage, QualityGate, QualityGateResult

logger = get_logger("workflows.gates_runner")

QUALITY_GATES = [
    QualityGate(
        name="QG-1",
        stage=PipelineStage.RESEARCH,
        check=qg.check_qg1_sources,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-2",
        stage=PipelineStage.RESEARCH,
        check=qg.check_qg2_hallucinations,
        severity="blocking",
        on_failure="abort",
    ),
    QualityGate(
        name="QG-3",
        stage=PipelineStage.MAIN,
        check=qg.check_qg3_outline,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-4",
        stage=PipelineStage.MAIN,
        check=qg.check_qg4_word_count,
        severity="warning",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-5",
        stage=PipelineStage.EDITORIAL,
        check=qg.check_qg5_readability,
        severity="warning",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-6",
        stage=PipelineStage.EDITORIAL,
        check=qg.check_qg6_review_concerns,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-7",
        stage=PipelineStage.RESEARCH,
        check=qg.check_qg7_citations,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-8",
        stage=PipelineStage.POST_PROCESSING,
        check=qg.check_qg8_compilation,
        severity="blocking",
        on_failure="retry",
    ),
    QualityGate(
        name="QG-9",
        stage=PipelineStage.POST_PROCESSING,
        check=qg.check_qg9_pages,
        severity="blocking",
        on_failure="abort",
    ),
    QualityGate(
        name="QG-10",
        stage=PipelineStage.QA,
        check=qg.check_qg10_qa_signoff,
        severity="blocking",
        on_failure="abort",
    ),
]


def run_all_gates(state: PipelineState) -> dict[str, bool]:
    """Run all quality gates and return a summary.

    Gates are evaluated based on the current state.artifacts.
    Only gates that have the requisite artifacts will pass.

    Args:
        state: Current pipeline state.

    Returns:
        Dict mapping gate names to pass/fail booleans.
    """
    gate_results: dict[str, bool] = {}

    for gate in QUALITY_GATES:
        try:
            result = gate.check(state)
        except Exception as e:
            result = QualityGateResult(False, f"Check failed with error: {e}")

        gate_results[gate.name] = result.passed

        if "not found in state artifacts" not in result.message:
            if result.passed:
                status_str = "PASS"
            else:
                status_str = "WARN" if gate.severity == "warning" else "FAIL"
            logger.info(f"{gate.name} ({gate.stage.value}): {status_str} — {result.message}")

        if result.passed:
            state.mark_gate_passed(gate.name)

    return gate_results
