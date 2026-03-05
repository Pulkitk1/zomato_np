# AI Restaurant Recommendation Service — Architecture

## 1. Overview

**Purpose**: An AI-powered service that takes user preferences (price, place, rating, cuisine), uses a Groq-hosted LLM, and returns clear, actionable restaurant recommendations.

**Data source**: [Hugging Face — ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) (~51.7k rows, ~574 MB).

**LLM**: Groq (low-latency inference).

---

## 2. High-Level Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   UI / Web Page │────▶│  Recommendation  │────▶│  Groq LLM API   │
│ (preferences)   │     │     Service      │     │  (reasoning)    │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │                       ▼
         │              ┌──────────────────┐
         └─────────────▶│  Restaurant Data │
         (recommendations) (Hugging Face)  │
                        └──────────────────┘
```

**Flow**: User enters preferences in UI → Service filters/ranks data → LLM receives context → LLM returns recommendations → UI displays results.

---

## 3. Data Model (Hugging Face Dataset)

Relevant fields from `ManikaSaini/zomato-restaurant-recommendation`:

| Field | Type | Maps to User Preference |
|-------|------|-------------------------|
| `name` | string | — |
| `address` | string | — |
| `location` | string | **place** |
| `rate` | string | **rating** |
| `approx_cost(for two people)` | string | **price** |
| `cuisines` | string | **cuisine** |
| `rest_type` | string | Optional filter |
| `online_order` | string | Optional |
| `book_table` | string | Optional |
| `votes` | int64 | Optional ranking |
| `url`, `phone`, `dish_liked`, `reviews_list`, `menu_item`, `listed_in(type)` | — | Enrichment / display |

---

## 4. User Preferences Contract

| Preference | Description | Example |
|------------|-------------|--------|
| **price** | Budget (e.g. low / medium / high or numeric band) | "under 500 for two" |
| **place** | Location / area | "Koramangala", "Bangalore" |
| **rating** | Minimum or target rating | "4+", "above 4.5" |
| **cuisine** | Cuisine type(s) | "North Indian", "Italian" |

Optional: rest_type, online_order, book_table.

---

## 5. System Components

| Component | Responsibility |
|-----------|----------------|
| **Data layer** | Load/cache dataset from Hugging Face; expose filtered subsets (by place, rating, price, cuisine). |
| **Preference parser** | Normalize and validate user inputs (price bands, location, rating thresholds, cuisine list). |
| **Retrieval / filter** | Apply filters on dataset; optionally rank by votes/rating; return top-N candidates. |
| **Prompt builder** | Build LLM prompt with user preferences + candidate restaurants (names, details). |
| **LLM client (Groq)** | Call Groq API with prompt; handle rate limits, errors, timeouts. |
| **Response formatter** | Parse LLM output; structure recommendations (list + short rationale). |
| **API / app entry** | Expose HTTP or CLI interface; accept preferences, return recommendations. |
| **UI / frontend** | Web page for entering preferences (price, place, rating, cuisine) and displaying recommendations. |

---

## 6. Phased Implementation Plan

### Phase 1 — Data & Environment

- **1.1** Project setup: repo structure, Python env, `requirements.txt` (e.g. `datasets`, `groq`, `python-dotenv`).
- **1.2** Hugging Face integration: load `ManikaSaini/zomato-restaurant-recommendation`; define schema mapping and column selection.
- **1.3** Data exploration & validation: nulls, value ranges for `rate`, `approx_cost`, `location`, `cuisines`; document edge cases.
- **1.4** Caching strategy: optional local cache (Parquet/CSV) to avoid re-downloading on every run.

**Deliverable**: Loaded, validated dataset and a clear data contract (columns used for filtering and for LLM context).

---

### Phase 2 — Filtering & Retrieval

- **2.1** Preference model: define structures for price/place/rating/cuisine (e.g. Pydantic models or dataclasses).
- **2.2** Preference parsing: map free text or structured input (e.g. "4+ rating", "under 600") into normalized filters.
- **2.3** Filter engine: filter dataset by location, rating band, price band, cuisines (substring or tag match).
- **2.4** Ranking: optional sort by `votes`, `rate`, or combined score; limit to top-K (e.g. 10–20) for LLM context.

**Deliverable**: Given preferences, return a ranked list of candidate restaurants (no LLM yet).

---

### Phase 3 — Groq LLM Integration

- **3.1** Groq setup: API key (env), client SDK; minimal “hello” call to verify connectivity.
- **3.2** Prompt design: system + user prompt; include user preferences and top-K candidate rows (name, location, rate, cost, cuisines).
- **3.3** LLM invocation: send prompt to Groq; choose model (e.g. Llama or Mixtral); handle token limits (truncate candidate list if needed).
- **3.4** Robustness: retries, timeouts, error handling; optional fallback when LLM is unavailable.

**Deliverable**: End-to-end flow: preferences → filtered candidates → Groq → raw LLM recommendation text.

---

### Phase 4 — Response Shaping & API

- **4.1** Response format: define output shape (e.g. list of recommended restaurants + short explanation); optional structured output (JSON) via prompt or post-processing.
- **4.2** Response formatter: parse LLM output into a stable structure (list of names/links + rationale).
- **4.3** API layer: REST (FastAPI/Flask) or CLI; single endpoint or command: input = preferences, output = recommendations.
- **4.4** Configuration: env for Groq key, Hugging Face cache path, model name, top-K size.

**Deliverable**: Service callable via API or CLI with clear, consistent recommendations.

---

### Phase 5 — UI, Quality & Operations

- **5.1** **UI page**: Single web page (or small SPA) for the recommendation flow:
  - Form inputs: place, price (e.g. dropdown or range), rating (e.g. min rating), cuisine (e.g. multi-select or tags).
  - Submit button to call the recommendation API.
  - Results area: display recommended restaurants (name, location, rating, cost, cuisines) and optional LLM rationale; loading and error states.
- **5.2** UI tech: Static HTML/JS or React/Vue/Svelte; served by the same app (FastAPI static/templates) or separate frontend dev server; ensure CORS if frontend and API are split.
- **5.3** Logging & observability: log requests, latency, LLM token usage, errors.
- **5.4** Evaluation: small set of preference → expected-style recommendations; compare LLM output quality.
- **5.5** Documentation: API spec (OpenAPI), README with setup, example API requests, and how to run the UI.
- **5.6** Deployment: container (Docker), optional cloud deploy; serve UI and API together or behind same origin; secrets for Groq key and any HF token if needed.

**Deliverable**: Production-ready service with a working UI page, docs, and a path to deployment.

---

## 7. Technology Stack (Reference)

| Layer | Choice |
|-------|--------|
| Language | Python 3.10+ |
| Data | `datasets` (Hugging Face), optional `pandas` |
| LLM | Groq API (official SDK or `openai`-compatible client if supported) |
| API | FastAPI (recommended) or Flask |
| **UI / frontend** | Static HTML/CSS/JS or React/Vue/Svelte; served via FastAPI static/templates or separate dev server |
| Config / secrets | Environment variables, `python-dotenv` |
| Caching | Local Parquet/CSV or `datasets` cache |

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Dataset size / load time | Cache after first load; filter in chunks if needed. |
| Groq rate limits | Respect limits; optional queue or backoff. |
| LLM output inconsistency | Clear prompt template; optional JSON mode or regex-based parsing. |
| Stale data | Document dataset update frequency; optional periodic re-download. |

---

## 9. Out of Scope (Architecture Only)

- No implementation in this document.
- No user accounts or persistence of preferences.
- No real-time availability or booking (data is static from the dataset).

---

*Document version: 1.1 — Architecture only; implementation to follow per phases above. Phase 5 includes UI page.*
