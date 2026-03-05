import sys
import os

# Add the src directory to the system path to allow imports of our local modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from restaurant_recommender.phase4.api import app

# Vercel's serverless functions expect the app to be exported
# FastAPI's 'app' is the entry point
