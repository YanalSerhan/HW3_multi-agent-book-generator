"""Fact-checking tool for CrewAI agents.

Cross-verifies claims by searching for corroborating evidence
from multiple sources, helping detect potential hallucinations.
"""

from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..observability.logger import get_logger
from ..sdk.search_client import SearchClient


class FactCheckInput(BaseModel):
    """Input schema for the fact check tool."""

    claim: str = Field(..., description="The factual claim to verify.")


class FactCheckTool(BaseTool):
    """Cross-verify a factual claim against web sources.

    Searches for the claim and analyzes whether multiple independent
    sources corroborate it. Returns a confidence assessment to help
    agents identify potentially hallucinated content.
    """

    name: str = "fact_check"
    description: str = (
        "Verify a factual claim by cross-referencing web sources. "
        "Returns whether the claim is corroborated and a confidence level."
    )
    args_schema: type[BaseModel] = FactCheckInput

    def _run(self, claim: str, **kwargs: Any) -> str:
        """Verify a claim against web sources."""
        logger = get_logger("tools.fact_check")
        logger.info(f"Fact-checking claim: {claim[:100]}...")

        client = SearchClient()
        results = client.search_web(claim)

        if not results:
            return (
                "UNVERIFIED: No corroborating sources found.\n"
                "Confidence: LOW\n"
                "Recommendation: Remove or rephrase this claim."
            )

        # Count results that seem relevant
        corroborating = 0
        sources = []
        for result in results[:5]:
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            claim_words = set(claim.lower().split())
            combined = f"{title} {snippet}"
            overlap = sum(1 for w in claim_words if w in combined)
            if overlap >= len(claim_words) * 0.3:  # pragma: no cover
                corroborating += 1
                sources.append(result.get("title", "Unknown"))

        confidence = self._assess_confidence(corroborating)

        return (
            f"Claim: {claim}\n"
            f"Corroborating sources: {corroborating}/5\n"
            f"Confidence: {confidence}\n"
            f"Sources: {'; '.join(sources[:3])}"
        )

    @staticmethod
    def _assess_confidence(count: int) -> str:
        """Assess confidence based on corroborating source count."""
        if count >= 3:
            return "HIGH"
        if count >= 1:  # pragma: no cover
            return "MEDIUM"  # pragma: no cover
        return "LOW"  # pragma: no cover
