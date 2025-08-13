import pandas as pd
import re
import random
import os

# ----------------------------------------
# 🔹 Auto-detect paths based on current script
# ----------------------------------------
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))  # youtube folder
CSV_PATH = os.path.join(PROJECT_FOLDER, "topic_trends.csv")  # trending topics CSV
IDEAS_PATH = os.path.join(PROJECT_FOLDER, "ideas.md")       # ideas file in same folder
OUTPUT_PATH = os.path.join(PROJECT_FOLDER, "podcast_topic_titles.md")  # output in same folder

# ----------------------------------------
# Create output folder if needed (optional)
# ----------------------------------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# ----------------------------------------
# 1️⃣ Load trending topics (excluding "other")
# ----------------------------------------
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"❌ CSV not found at {CSV_PATH}")

topic_trends = pd.read_csv(CSV_PATH)
top_topics = topic_trends[topic_trends['topics'] != "other"].head(5)['topics'].tolist()

print("🔥 Top 5 Topics Selected:")
for t in top_topics:
    print("-", t)

# ----------------------------------------
# 2️⃣ Read ideas.md and filter based on top topics
# ----------------------------------------
if not os.path.exists(IDEAS_PATH):
    raise FileNotFoundError(f"❌ ideas.md not found at {IDEAS_PATH}")

with open(IDEAS_PATH, "r", encoding="utf-8") as f:
    ideas = f.readlines()

filtered_ideas_tuples = []
for idea in ideas:
    for topic in top_topics:
        if topic.lower() in idea.lower():
            filtered_ideas_tuples.append((topic, idea.strip()))
            break

print(f"✅ {len(filtered_ideas_tuples)} filtered ideas found")

# ----------------------------------------
# 3️⃣ Catchy Title Generator
# ----------------------------------------
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
        return [t.format(topic=topic) for t in random.sample(self.hook_templates, n)]

title_generator = CatchyTitleGenerator()

# ----------------------------------------
# 4️⃣ Hashtags per topic
# ----------------------------------------
hashtags_map = {
    "Mental Health - Trauma": "#TraumaRecovery #HealingJourney #MentalHealthAwareness",
    "Mental Health - Stress": "#StressRelief #CalmMind #MentalHealth",
    "Mental Health - Anxiety": "#AnxietyRelief #CalmMind #Mindfulness",
    "Work & Study Life": "#Productivity #StudyTips #WorkLifeBalance",
    "Mental Health - Therapy": "#TherapyTalk #HealingJourney #SelfCare"
}

# ----------------------------------------
# 5️⃣ Combine ideas + catchy titles + hashtags
# ----------------------------------------
final_posts = []
for topic, text in filtered_ideas_tuples:
    catchy_titles = title_generator.generate_titles(text, n=3)
    hashtags = hashtags_map.get(topic, "#PodcastIdeas #Trending #GenZ")
    
    final_posts.append({
        "topic": topic,
        "original_idea": text,
        "catchy_titles": catchy_titles,
        "hashtags": hashtags
    })

# ----------------------------------------
# 6️⃣ Save everything to one file
# ----------------------------------------
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for post in final_posts:
        f.write(f"## {post['topic']}\n")
        f.write(f"Original Idea: {post['original_idea']}\n")
        f.write("Catchy Titles:\n")
        for title in post['catchy_titles']:
            f.write(f"- {title}\n")
        f.write(f"Hashtags: {post['hashtags']}\n\n")

print(f"✅ Saved {len(final_posts)} topic packs with catchy titles to {OUTPUT_PATH}")
