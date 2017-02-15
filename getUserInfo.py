import tweepy
from tweepy import OAuthHandler

consumer_key = 'BGM0wTogXmt1yCleGIgbMRFbS'
consumer_secret = 'NP0CgXxQo4xz5BdFiH76v7a6dBQNlTTlszsE2SOTJl44Ijekcb'
access_token = '292434485-KOEeAtHI8Mao57fYJpJp3S5NQf9niiDGK1nfGe59'
access_secret = 'hm2mmd539zjT1mGC5BqQgpbygK0nqSBxh6CE0ImozzHZl'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

print(api.me().statuses_count)

# for friend in tweepy.Cursor(api.statuses_lookup(365293710)).items(1):
#     print(friend)
