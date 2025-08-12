from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()

# Define an endpoint to fetch Reddit threads
@app.get("/reddit_threads")
def get_reddit_threads():
    # Path to JSON file (relative to this file's directory)
    json_path = Path(__file__).parent / "Podcast-Topic-Recommender" / "reddit_scraper" / "reddit_threads.json"
    
    if not json_path.exists():
        return {"error": f"File not found: {json_path}"}
    
    with open(json_path, "r", encoding="utf-8") as f:
        reddit_data = json.load(f)
    
    return reddit_data
