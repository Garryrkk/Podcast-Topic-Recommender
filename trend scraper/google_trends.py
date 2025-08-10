from pytrends.request import TrendReq

def get_trending_keywords(niche="mental health"):
    pytrends = TrendReq()
    pytrends.build_payload([niche], cat=0, timeframe='now 7-d', geo='', gprop='')
    return pytrends.related_queries()[niche]['rising']
