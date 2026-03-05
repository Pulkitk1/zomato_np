"""
Pydantic models for the public API contract (Phase 4).
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class PreferenceRequest(BaseModel):
    """
    Request body sent to the /recommend endpoint.
    """

    place: Optional[str] = Field(
        default=None, description="Preferred location, e.g. 'Bangalore' or an area name."
    )
    min_rating: Optional[float] = Field(
        default=None, description="Minimum acceptable rating (e.g. 4.0)."
    )
    price_band: Optional[str] = Field(
        default=None,
        description="One of 'low', 'medium', 'high'; interpreted heuristically from cost. Optional.",
    )
    budget: Optional[float] = Field(
        default=None,
        ge=0,
        description="Maximum budget for two people. Restaurants with cost <= budget are returned.",
    )
    cuisines: Optional[List[str]] = Field(
        default=None,
        description="List of preferred cuisines such as ['north indian', 'italian'].",
    )


class RecommendationItem(BaseModel):
    """
    One restaurant recommendation in the API response.
    """

    name: str
    location: Optional[str] = None
    rating: Optional[str] = None
    approx_cost_for_two: Optional[str] = None
    cuisines: Optional[str] = None
    rest_type: Optional[str] = None
    votes: Optional[int] = None


class RecommendationResponse(BaseModel):
    """
    Top-level response containing structured recommendations and the
    original LLM summary text.
    """

    recommendations: List[RecommendationItem]
    llm_summary: str


__all__ = [
    "PreferenceRequest",
    "RecommendationItem",
    "RecommendationResponse",
]

