import sys
import os

# Add the project root to the system path to allow imports of our local modules
# This is necessary when the serverless function is triggered from a subdirectory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from restaurant_recommender.phase4.api import app

# Vercel's serverless functions expect the app to be exported
# FastAPI's 'app' is the entry point
