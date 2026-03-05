"""
Filtering and ranking logic for Phase 2.

This module operates on pandas DataFrames produced by the Phase 1 data loader.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

from ..config import CORE_COLUMNS
from .preferences import PriceBand, UserPreferences


def _parse_numeric_rating(rate_value: object) -> Optional[float]:
    """
    Convert the string rating format used in the dataset into a float.

    The dataset often stores ratings as strings like "4.1/5" or "4.5".
    """

    if rate_value is None:
        return None
    text = str(rate_value).strip()
    if not text or text in {"NEW", "-"}:
        return None
    # Keep the part before any slash.
    if "/" in text:
        text = text.split("/", 1)[0]
    try:
        return float(text)
    except ValueError:
        return None


def _price_band_from_cost(cost_value: object) -> Optional[PriceBand]:
    """
    Map the 'approx_cost(for two people)' field into a PriceBand.

    The column is typically a string like "800", "1,200", etc.
    Thresholds are heuristic and can be refined later.
    """

    if cost_value is None:
        return None
    text = str(cost_value).replace(",", "").strip()
    if not text:
        return None
    try:
        value = float(text)
    except ValueError:
        return None

    if value <= 500:
        return PriceBand.LOW
    if value <= 1200:
        return PriceBand.MEDIUM
    return PriceBand.HIGH


def filter_restaurants(df: pd.DataFrame, prefs: UserPreferences) -> pd.DataFrame:
    """
    Apply preference-based filtering on the DataFrame.

    This function is deliberately conservative: if a preference field is None
    or empty, it is ignored (no constraint for that dimension).
    """

    filtered = df.copy()

    # Filter by place (location contains substring, case-insensitive).
    if prefs.place and "location" in filtered.columns:
        mask = (
            filtered["location"]
            .astype(str)
            .str.lower()
            .str.contains(prefs.place, na=False)
        )
        filtered = filtered[mask]

    # Filter by minimum rating.
    if prefs.min_rating is not None and "rate" in filtered.columns:
        ratings = filtered["rate"].map(_parse_numeric_rating)
        filtered = filtered[ratings >= prefs.min_rating]

    # Filter by price band.
    if prefs.price_band is not None and "approx_cost(for two people)" in filtered.columns:
        price_bands = filtered["approx_cost(for two people)"].map(_price_band_from_cost)
        filtered = filtered[price_bands == prefs.price_band]

    # Filter by cuisines (requires that each requested cuisine appears as a substring).
    if prefs.cuisines and "cuisines" in filtered.columns:
        cuisines_series = filtered["cuisines"].astype(str).str.lower()
        for cuisine in prefs.cuisines:
            cuisines_series = cuisines_series[cuisines_series.str.contains(cuisine, na=False)]
        filtered = filtered.loc[cuisines_series.index]

    return filtered


def rank_restaurants(df: pd.DataFrame, *, top_k: int = 20) -> pd.DataFrame:
    """
    Rank restaurants using a simple heuristic:
    - Primary key: votes (descending)
    - Secondary key: rating (numeric, descending)
    - Tertiary key: name (ascending for stability)
    """

    working = df.copy()

    # Ensure columns are present; if not, add defaults so sorting works.
    if "votes" not in working.columns:
        working["votes"] = 0
    if "rate" not in working.columns:
        working["rate"] = "0"

    working["_numeric_rate"] = working["rate"].map(_parse_numeric_rating).fillna(0.0)

    working = working.sort_values(
        by=["votes", "_numeric_rate", "name"],
        ascending=[False, False, True],
        kind="mergesort",  # stable sort
    )

    result = working.head(top_k).drop(columns=["_numeric_rate"])
    return result


__all__ = [
    "filter_restaurants",
    "rank_restaurants",
]

