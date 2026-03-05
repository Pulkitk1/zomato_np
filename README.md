# AI Restaurant Recommendation Service

This project implements an AI-powered restaurant recommendation service using:

- The Zomato dataset from Hugging Face: `ManikaSaini/zomato-restaurant-recommendation`
- A Groq-hosted LLM for natural-language recommendations.
- A modern FastAPI-based UI for easy interaction.

## Features

- **Personalized Recommendations**: Get suggestions based on place, cuisine, rating, and budget.
- **AI-Powered Insights**: LLM-generated summaries describing why a restaurant is a good match.
- **Modern UI**: Dark mode interface with a Zomato-themed design.

## Setup

### Requirements

- Python 3.10 or later.
- Groq API Key (Place in a `.env` file as `GROQ_API_KEY`).

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   Create a `.env` file with your Groq API key:
   ```env
   GROQ_API_KEY=your_key_here
   ```

## Running the Application

### Launch the UI & API

Run the following command from the project root:

```bash
# On Windows (PowerShell)
$env:PYTHONPATH="src"; python -m uvicorn restaurant_recommender.phase4.api:app --reload

# On Linux/macOS
PYTHONPATH=src python -m uvicorn restaurant_recommender.phase4.api:app --reload
```

Once running, navigate to:
- UI: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Running Tests

To verify the core logic:

```bash
pytest
```

## Architecture

For the full architecture and implementation plan, see [ARCHITECTURE.md](file:///d:/cursor/np_zomato/zomato_np/ARCHITECTURE.md).

