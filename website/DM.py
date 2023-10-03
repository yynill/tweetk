import tweepy
from .models import User, Message
from flask_login import current_user

current_user = User.query.get(current_user.id)

# Initialise API
consumer_key = "AbGCD0cnJviDRWHD2Eo5tl938"
consumer_secret = "kpo8bf1CqH9O5gGuUzqzO95Qg4xr7Jn5j9p4WIFvjEhmVPyZIJ"

access_token = current_user.access_token
access_token_secret = current_user.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Listen to DMs
already_messaged_users = set()  # make sure participant is only dm once


class MyStreamListener(tweepy.StreamListener):
    # listens to events from Stream
    def on_event(self, event):
        # checks if chat is opened
        if event['event']['type'] == 'participant_join':
            participant_id = event['event']['user_id']
            if participant_id not in already_messaged_users:
                send_initial_message(participant_id)
                already_messaged_users.add(participant_id)


def send_initial_message(user_id):
    # Here send an initial message to the user with user_id using the Twitter API.
    user = User.query.get(user_id)
    active_message = Message.query.filter_by(
        user_id=user.id, active=True).first()

    initial_message = active_message

    api.send_direct_message(user_id=user_id, text=initial_message)


# Instantiate the stream listener and start listening for events
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Start listening for user events
myStream.userstream()
