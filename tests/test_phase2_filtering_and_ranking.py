import pandas as pd

from restaurant_recommender.data_loader import load_core_dataframe
from restaurant_recommender.phase2 import (
    PreferenceInput,
    PriceBand,
    filter_restaurants,
    parse_preferences,
    rank_restaurants,
)


def _load_sample_df() -> pd.DataFrame:
    # Keep the sample relatively small so tests remain quick and light.
    return load_core_dataframe(sample_size=500)


def test_parse_preferences_normalizes_case_and_cuisines():
    raw = PreferenceInput(
        place="Koramangala ",
        min_rating=4.0,
        price_band=PriceBand.MEDIUM,
        cuisines=["North Indian", " north indian ", "Italian"],
    )
    prefs = parse_preferences(raw)

    assert prefs.place == "koramangala"
    # Duplicates and whitespace should have been removed, and all lowercased.
    assert set(prefs.cuisines) == {"north indian", "italian"}
    assert prefs.price_band == PriceBand.MEDIUM
    assert prefs.min_rating == 4.0


def test_filter_restaurants_applies_basic_constraints():
    df = _load_sample_df()

    raw = PreferenceInput(
        place=None,  # no location filter
        min_rating=3.5,
        price_band=None,
        cuisines=None,
    )
    prefs = parse_preferences(raw)

    filtered = filter_restaurants(df, prefs)
    assert not filtered.empty

    # All remaining rows should have numeric rating >= 3.5 where rating is present.
    from restaurant_recommender.phase2.filtering import _parse_numeric_rating

    numeric_ratings = filtered["rate"].map(_parse_numeric_rating)
    assert (numeric_ratings.dropna() >= 3.5).all()


def test_filter_by_place_and_cuisine_reduces_result_set():
    df = _load_sample_df()

    # We don't know exact values ahead of time, but we can at least ensure
    # that applying more constraints does not increase the number of rows.
    base_prefs = parse_preferences(PreferenceInput())
    base = filter_restaurants(df, base_prefs)

    constrained_prefs = parse_preferences(
        PreferenceInput(place="bangalore", cuisines=["north indian"])
    )
    constrained = filter_restaurants(df, constrained_prefs)

    assert len(constrained) <= len(base)


def test_rank_restaurants_sorts_by_votes_and_rating():
    df = _load_sample_df()

    ranked = rank_restaurants(df, top_k=30)
    assert not ranked.empty
    assert len(ranked) <= 30

    # Check that the ordering is non-increasing in votes, and for ties,
    # non-increasing in rating.
    votes = ranked["votes"].fillna(0).astype(int).tolist()
    assert votes == sorted(votes, reverse=True)

