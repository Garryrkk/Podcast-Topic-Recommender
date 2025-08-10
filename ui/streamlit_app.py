import streamlit as st
from trend_scraper.reddit_scraper import get_reddit_posts
from trend_scraper.twitter_scraper import get_tweets
from trend_scraper.google_trends import get_trending_keywords
from nlp.topic_cluster import get_clusters
from generator.hook_generator import generate_hook

st.title("🎙️ Gen Z Podcast Topic Recommender")

niche = st.text_input("Enter your niche (e.g., 'mental health', 'eating disorders')")

if st.button("Get Topics"):
    reddit_posts = get_reddit_posts()
    tweets = get_tweets(niche)
    trends = get_trending_keywords(niche)

    all_texts = reddit_posts + tweets + [t['query'] for t in trends if 'query' in t]
    clusters = get_clusters(all_texts)

    for label, topics in clusters.items():
        if topics:
            st.subheader(f"🔥 Topic Cluster {label + 1}")
            topic_sample = topics[0]
            hook = generate_hook(topic_sample)
            st.markdown(f"**Suggested Topic:** {topic_sample}")
            st.markdown(f"**Hook/Title Suggestion:** {hook}")
