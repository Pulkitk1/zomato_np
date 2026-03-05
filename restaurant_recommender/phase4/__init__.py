"""
Phase 4: response shaping and API.

This subpackage exposes:
- Pydantic models for the external API contract.
- A formatter that converts ranked restaurant rows and LLM text into a
  stable JSON response.
- A FastAPI application that wires together Phases 1–3 behind a single
  `/recommend` endpoint.
"""

from .schemas import PreferenceRequest, RecommendationItem, RecommendationResponse
from .formatter import build_recommendation_response
from .api import app

__all__ = [
    "PreferenceRequest",
    "RecommendationItem",
    "RecommendationResponse",
    "build_recommendation_response",
    "app",
]

