import re
import tweepy
from textblob import TextBlob


class TwitterAnalysis(object):

	def __init__(self):

		# Twitter app token and keys
		consumer_key 		= "xxxx"
		consumer_secret 	= "xxxx"
		access_token 		= "xxxx"
		access_token_secret     = "xxxx"

		try:
			self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			print("Error authenticating app.")

			
	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):

		tweet_analysis = TextBlob(self.clean_tweet(tweet))

		if tweet_analysis.sentiment.polarity > 0:
			return 'positive'
		elif tweet_analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def fetch_tweets(self, query, count=10):

		tweets = []

		try:
			fetched_tweets = self.api.search(q=query, count=count)

			for tweet in fetched_tweets:
				parsed_tweet = {}
				parsed_tweet["text"] = tweet.text
				parsed_tweet["sentiment"] = self.get_tweet_sentiment(parsed_tweet["text"])

				if tweet.retweet_count > 0:
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
			return tweets
		except tweepy.TweepError as e:
			print("Error: " + str(e))


def main():

	twitterApi = TwitterAnalysis()
	get_tweets = twitterApi.fetch_tweets(query="Global Warming", count=200)

	positive_tweets = [tweet for tweet in get_tweets if tweet['sentiment'] == 'positive']
	print("Positive tweets percentage: {} %".format(100*len(positive_tweets)/len(get_tweets)))

	negative_tweets = [tweet for tweet in get_tweets if tweet['sentiment'] == 'negative']
	print("Negative tweets percentage: {} %".format(100*len(negative_tweets)/len(get_tweets)))

	print("Neutral tweets percentage: {} %".format(100*(len(get_tweets) - len(negative_tweets) - len(positive_tweets))/len(get_tweets)))


if __name__ == "__main__":
	main()