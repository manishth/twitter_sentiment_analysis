import re
import tweepy
from textblob import TextBlob


class TwitterAnalysis(object):

	def __init__(self):

		# Twitter app token and keys
		consumer_key 		= "xxxx"
		consumer_secret 	= "xxxx"
		access_token 		= "xxxx"
		access_token_secret = "xxxx"

		try:
			self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			print("Error authenticating app.")

			