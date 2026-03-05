"""
Simple HTML UI for Phase 5.

Provides a single GET `/` route that renders a small form which posts
preferences to the `/recommend` API (Phase 4) and displays results.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>AI Restaurant Recommendation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      :root {
        --bg: #121212;
        --card-bg: #181818;
        --accent: #e23744;
        --accent-soft: rgba(226, 55, 68, 0.18);
        --border: #2a2a2a;
        --text: #f5f5f5;
        --muted: #b3b3b3;
        --error: #ff6b6b;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: radial-gradient(circle at top, #1f1f1f 0, #050505 55%);
        color: var(--text);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.5rem;
      }
      .shell {
        width: 100%;
        max-width: 1040px;
        display: grid;
        grid-template-columns: minmax(0, 1.1fr) minmax(0, 1.4fr);
        gap: 1.5rem;
      }
      @media (max-width: 900px) {
        .shell { grid-template-columns: minmax(0, 1fr); }
      }
      .card {
        background: radial-gradient(circle at top left, #1f1f1f 0, #121212 60%);
        border-radius: 1.1rem;
        border: 1px solid rgba(148, 163, 184, 0.25);
        box-shadow: 0 22px 40px rgba(15, 23, 42, 0.85);
        padding: 1.6rem 1.7rem;
      }
      h1 {
        margin: 0 0 0.5rem;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.2;
      }
      h1 span {
        color: var(--accent);
      }
      p.subtitle {
        margin: 0 0 2rem;
        color: #d1d5db;
        font-size: 1rem;
        line-height: 1.5;
        max-width: 90%;
      }
      form {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.9rem;
      }
      .field { display: flex; flex-direction: column; gap: 0.3rem; }
      .field.full { grid-column: 1 / -1; }
      label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
      }
      input[type="text"], input[type="number"], select {
        border-radius: 0.7rem;
        border: 1px solid var(--border);
        padding: 0.55rem 0.8rem;
        background: #181818;
        color: var(--text);
        font-size: 0.9rem;
        outline: none;
      }
      input::placeholder { color: #6b7280; }
      input:focus, select:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 1px var(--accent-soft);
        background: #101010;
      }
      .hint {
        font-size: 0.78rem;
        color: var(--muted);
      }
      .actions {
        grid-column: 1 / -1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin-top: 0.25rem;
      }
      .btn-primary {
        border-radius: 999px;
        padding: 0.6rem 1.3rem;
        border: none;
        background: linear-gradient(135deg, #e23744, #ff4557);
        color: #ffffff;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
      }
      .btn-primary:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 14px 30px rgba(226, 55, 68, 0.4);
      }
      .btn-primary:disabled { opacity: 0.6; cursor: wait; box-shadow: none; }
      .status { font-size: 0.8rem; color: var(--muted); }
      .status.error { color: var(--error); }
      .results-card {
        border-radius: 1.1rem;
        border: 1px solid rgba(226, 55, 68, 0.5);
        background: radial-gradient(circle at top right, #202020 0, #050505 70%);
        padding: 1.6rem 1.7rem;
        display: flex;
        flex-direction: column;
        gap: 0.9rem;
      }
      .results-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.7rem;
      }
      .results-header h2 {
        margin: 0;
        font-size: 1.2rem;
        letter-spacing: -0.02em;
      }
      .results-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        font-size: 0.9rem;
      }
      .result-item {
        padding: 0.65rem 0.75rem;
        border-radius: 0.75rem;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.25);
      }
      .result-item-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 0.5rem;
        margin-bottom: 0.15rem;
      }
      .result-name { font-weight: 600; }
      .result-meta { font-size: 0.8rem; color: var(--muted); }
      .summary {
        margin-top: 0.4rem;
        padding-top: 0.4rem;
        border-top: 1px dashed rgba(148, 163, 184, 0.4);
        font-size: 0.85rem;
        color: var(--muted);
      }
    </style>
  </head>
  <body>
    <div class="shell">
      <section class="card">
        <h1><span>Zomato</span> Restaurant Recommendation System</h1>
        <p class="subtitle">
          Helping users discover the best restaurants in Bangalore city based on their preferences.
        </p>
        <form id="preferences-form">
          <div class="field full">
            <label for="place">Location</label>
            <select id="place" name="place">
              <option value="">Any location</option>
            </select>
            <div class="hint">Pick a location from the dataset.</div>
          </div>
          <div class="field">
            <label for="min_rating">Minimum rating</label>
            <input id="min_rating" name="min_rating" type="number" step="0.1" min="0" max="5" placeholder="4.0" />
          </div>
          <div class="field">
            <label for="budget">Budget (₹ for two)</label>
            <input id="budget" name="budget" type="number" min="0" step="50" placeholder="800" />
          </div>
          <div class="field">
            <label for="cuisine">Cuisine</label>
            <select id="cuisine" name="cuisine">
              <option value="">Any cuisine</option>
            </select>
          </div>
          <div class="actions">
            <button type="submit" class="btn-primary" id="submit-btn">
              <span>Get recommendations</span>
            </button>
            <div id="status" class="status"></div>
          </div>
        </form>
      </section>

      <section class="results-card">
        <div class="results-header">
          <h2>Recommendations</h2>
          <span id="result-count" class="status">No results yet</span>
        </div>
        <div id="results" class="results-list"></div>
        <div id="summary" class="summary"></div>
      </section>
    </div>

    <script>
      const form = document.getElementById("preferences-form");
      const statusEl = document.getElementById("status");
      const resultsEl = document.getElementById("results");
      const summaryEl = document.getElementById("summary");
      const countEl = document.getElementById("result-count");
      const submitBtn = document.getElementById("submit-btn");
      const placeSelect = document.getElementById("place");
      const cuisineSelect = document.getElementById("cuisine");
      const budgetInput = document.getElementById("budget");

      async function populateOptions() {
        try {
          const [locResp, cuisineResp] = await Promise.all([
            fetch("/meta/locations"),
            fetch("/meta/cuisines"),
          ]);
          
          if (!locResp.ok || !cuisineResp.ok) throw new Error("Metadata fetch failed");

          const locations = await locResp.json();
          const cuisines = await cuisineResp.json();

          if (locations.length === 0) {
            const opt = document.createElement("option");
            opt.textContent = "No locations found (timeout?)";
            opt.disabled = true;
            placeSelect.appendChild(opt);
          } else {
            locations.forEach((loc) => {
              const opt = document.createElement("option");
              opt.value = loc;
              opt.textContent = loc;
              placeSelect.appendChild(opt);
            });
          }

          if (cuisines.length === 0) {
            const opt = document.createElement("option");
            opt.textContent = "No cuisines found (timeout?)";
            opt.disabled = true;
            cuisineSelect.appendChild(opt);
          } else {
            cuisines.forEach((c) => {
              const opt = document.createElement("option");
              opt.value = c;
              opt.textContent = c;
              cuisineSelect.appendChild(opt);
            });
          }
        } catch (err) {
          console.error("Failed to load options", err);
          const errOpt = document.createElement("option");
          errOpt.textContent = "Error loading options";
          errOpt.disabled = true;
          placeSelect.appendChild(errOpt.cloneNode(true));
          cuisineSelect.appendChild(errOpt);
        }
      }

      populateOptions();

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        statusEl.textContent = "Finding restaurants...";
        statusEl.classList.remove("error");
        submitBtn.disabled = true;
        resultsEl.innerHTML = "";
        summaryEl.textContent = "";

        const formData = new FormData(form);

        // Budget validation (numbers only, no negatives).
        let budgetValue = null;
        const rawBudget = formData.get("budget");
        if (rawBudget !== null && String(rawBudget).trim() !== "") {
          const parsed = Number(rawBudget);
          if (Number.isNaN(parsed) || parsed < 0) {
            statusEl.textContent = "Please enter a valid, non-negative budget.";
            statusEl.classList.add("error");
            submitBtn.disabled = false;
            return;
          }
          budgetValue = parsed;
        }

        const payload = {
          place: formData.get("place") || null,
          min_rating: formData.get("min_rating")
            ? Number(formData.get("min_rating"))
            : null,
          price_band: null,
          budget: budgetValue,
          cuisines: formData.get("cuisine")
            ? [String(formData.get("cuisine"))]
            : null,
        };

        try {
          const resp = await fetch("/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });

          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            throw new Error(err.detail || "Request failed");
          }

          const data = await resp.json();
          const items = data.recommendations || [];

          if (!items.length) {
            countEl.textContent = "No matches found";
            statusEl.textContent = "No restaurants matched your filters.";
            return;
          }

          countEl.textContent = `${items.length} recommendation(s)`;
          statusEl.textContent = "Done.";

          resultsEl.innerHTML = "";
          for (const item of items) {
            const div = document.createElement("div");
            div.className = "result-item";
            const loc = item.location ? ` · ${item.location}` : "";
            const rating = item.rating ? `★ ${item.rating}` : "";
            const cost = item.approx_cost_for_two
              ? `₹${item.approx_cost_for_two} for two`
              : "";
            const cuisines = item.cuisines || "";

            div.innerHTML = `
              <div class="result-item-header">
                <div class="result-name">${item.name}</div>
                <div class="result-meta">${rating}</div>
              </div>
              <div class="result-meta">
                ${[loc, cuisines, cost].filter(Boolean).join(" · ")}
              </div>
            `;
            resultsEl.appendChild(div);
          }

          summaryEl.textContent = data.llm_summary || "";
        } catch (err) {
          console.error(err);
          statusEl.textContent = err.message || "Something went wrong.";
          statusEl.classList.add("error");
          countEl.textContent = "Error";
        } finally {
          submitBtn.disabled = false;
        }
      });
    </script>
  </body>
</html>
"""


__all__ = ["router", "index"]

