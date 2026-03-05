"""
Prompt construction for Groq LLM calls (Phase 3).

This module is responsible for turning user preferences and a small set of
candidate restaurants into a prompt string that can be sent to an LLM.
"""

from __future__ import annotations

from typing import Iterable, Mapping

import pandas as pd

from ..phase2.preferences import UserPreferences


def _format_restaurant_row(row: Mapping[str, object]) -> str:
    parts: list[str] = []
    name = row.get("name") or "Unknown"
    parts.append(f"Name: {name}")

    location = row.get("location")
    if location:
        parts.append(f"Location: {location}")

    cuisines = row.get("cuisines")
    if cuisines:
        parts.append(f"Cuisines: {cuisines}")

    rate = row.get("rate")
    if rate:
        parts.append(f"Rating: {rate}")

    cost = row.get("approx_cost(for two people)")
    if cost:
        parts.append(f"Approx cost for two: {cost}")

    rest_type = row.get("rest_type")
    if rest_type:
        parts.append(f"Type: {rest_type}")

    return " | ".join(parts)


def build_recommendation_prompt(
    prefs: UserPreferences,
    restaurants: pd.DataFrame,
    *,
    max_items: int = 15,
) -> str:
    """
    Build a textual prompt summarizing the user preferences and a list of
    candidate restaurants for the LLM.
    """

    lines: list[str] = []

    lines.append(
        "You are an expert restaurant recommendation assistant. "
        "Given the user preferences and the candidate restaurants below, "
        "select the best few options and explain briefly why they are suitable."
    )

    # Preferences section.
    lines.append("\nUser preferences:")
    if prefs.place:
        lines.append(f"- Location: {prefs.place}")
    if prefs.min_rating is not None:
        lines.append(f"- Minimum rating: {prefs.min_rating}")
    if prefs.price_band:
        lines.append(f"- Price band: {prefs.price_band.value}")
    if prefs.cuisines:
        lines.append(f"- Preferred cuisines: {', '.join(prefs.cuisines)}")
    if len(lines) == 2:  # no preferences lines added
        lines.append("- (No specific preferences provided)")

    # Candidate restaurants.
    lines.append("\nCandidate restaurants:")
    subset = restaurants.head(max_items)
    if subset.empty:
        lines.append("- (No candidates available; explain that you cannot recommend anything.)")
    else:
        for idx, (_, row) in enumerate(subset.iterrows(), start=1):
            lines.append(f"{idx}. {_format_restaurant_row(row)}")

    # Instruction for the LLM.
    lines.append(
        "\nRespond with a concise list of the best 3–5 restaurants from the candidates, "
        "each with a short explanation tailored to the user's preferences."
    )

    return "\n".join(lines)


__all__ = [
    "build_recommendation_prompt",
]

