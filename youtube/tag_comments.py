import pandas as pd
import json

# Load comments
df = pd.read_csv("youtube_comments.csv")

# Load mapping
with open("topics_mapping.json", "r", encoding="utf-8") as f:
    topic_map = json.load(f)

# Function to find topics in a comment
def get_topics(comment):
    comment_lower = str(comment).lower()
    found_topics = set()
    for word, topic in topic_map.items():
        if word in comment_lower:
            found_topics.add(topic)
    return ", ".join(found_topics) if found_topics else "other"

# Apply mapping
df["topics"] = df["comment"].apply(get_topics)

# Save tagged comments
df.to_csv("tagged_comments.csv", index=False)
print("✅ Tagged comments saved to tagged_comments.csv")
