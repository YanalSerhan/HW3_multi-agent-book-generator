"""Quality gate data models."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from ..domain.state import PipelineState


class PipelineStage(StrEnum):
    """Stages of the book generation pipeline."""

    RESEARCH = "research"
    MAIN = "main"
    EDITORIAL = "editorial"
    POST_PROCESSING = "post_processing"
    QA = "qa"


@dataclass
class QualityGateResult:
    """Result of evaluating a quality gate."""

    passed: bool
    message: str


@dataclass
class QualityGate:
    """Definition of a single quality gate."""

    name: str
    stage: PipelineStage
    check: Callable[[PipelineState], QualityGateResult]
    severity: Literal["blocking", "warning"]
    on_failure: Literal["retry", "abort", "human_review"]
