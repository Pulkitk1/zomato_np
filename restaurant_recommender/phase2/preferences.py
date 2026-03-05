"""
Preference models and parsing utilities for Phase 2.

These models are intentionally simple and assume that upstream consumers
provide already-structured data (e.g. numbers or canonical strings),
not raw natural language.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional


class PriceBand(str, Enum):
    """Simple categorical representation of price."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class PreferenceInput:
    """
    Raw, structured preference input.

    All fields are optional; missing values simply mean "no constraint" for
    that dimension.
    """

    place: Optional[str] = None
    min_rating: Optional[float] = None
    price_band: Optional[PriceBand] = None
    cuisines: Optional[Iterable[str]] = None
    max_budget: Optional[float] = None


@dataclass(frozen=True)
class UserPreferences:
    """
    Normalized user preferences used by the filtering layer.
    """

    place: Optional[str]
    min_rating: Optional[float]
    price_band: Optional[PriceBand]
    cuisines: tuple[str, ...]
    max_budget: Optional[float]


def parse_preferences(raw: PreferenceInput) -> UserPreferences:
    """
    Normalize a PreferenceInput into a UserPreferences instance.

    - `place` is lowercased for case-insensitive matching.
    - `cuisines` are normalized to lower case and stored as a tuple.
    """

    place = raw.place.lower().strip() if raw.place else None
    cuisines: tuple[str, ...] = ()
    if raw.cuisines:
        cuisines = tuple(sorted({c.strip().lower() for c in raw.cuisines if c.strip()}))

    return UserPreferences(
        place=place,
        min_rating=raw.min_rating,
        price_band=raw.price_band,
        cuisines=cuisines,
        max_budget=raw.max_budget,
    )


__all__ = [
    "PriceBand",
    "PreferenceInput",
    "UserPreferences",
    "parse_preferences",
]

