import os
import time

import tweepy


API_KEY = os.environ['TWITTER_API_KEY']
API_SECRET = os.environ['TWITTER_API_SECRET']

ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

search_results = api.search(q='#bgnow')

for result in search_results:
    if not result.user.following:
        print 'Following %s...' % result.user.screen_name
        result.user.follow()
        time.sleep(3)
