"""
Groq LLM client integration (Phase 3).

This module provides a thin wrapper around the Groq Python SDK so that
the rest of the application can request restaurant recommendations in
a simple, testable way.

Actual tests that perform live API calls should be added only when a
GROQ_API_KEY is configured in the environment or `.env`.
"""

from __future__ import annotations

import os
from typing import Optional

import pandas as pd
from dotenv import load_dotenv
from groq import Groq

from ..phase2.preferences import UserPreferences
from .prompt_builder import build_recommendation_prompt


class GroqLLMClient:
    """
    High-level client used by the application to obtain recommendations
    from the Groq LLM.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = "llama-3.1-8b-instant",
    ) -> None:
        # Load from .env if present, but allow explicit override.
        load_dotenv(override=False)
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Please configure it in your environment "
                "or in a `.env` file at the project root."
            )

        self._client = Groq(api_key=api_key)
        self._model = model

    @property
    def model(self) -> str:
        return self._model

    def recommend(
        self,
        prefs: UserPreferences,
        candidates: pd.DataFrame,
        *,
        max_items: int = 15,
        temperature: float = 0.3,
    ) -> str:
        """
        Call the Groq LLM with a prompt built from the given preferences and
        candidate restaurants, returning the model's textual response.
        """

        prompt = build_recommendation_prompt(prefs, candidates, max_items=max_items)

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful restaurant recommendation assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=temperature,
        )

        # The exact response structure is defined by the Groq SDK; here we
        # assume an OpenAI-compatible `choices[0].message.content` format.
        return response.choices[0].message.content  # type: ignore[no-any-return]


__all__ = [
    "GroqLLMClient",
]

