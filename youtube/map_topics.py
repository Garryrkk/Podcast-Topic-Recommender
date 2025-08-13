import pandas as pd
import json

# Load word frequencies
df = pd.read_csv("word_frequency.csv")

# Load topic mappings
with open("topics_mapping.json", "r") as f:
    topic_map = json.load(f)

# Create a list for matched topics
mapped_data = []

for _, row in df.iterrows():
    word = row["word"].lower().strip()
    freq = row["count"]
    
    # Find topic for the word
    if word in topic_map:
        topic = topic_map[word]
        mapped_data.append({"word": word, "count": freq, "topic": topic})

# Convert to DataFrame
topics_df = pd.DataFrame(mapped_data)

# Aggregate by topic (sum frequencies)
topic_summary = topics_df.groupby("topic")["count"].sum().reset_index()

# Save detailed word-topic mapping
topics_df.to_csv("topics_detailed.csv", index=False)

# Save summary (topic frequency)
topic_summary.to_csv("topics.csv", index=False)

print("✅ Topic mapping complete. Files saved: topics_detailed.csv, topics.csv")
