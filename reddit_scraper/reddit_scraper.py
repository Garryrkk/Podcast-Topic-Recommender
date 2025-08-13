import json
import csv
import os
from datetime import datetime
import praw  # Reddit API wrapper (pip install praw)
import pandas as pd

# --------------------------
# 🔹 Reddit API credentials
# --------------------------
REDDIT_CLIENT_ID = "DLCXyT-e2gU2BjsUbV9-PA"
REDDIT_CLIENT_SECRET = "hY5DsXL_zgr7qHEnbGwUOKk8cvcDPw"
REDDIT_USER_AGENT = "genzi_topic_recommender_bot_v1 by /u/Careless_Nebula_4368"

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# --------------------------
# 🔹 Paths
# --------------------------
CSV_PATH = os.path.join(os.path.dirname(__file__), "reddit_posts.csv")
JSON_PATH = os.path.join(os.path.dirname(__file__), "combined_data.json")

# --------------------------
# 🔹 Subreddits
# --------------------------
subreddits = ["mentalhealth", "selfcare", "depression", "Anxiety", "trauma", "lonely"]

# --------------------------
# 🔹 Map subreddit -> topic
# --------------------------
subreddit_to_topic = {
    "mentalhealth": "Mental Health",
    "selfcare": "Self Care",
    "depression": "Mental Health - Depression",
    "Anxiety": "Mental Health - Anxiety",
    "trauma": "Mental Health - Trauma",
    "lonely": "Mental Health - Loneliness"
}

# --------------------------
# 🔹 Functions
# --------------------------
def fetch_posts(limit=50):
    all_posts = []
    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub)
            for submission in subreddit.hot(limit=limit):
                all_posts.append({
                    "title": submission.title,
                    "text": submission.selftext,
                    "url": submission.url,
                    "subreddit": sub,
                    "topic": subreddit_to_topic.get(sub, "Other")
                })
        except Exception as e:
            print(f"❌ Failed to fetch from r/{sub}: {e}")
    return all_posts


def save_posts_to_csv(posts, path=CSV_PATH):
    if not posts:
        print("⚠️ No posts to save.")
        return

    keys = posts[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(posts)
    print(f"✅ Saved {len(posts)} Reddit posts to {path}")


def save_posts_to_json(posts, path=JSON_PATH):
    if not posts:
        print("⚠️ No posts to save.")
        return

    with open(path, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(posts)} Reddit posts to {path}")


# --------------------------
# 🔹 Main
# --------------------------
if __name__ == "__main__":
    print(f"⏱ Fetching Reddit posts at {datetime.now()}")
    posts = fetch_posts(limit=100)

    save_posts_to_csv(posts)
    save_posts_to_json(posts)
    print("🔥 Reddit scraping completed successfully!")
