import tweepy
from tweepy import OAuthHandler





consumer_key ='OpnME1SdurksDoeo9BTGOSqTn'
consumer_secret ='8Wr5hn3g0h2lCdk940MOyLcTm7Ddd1O8r53DqqThl86RM1Pe5c'
access_token ='3999249914-gH0ppqbLTj2crSTdaKt7u3tN3rEwLl57WCpJO2y'
access_secret='eDgqcV4ELmRBgzCihF4aAUGqtROmdXbuXhteWJcyEQeTw'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def tweethub():
	status = []
	urls = []
	for tweets in tweepy.Cursor(api.home_timeline, include_entities=True).items(10):		
		for url in tweets.entities['urls']:
			status.append(tweets.text.split('https')[0].encode('utf-8'))
			urls.append(url['display_url'].encode('utf-8'))
	return dict(zip(status,urls))