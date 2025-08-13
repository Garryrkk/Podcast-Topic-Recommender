# topic_recommender.py
import pandas as pd
import random

def generate_ideas(input_file="topic_trends.csv", output_file="ideas.md", ideas_per_topic=15):
    df = pd.read_csv(input_file, names=["topic", "count"], skiprows=1)  # skip header from .to_csv()

    title_templates = [
        "Let's Talk About {} (What No One Tells You)",
        "The Truth About {}",
        "Why {} Affects Gen Z So Much",
        "How to Deal with {} in 2025",
        "Is {} Ruining Our Mental Health?",
        "{} Explained in 5 Minutes",
        "My Story with {}",
        "Why We Need to Talk About {} Now",
        "What {} Taught Me About Life",
        "The Dark Side of {}"
    ]

    ideas = []

    for _, row in df.iterrows():
        topic = row["topic"]
        for _ in range(ideas_per_topic):
            template = random.choice(title_templates)
            ideas.append(template.format(topic))

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🎙 Content Ideas Based on Trending Topics\n\n")
        for idea in ideas:
            f.write(f"- {idea}\n")

    print(f"✅ {len(ideas)} ideas saved to {output_file}")

if __name__ == "__main__":
    generate_ideas()
