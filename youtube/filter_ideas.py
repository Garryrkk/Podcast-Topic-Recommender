import pandas as pd
import re

# Load trending topics (excluding "other")
topic_trends = pd.read_csv("topic_trends.csv")
top_topics = topic_trends[topic_trends['topics'] != "other"].head(5)['topics'].tolist()

print("🔥 Top 5 Topics Selected:")
for t in top_topics:
    print("-", t)

# Read ideas.md
with open("ideas.md", "r", encoding="utf-8") as f:
    ideas = f.readlines()

filtered_ideas = []
for idea in ideas:
    if any(topic in idea for topic in top_topics):
        filtered_ideas.append(idea.strip())

# Function to make social-ready title + hashtags
def make_social_post(idea):
    base_title = re.sub(r"\[.*?\]", "", idea).strip()  # remove brackets
    hashtags = ["#PodcastIdeas", "#ContentCreation", "#MentalHealth", "#Trending", "#GenZ"]
    return f"{base_title}\n{' '.join(hashtags)}\n"

# Create social-ready list
social_posts = [make_social_post(idea) for idea in filtered_ideas]

# Save to top_ideas.md
with open("top_ideas.md", "w", encoding="utf-8") as f:
    for post in social_posts:
        f.write(post + "\n")

print(f"✅ {len(social_posts)} filtered & social-ready ideas saved to top_ideas.md")

def make_catchy(title):
    # Remove extra spaces
    title = re.sub(r'\s+', ' ', title).strip()
    # Shorten to 60 chars max without cutting words
    if len(title) > 60:
        cut = title[:57].rsplit(' ', 1)[0]
        title = cut + "..."
    # Add a power word if missing
    power_words = ["Secrets", "Hacks", "Tips", "Guide", "Boost", "Proven", "Quick", "Easy"]
    if not any(word.lower() in title.lower() for word in power_words):
        title += " | Quick Tips"
    # Capitalize each word
    title = title.title()
    return title

# Hashtags per topic
hashtags_map = {
    "Mental Health - Trauma": "#TraumaRecovery #HealingJourney #MentalHealthAwareness",
    "Mental Health - Stress": "#StressRelief #CalmMind #MentalHealth",
    "Mental Health - Anxiety": "#AnxietyRelief #CalmMind #Mindfulness",
    "Work & Study Life": "#Productivity #StudyTips #WorkLifeBalance",
    "Mental Health - Therapy": "#TherapyTalk #HealingJourney #SelfCare"
}

filtered_ideas_tuples = []
for idea in ideas:
    match = re.match(r"\[(.*?)\]\s*(.*)", idea)
    if match:
        topic = match.group(1).strip()
        text = match.group(2).strip()
        if topic in top_topics:
            filtered_ideas_tuples.append((topic, text))

filtered_ideas = filtered_ideas_tuples


# Save
with open("top_ideas.md", "w", encoding="utf-8") as f:
    f.write("\n".join(filtered_ideas_tuples))

print(f"✅ {len(filtered_ideas_tuples)} social-optimized ideas saved to top_ideas.md")


from title_generator import CatchyTitleGenerator

generator = CatchyTitleGenerator()

with open("filter_ideas.py", "r") as f:
    topics = [line.strip() for line in f if line.strip()]

with open("title_generator.py", "w") as f:
    for topic in topics:
        titles = generator.generate_titles(topic, n=5)
        f.write(f"## {topic}\n")
        for title in titles:
            f.write(f"- {title}\n")
        f.write("\n")
