from db import session
from models import to_follow,followed
import config,tweepy,random,time
from datetime import datetime
import requests

#Twitter Credentials:
#Username: 
#id:id=

def getClient():
    client = tweepy.Client(
        consumer_key = config.consumer_key,
        consumer_secret= config.consumer_secret,
        access_token= config.access_token,
        access_token_secret= config.access_token_secret
        )
    return client

def liketweets(client):
    hashtags = ['#gamblingtwitter','#freepicks','#gambling']
    choice = random.choice(hashtags)
    tweets = client.search_recent_tweets(query=choice, max_results=11,user_auth=True).data

    try:
        for tweet in tweets:
            client.like(tweet_id = tweet.id)
            print(f'Liked {tweet.id}')

    except tweepy.TweepyException as e:
        
        print(e)


#does user exist in database/ do i follow user?
def do_i_follow(client,check_id):

    user = client.get_user(id=config.my_id,user_auth=True,user_fields=['public_metrics']).data
    follower_count = user['public_metrics']['following_count']

    try:
        for t_user in tweepy.Paginator(client.get_users_following,id=config.my_id, max_results = 1000, user_auth=True).flatten(limit=follower_count):
            if str(t_user.id) == str(check_id):
                return True
        return False

    except tweepy.TweepyException as e:
        #text from twilio this error and time
        print(e)


#Not allowed to run will get banned
def unfollow_users(client):
    users = session.query(followed).order_by('date').limit(10).all()
    try:
        for user in users:
            print(f'{user.username} unfollowing')
            client.unfollow(user.id)
            session.delete(user)
            session.commit()
            print(f'User {user.username} deleted from database ')

    except tweepy.TweepyException as e:
        #text from twilio this error and time
        print(e)

#will get banned running. Maybe timed seconds between? definitley less than 10 accounts
def follow_users(client):
    following_id = random.choice(session.query(to_follow).all()).id
    users = client.get_users_followers(id = following_id, max_results=1000,user_auth=True).data
    users = random.sample(users,10)
    for user in users:
        if not do_i_follow(client,user.id) and not(session.query(followed).filter_by(id = user.id).first()):
            try:
                client.follow(target_user_id=user.id,user_auth=True)
            except tweepy.TweepyException as e:
                #text from twilio this error and time
                print(e)

            new_follow = followed()
            new_follow.id = user.id
            new_follow.username = user.username
            new_follow.date = datetime.today()
            print(f'Followed and added to db {new_follow.username}')
            session.add(new_follow)
            session.commit()
        else:
            print(f'Already follow {user.username}')
    
    session.close()


#client = getClient()
#follow_users(client)
#liketweets(client)
#unfollow_users(client)