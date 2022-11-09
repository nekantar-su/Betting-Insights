import config,tweepy

def getClient():
    client = tweepy.Client(
        consumer_key = config.consumer_key,
        consumer_secret= config.consumer_secret,
        access_token= config.access_token,
        access_token_secret= config.access_token_secret
        )
    return client
