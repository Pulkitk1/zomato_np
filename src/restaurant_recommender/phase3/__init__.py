"""
Phase 3: Groq LLM integration.

This subpackage focuses on:
- Building prompts that combine user preferences and candidate restaurants.
- Calling the Groq LLM API to obtain natural-language recommendations.

Tests that actually hit the Groq API should only be added once a valid
GROQ_API_KEY is configured in the environment or `.env` file.
"""

from .client import GroqLLMClient
from .prompt_builder import build_recommendation_prompt

__all__ = [
    "GroqLLMClient",
    "build_recommendation_prompt",
]

