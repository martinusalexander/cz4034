#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials

consumer_key = "BGM0wTogXmt1yCleGIgbMRFbS"
consumer_secret = "NP0CgXxQo4xz5BdFiH76v7a6dBQNlTTlszsE2SOTJl44Ijekcb"
access_key = "292434485-KOEeAtHI8Mao57fYJpJp3S5NQf9niiDGK1nfGe59"
access_secret = "hm2mmd539zjT1mGC5BqQgpbygK0nqSBxh6CE0ImozzHZl"
"""
consumer_key = 'PSX3TZVXzB0DBEwsVOAvkSzQ2'
consumer_secret = 'GRlMa4ICbDDm0ChmXuM6KSADs7g0jQPufoODb2gYanI0hkM4cE'
access_key = '166141524-9VeZNOXRmTSSwHhGXqfyZOoStTzOdrp0b8FRp8d0'
access_secret = 'bmGAkF2JsitdYIF17Mqqe8qYxqU1IupyUCe8bRflgsX9A'
"""

def get_all_tweets(search_keyword):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True)

	#initialize a list to hold all the tweepy Tweets
	all_tweets = []

	new_tweets = tweepy.Cursor(api.search,
					  q=search_keyword,
					  count=10,
					  result_type="recent",
					  include_entities=True,
					  lang="en").items()

	# Save tweets if it is not in the list
	for tweet in new_tweets:
		if tweet not in all_tweets:
			all_tweets.append(tweet)

	final_tweet_data = []
	for tweet in all_tweets:
		tweet_data = {'id': tweet.id,
					  'name': tweet.user.name,
					  'screen_name': tweet.user.screen_name,
					  'status': tweet.text,
					  'location': tweet.user.location,
					  'source': tweet.source,
					  'created_at': tweet.created_at}
		print(tweet_data)
		final_tweet_data.append(tweet_data)

	return final_tweet_data
