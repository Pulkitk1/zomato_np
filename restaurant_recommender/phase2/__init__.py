"""
Phase 2: preference modelling, parsing, filtering and ranking.

This subpackage builds on the Phase 1 data loading utilities to:
- Represent user preferences in a structured form.
- Parse simple, structured inputs into that representation.
- Filter the restaurant dataset based on those preferences.
- Apply a simple ranking strategy on the filtered results.
"""

from .preferences import (
    PriceBand,
    PreferenceInput,
    UserPreferences,
    parse_preferences,
)
from .filtering import filter_restaurants, rank_restaurants

__all__ = [
    "PriceBand",
    "PreferenceInput",
    "UserPreferences",
    "parse_preferences",
    "filter_restaurants",
    "rank_restaurants",
]

