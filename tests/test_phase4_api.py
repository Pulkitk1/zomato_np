from fastapi.testclient import TestClient
import pandas as pd

from restaurant_recommender.phase4 import api as api_module
from restaurant_recommender.phase4.api import app, get_groq_client
from restaurant_recommender.phase4.schemas import RecommendationResponse


class _FakeGroqClient:
    def recommend(self, prefs, ranked, max_items: int = 15, temperature: float = 0.3) -> str:  # noqa: D401
        """
        Fake recommend implementation returning deterministic text.
        """

        return "This is a fake LLM summary for testing purposes."


def _override_groq_client() -> _FakeGroqClient:
    return _FakeGroqClient()


def test_recommend_endpoint_returns_structured_response():
    """
    Phase 4: verify that the /recommend endpoint:
    - Accepts a valid JSON body.
    - Returns 200 and a response that matches the RecommendationResponse schema.
    - Does not require a real Groq API key (uses a fake client).
    """

    app.dependency_overrides[get_groq_client] = _override_groq_client

    # Override the data loader used in the API module so the test does not
    # depend on real dataset contents.
    df = pd.DataFrame(
        [
            {
                "name": "Test Bistro",
                "address": "123 Test Street",
                "location": "Bangalore",
                "rate": "4.5",
                "approx_cost(for two people)": "800",
                "cuisines": "north indian, italian",
                "rest_type": "Casual Dining",
                "online_order": "Yes",
                "book_table": "No",
                "votes": 120,
            }
        ]
    )

    def _fake_load_core_dataframe(sample_size: int = 1500, split: str = "train"):
        return df

    api_module.load_core_dataframe = _fake_load_core_dataframe

    client = TestClient(app)

    payload = {
        "place": "Bangalore",
        "min_rating": 3.5,
        "budget": 900,
        "cuisines": ["north indian"],
    }

    resp = client.post("/recommend", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    # Basic shape checks.
    assert "recommendations" in data
    assert "llm_summary" in data
    assert isinstance(data["recommendations"], list)
    assert isinstance(data["llm_summary"], str)
    assert data["llm_summary"].strip()

    # Ensure at least one recommendation is present.
    assert len(data["recommendations"]) > 0

