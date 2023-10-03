import tweepy
from .models import User
from flask_login import current_user

current_user = User.query.get(current_user.id)

consumer_key = "AbGCD0cnJviDRWHD2Eo5tl938"
consumer_secret = "kpo8bf1CqH9O5gGuUzqzO95Qg4xr7Jn5j9p4WIFvjEhmVPyZIJ"

access_token = current_user.access_token
access_token_secret = current_user.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# listen for dms


class MyStreamListener(tweepy.StreamListener):
    def on_event(self, event):
        if event['event']['type'] == 'message_create':
            sender_id = event['event']['user_id']
            message_text = event['event']['message_create']['message_data']['text']
            print(f"New DM from user ID {sender_id}: {message_text}")


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Start listening for user events
myStream.userstream()
