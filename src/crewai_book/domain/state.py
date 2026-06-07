from typing import Any

from pydantic import BaseModel, Field, field_validator


class Citation(BaseModel):
    """Represents a single academic source or citation."""

    bibtex_key: str = Field(..., description="The unique BibTeX key for this source")
    title: str = Field(..., description="Title of the paper or book")
    authors: list[str] = Field(..., description="List of author names")
    year: int = Field(..., description="Year of publication")
    venue: str | None = Field(default=None, description="Publication venue (journal, conference)")
    doi: str | None = Field(default=None, description="Digital Object Identifier")
    url: str | None = Field(default=None, description="URL to the paper")
    abstract: str | None = Field(default=None, description="Abstract or summary of the source")
    confidence_score: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Confidence score against hallucinations"
    )

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        """Validate year is within reasonable bounds."""
        if v < 1900 or v > 2100:
            raise ValueError(f"Year {v} is outside valid bounds [1900, 2100]")
        return v


class Bibliography(BaseModel):
    """Collection of verified citations."""

    entries: list[Citation] = Field(default_factory=list, description="List of verified citations")

    def add_citation(self, citation: Citation) -> None:
        """Add a citation if it doesn't already exist by DOI or title."""
        for existing in self.entries:
            if citation.doi and existing.doi == citation.doi:
                return
            if existing.title.lower() == citation.title.lower():
                return
        self.entries.append(citation)


class PipelineState(BaseModel):
    """State tracker for the multi-agent execution pipeline."""

    current_stage: str = Field(
        default="initialization", description="Current stage of the pipeline"
    )
    topic: str = Field(..., description="Main topic being generated")
    run_id: str = Field(..., description="Unique run identifier")
    errors: list[dict[str, Any]] = Field(
        default_factory=list, description="Log of non-fatal errors"
    )
    retries_used: int = Field(
        default=0, description="Total number of retries used across all agents"
    )
    quality_gates_passed: list[str] = Field(
        default_factory=list, description="Gates successfully passed"
    )

    def add_error(self, stage: str, message: str, context: dict[str, Any] | None = None) -> None:
        """Log an error during pipeline execution."""
        self.errors.append({"stage": stage, "message": message, "context": context or {}})

    def mark_gate_passed(self, gate_name: str) -> None:
        """Mark a quality gate as passed."""
        if gate_name not in self.quality_gates_passed:
            self.quality_gates_passed.append(gate_name)
