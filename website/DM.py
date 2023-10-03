import tweepy
from .models import User, Message, MessagedUser
from flask_login import current_user
from . import db


def start_twitter_listener():
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

    # make sure participant is only dm once
    already_messaged_users_list = set(
        user.user_id for user in MessagedUser.query.all())

    class MyStreamListener(tweepy.StreamListener):
        def on_event(self, event):
            # checks if chat is opened
            if event['event']['type'] == 'participant_join':
                participant_id = event['event']['user_id']
                if participant_id not in already_messaged_users_list:
                    send_initial_message(participant_id)

                    new_messaged_users = MessagedUser(
                        already_messaged_user=participant_id)
                    db.session.add(new_messaged_users)
                    db.session.commit()
                    print(' ')
                    print('CHAT OPENED')

    def send_initial_message(participant_id):
        # Here send an initial message to the user with user_id using the Twitter API.
        user = User.query.get(current_user.id)
        active_message = Message.query.filter_by(
            user_id=user.id, active=True).first()

        api.send_direct_message(participant_id, active_message)

    # Instantiate the stream listener and start listening for events
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # Start listening for user events
    myStream.userstream()

    # user is lokked in with tweetk
    # participant is a 3rd - messaging the user
