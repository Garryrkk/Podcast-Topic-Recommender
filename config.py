import os

# Base directory = project root (where config.py is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Possible CSV locations
possible_paths = [
    os.path.join(BASE_DIR, "data", "topic_trends.csv"),
    os.path.join(BASE_DIR, "youtube", "topic_trends.csv"),
    os.path.join(BASE_DIR, "topic_trends.csv"),
]

CSV_PATH = None
for path in possible_paths:
    if os.path.exists(path):
        CSV_PATH = path
        break

if CSV_PATH is None:
    raise FileNotFoundError(
        "Could not find topic_trends.csv in data/, youtube/, or root folder.\n"
        "Please place the CSV in one of those folders."
    )

# Path to ideas.md
IDEAS_PATH = os.path.join(BASE_DIR, "ideas.md")

# Output file path
OUTPUT_PATH = os.path.join(BASE_DIR, "podcast_topic_titles.md")
