import csv
import random

def get_top_topics(csv_path):
    topics = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            raw_topics = row['topics']  # correct column name
            for t in raw_topics.split(','):
                t = t.strip()
                if t and t not in topics:
                    topics.append(t)
    return topics[:5]  # top 5 unique topics

def generate_titles(topic):
    templates = [
        "Why Everyone’s Talking About {}",
        "Is This the End of {}?",
        "Why {} Might Be Your Biggest Mistake",
        "The Dark Side of {}",
        "Is {} Secretly Ruining Your Life?",
        "The Truth About {}",
        "{}: What No One is Talking About",
        "The Shocking Reality of {}",
        "3 Things You Didn’t Know About {}"
    ]
    return [template.format(topic) for template in random.sample(templates, 5)]

if __name__ == "__main__":
    csv_path = "trending_topics.csv"  # your CSV
    top_topics = get_top_topics(csv_path)
    
    for topic in top_topics:
        print(f"\nTopic: {topic}")
        for title in generate_titles(topic):
            print(f"- {title}")
