import tweepy
from tweepy import OAuthHandler

consumer_key = 'BGM0wTogXmt1yCleGIgbMRFbS'
consumer_secret = 'NP0CgXxQo4xz5BdFiH76v7a6dBQNlTTlszsE2SOTJl44Ijekcb'
access_token = '292434485-KOEeAtHI8Mao57fYJpJp3S5NQf9niiDGK1nfGe59'
access_secret = 'hm2mmd539zjT1mGC5BqQgpbygK0nqSBxh6CE0ImozzHZl'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# get total tweets of a user
# Example
# screen name : Zeyan_hahi
# name: Liuzeyan
# id: 292434485
# print(api.me())

# Search a person total tweets by his id
print(api.lookup_users(user_ids=['292434485']))
