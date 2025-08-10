import snscrape.modules.twitter as sntwitter

def get_tweets(query="gen z mental health"):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        tweets.append(tweet.content)
        if len(tweets) > 20:
            break
    return tweets
