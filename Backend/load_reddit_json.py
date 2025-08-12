import json
from pathlib import Path

# Path to your JSON file
json_path =  "Podcast-Topic-Recommender/reddit_scraper/reddit_threads.json"

# Load JSON data
with open(json_path, "r", encoding="utf-8") as f:
    reddit_data = json.load(f)

# Print to verify
print(reddit_data)
