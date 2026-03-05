"""
FastAPI application wiring together Phases 1–3 for Phase 4.

Exposes a single POST /recommend endpoint that:
- Accepts user preferences as JSON.
- Loads restaurant data (Phase 1).
- Filters and ranks restaurants (Phase 2).
- Obtains a natural-language summary from Groq (Phase 3).
- Returns a structured JSON response (Phase 4).
"""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException

from restaurant_recommender.data_loader import load_core_dataframe
from restaurant_recommender.phase2 import (
    PreferenceInput,
    PriceBand,
    filter_restaurants,
    parse_preferences,
    rank_restaurants,
)
from restaurant_recommender.phase3 import GroqLLMClient
from restaurant_recommender.phase5 import ui_router
from .formatter import build_recommendation_response
from .schemas import PreferenceRequest, RecommendationResponse


app = FastAPI(title="AI Restaurant Recommendation Service")
app.include_router(ui_router)


def get_groq_client() -> GroqLLMClient:
    """
    Dependency that returns a GroqLLMClient instance.

    Tests can override this dependency to inject a fake client.
    """

    return GroqLLMClient()


ClientDep = Annotated[GroqLLMClient, Depends(get_groq_client)]


@app.get("/meta/locations")
def get_locations() -> list[str]:
    """
    Return all unique locations from the dataset.
    """

    df = load_core_dataframe(sample_size=1000)
    if "location" not in df.columns:
        return []
    values = (
        df["location"]
        .dropna()
        .astype(str)
        .str.strip()
        .replace("", None)
        .dropna()
        .unique()
    )
    return sorted(set(values))


@app.get("/meta/cuisines")
def get_cuisines() -> list[str]:
    """
    Return all unique cuisine strings from the dataset, split on commas.
    """

    df = load_core_dataframe(sample_size=1000)
    if "cuisines" not in df.columns:
        return []
    raw = (
        df["cuisines"]
        .dropna()
        .astype(str)
        .str.split(",")
    )
    cuisines: set[str] = set()
    for parts in raw:
        for part in parts:
            cleaned = part.strip()
            if cleaned:
                cuisines.add(cleaned)
    return sorted(cuisines)


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_endpoint(
    prefs_body: PreferenceRequest,
    client: ClientDep,
) -> RecommendationResponse:
    """
    Main recommendation endpoint used by Phase 5 UI or any other client.
    """

    # Map API-level price_band string into the internal enum.
    price_band_enum: Optional[PriceBand] = None
    if prefs_body.price_band:
        try:
            price_band_enum = PriceBand(prefs_body.price_band.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="price_band must be one of: 'low', 'medium', 'high'.",
            )

    # Validate budget (non-negative). Pydantic enforces numeric type & ge=0
    # but we add a clearer HTTP 400 for negative values just in case.
    if prefs_body.budget is not None and prefs_body.budget < 0:
        raise HTTPException(
            status_code=400,
            detail="budget must be a non-negative number.",
        )

    # Build internal preferences model (Phase 2).
    pref_input = PreferenceInput(
        place=prefs_body.place,
        min_rating=prefs_body.min_rating,
        price_band=price_band_enum,
        cuisines=prefs_body.cuisines,
    )
    prefs = parse_preferences(pref_input)

    # Load data (Phase 1).
    df = load_core_dataframe(sample_size=1500)

    # Apply budget filter early (cost <= budget) if provided.
    if prefs_body.budget is not None and "approx_cost(for two people)" in df.columns:
        def _numeric_cost(val: object) -> float | None:
            if val is None:
                return None
            text = str(val).replace(",", "").strip()
            if not text:
                return None
            try:
                return float(text)
            except ValueError:
                return None

        numeric_costs = df["approx_cost(for two people)"].map(_numeric_cost)
        df = df[numeric_costs <= prefs_body.budget]

    # Apply filtering/ranking (Phase 2).
    filtered = filter_restaurants(df, prefs)
    ranked = rank_restaurants(filtered, top_k=50)

    if ranked.empty:
        raise HTTPException(
            status_code=404,
            detail="No restaurants found matching the given preferences.",
        )

    # Call Groq LLM (Phase 3).
    llm_text = client.recommend(prefs, ranked, max_items=15)

    # Shape response (Phase 4).
    response = build_recommendation_response(ranked, llm_text, max_items=5)
    return response


__all__ = [
    "app",
    "get_groq_client",
]

