import os

import pandas as pd
import pytest
from dotenv import load_dotenv
from groq import AuthenticationError

from restaurant_recommender.data_loader import load_core_dataframe
from restaurant_recommender.phase2 import (
    PreferenceInput,
    PriceBand,
    filter_restaurants,
    parse_preferences,
    rank_restaurants,
)
from restaurant_recommender.phase3 import GroqLLMClient


@pytest.mark.integration
def test_groq_end_to_end_recommendation():
    """
    End-to-end integration test for Phase 3.

    This test:
    - Loads a small sample from the dataset.
    - Applies simple Phase 2 filtering and ranking.
    - Calls the Groq LLM via GroqLLMClient.

    It is intentionally light on assertions because LLM output is
    non-deterministic, but it verifies that a non-empty response is
    returned without raising errors.
    """

    # Ensure values from .env are loaded into the environment for this test run.
    load_dotenv(override=False)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        pytest.skip("GROQ_API_KEY not set; skipping Groq integration test.")

    # Phase 1: load sample data.
    df: pd.DataFrame = load_core_dataframe(sample_size=400)

    # Phase 2: build preferences, filter, and rank.
    prefs = parse_preferences(
        PreferenceInput(
            place="bangalore",
            min_rating=4.0,
            price_band=PriceBand.MEDIUM,
            cuisines=["north indian"],
        )
    )
    filtered = filter_restaurants(df, prefs)
    ranked = rank_restaurants(filtered, top_k=15)

    # Even if filtering is very strict, we want to ensure we always have
    # at least a few candidates to send; if not, relax the filters.
    if ranked.empty:
        prefs = parse_preferences(
            PreferenceInput(
                place=None,
                min_rating=3.5,
                price_band=None,
                cuisines=None,
            )
        )
        filtered = filter_restaurants(df, prefs)
        ranked = rank_restaurants(filtered, top_k=15)

    assert not ranked.empty

    # Phase 3: call Groq.
    client = GroqLLMClient(api_key=api_key)
    try:
        response_text = client.recommend(prefs, ranked, max_items=10)
    except AuthenticationError as exc:
        pytest.skip(f"Groq authentication failed (likely invalid API key): {exc}")

    assert isinstance(response_text, str)
    assert response_text.strip(), "Groq response should not be empty"

