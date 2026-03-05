"""
Response formatting utilities for Phase 4.

These helpers convert ranked restaurant rows and raw LLM output into the
stable JSON shape described by the Pydantic models.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd

from .schemas import RecommendationItem, RecommendationResponse


def build_recommendation_response(
    ranked: pd.DataFrame,
    llm_text: str,
    *,
    max_items: int = 5,
) -> RecommendationResponse:
    """
    Construct a RecommendationResponse from a ranked DataFrame and the
    LLM's textual summary.
    """

    items: list[RecommendationItem] = []
    subset = ranked.head(max_items)

    for _, row in subset.iterrows():
        items.append(
            RecommendationItem(
                name=str(row.get("name") or "Unknown"),
                location=row.get("location"),
                rating=str(row.get("rate")) if row.get("rate") is not None else None,
                approx_cost_for_two=str(row.get("approx_cost(for two people)"))
                if row.get("approx_cost(for two people)") is not None
                else None,
                cuisines=row.get("cuisines"),
                rest_type=row.get("rest_type"),
                votes=int(row.get("votes")) if row.get("votes") is not None else None,
            )
        )

    return RecommendationResponse(recommendations=items, llm_summary=llm_text)


__all__ = [
    "build_recommendation_response",
]

