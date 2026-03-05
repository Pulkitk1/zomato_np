from fastapi.testclient import TestClient

from restaurant_recommender.phase4.api import app


def test_ui_root_serves_html():
    """
    Phase 5: verify that the root (/) route serves the HTML UI.
    """

    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")

    body = resp.text
    assert '<form id="preferences-form"' in body
    # New dropdowns and meta fetch endpoints.
    assert 'id="place"' in body
    assert 'id="cuisine"' in body
    assert "fetch(\"/recommend\"" in body or "fetch('/recommend'" in body
    assert "fetch(\"/meta/locations\"" in body or "fetch('/meta/locations'" in body
    assert "fetch(\"/meta/cuisines\"" in body or "fetch('/meta/cuisines'" in body
    assert "AI Restaurant Recommendation" in body

