# trending_topics.py
import pandas as pd
from pathlib import Path

def generate_trending_topics(input_file="tagged_comments.csv", output_file="topic_trends.csv", top_n=10):
    if not Path(input_file).exists():
        print(f"❌ Error: {input_file} not found.")
        return

    # Load tagged data
    df = pd.read_csv(input_file)

    if "topics" not in df.columns:
        print("❌ Error: 'topics' column not found in the CSV.")
        return

    # Count topics
    topic_counts = df["topics"].value_counts()

    # Display top topics
    print("🔥 Top Topics:")
    print(topic_counts.head(top_n))

    # Save all topic counts
    topic_counts.to_csv(output_file)
    print(f"✅ Topic trends saved to {output_file}")

if __name__ == "__main__":
    generate_trending_topics()
