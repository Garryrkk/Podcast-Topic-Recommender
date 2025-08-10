import praw

def get_reddit_posts(subreddit="mentalhealth"):
    reddit = praw.Reddit(client_id="YOUR_ID", client_secret="YOUR_SECRET", user_agent="podcast-trend-app")
    posts = []
    for post in reddit.subreddit(subreddit).hot(limit=20):
        posts.append(post.title)
    return posts
