# combined/combined.py

import os
import pandas as pd
import random
import logging
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "combined.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_and_print(message, level="info"):
    print(message)
    getattr(logging, level)(message)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

YT_CSV_PATH = os.path.join(PROJECT_ROOT, "youtube", "topic_trends.csv")
YT_IDEAS_PATH = os.path.join(PROJECT_ROOT, "youtube", "ideas.md")
REDDIT_CSV_PATH = os.path.join(PROJECT_ROOT, "reddit_scraper", "reddit_posts.csv")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "combined", "podcast_topic_titles.md")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

def load_csv_safe(path, name):
    if not os.path.exists(path):
        log_and_print(f"❌ {name} CSV not found at {path}", "error")
        return None
    try:
        df = pd.read_csv(path)
        if df.empty:
            log_and_print(f"⚠️ {name} CSV is empty!", "warning")
        return df
    except Exception as e:
        log_and_print(f"❌ Failed to load {name} CSV: {e}", "error")
        return None

class CatchyTitleGenerator:
    def __init__(self):
        self.hook_templates = [
            "The Dark Side of {topic}",
            "Why Everyone’s Talking About {topic}",
            "Is {topic} Secretly Ruining Your Life?",
            "3 Things You Didn’t Know About {topic}",
            "How {topic} is Changing Gen Z Forever",
            "The Truth About {topic}",
            "Why {topic} Might Be Your Biggest Mistake",
            "{topic}: What No One is Talking About",
            "Is This the End of {topic}?",
            "The Shocking Reality of {topic}"
        ]
    def generate_titles(self, topic, n=3):
        return [t.format(topic=topic) for t in random.sample(self.hook_templates, min(n, len(self.hook_templates)))]

hashtags_map = {
    "Mental Health - Trauma": "#TraumaRecovery #HealingJourney #MentalHealthAwareness",
    "Mental Health - Stress": "#StressRelief #CalmMind #MentalHealth",
    "Mental Health - Anxiety": "#AnxietyRelief #CalmMind #Mindfulness",
    "Work & Study Life": "#Productivity #StudyTips #WorkLifeBalance",
    "Mental Health - Therapy": "#TherapyTalk #HealingJourney #SelfCare",
    "Mental Health - Depression": "#DepressionAwareness #HealingJourney",
    "Mental Health - Loneliness": "#Loneliness #MentalHealth #SelfCare",
    "Self Care": "#SelfCare #MentalHealthAwareness #Wellness"
}

def generate_combined_topics():
    log_and_print("🚀 Starting Combined Topic Generator")

    yt_topics_df = load_csv_safe(YT_CSV_PATH, "YouTube")
    if yt_topics_df is None:
        return []

    yt_top_topics = yt_topics_df[yt_topics_df['topics'] != "other"].head(5)['topics'].tolist()

    reddit_df = load_csv_safe(REDDIT_CSV_PATH, "Reddit")
    if reddit_df is None:
        return []

    if 'topic' not in reddit_df.columns:
        subreddit_to_topic = {
            "mentalhealth": "Mental Health",
            "selfcare": "Self Care",
            "depression": "Mental Health - Depression",
            "Anxiety": "Mental Health - Anxiety",
            "trauma": "Mental Health - Trauma",
            "lonely": "Mental Health - Loneliness"
        }
        reddit_df['topic'] = reddit_df['subreddit'].map(subreddit_to_topic)

    reddit_top_topics = reddit_df['topic'].value_counts().head(5).index.tolist()
    combined_top_topics = list(set(yt_top_topics + reddit_top_topics))

    if not os.path.exists(YT_IDEAS_PATH):
        return []

    with open(YT_IDEAS_PATH, "r", encoding="utf-8") as f:
        yt_ideas = f.readlines()

    filtered_ideas = []
    for idea in yt_ideas:
        for topic in combined_top_topics:
            if topic.lower() in idea.lower():
                filtered_ideas.append((topic, idea.strip()))
                break

    for topic in combined_top_topics:
        for _, row in reddit_df.iterrows():
            if topic.lower() in str(row['topic']).lower() or topic.lower() in str(row['text']).lower():
                filtered_ideas.append((topic, row['text']))

    title_generator = CatchyTitleGenerator()
    final_posts = []
    for topic, text in filtered_ideas:
        catchy_titles = title_generator.generate_titles(topic, n=3)
        hashtags = hashtags_map.get(topic, "#PodcastIdeas #Trending #GenZ")
        final_posts.append({
            "topic": topic,
            "original_idea": text,
            "catchy_titles": catchy_titles,
            "hashtags": hashtags
        })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for post in final_posts:
            f.write(f"## {post['topic']}\n")
            f.write(f"Original Idea: {post['original_idea']}\n")
            f.write("Catchy Titles:\n")
            for title in post['catchy_titles']:
                f.write(f"- {title}\n")
            f.write(f"Hashtags: {post['hashtags']}\n\n")

    return final_posts
