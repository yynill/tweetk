import tweepy
import threading
from .models import User, Message, MessagedUser
from flask_login import current_user
from . import db


def start_twitter_listener():
    def listener_thread():
        consumer_key = "AbGCD0cnJviDRWHD2Eo5tl938"
        consumer_secret = "kpo8bf1CqH9O5gGuUzqzO95Qg4xr7Jn5j9p4WIFvjEhmVPyZIJ"

        access_token = current_user.access_token
        access_token_secret = current_user.access_token_secret

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        # Listen to DMs
        already_messaged_users_list = set(
            user.user_id for user in MessagedUser.query.all())

        class MyStreamListener(tweepy.StreamListener):
            def on_event_status(self, event):
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
            user = User.query.get(current_user.id)
            active_message = Message.query.filter_by(
                user_id=user.id, active=True).first()

            api.send_direct_message(participant_id, active_message.message)
            print('DM sent')

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

        try:
            myStream.userstream()
        except Exception as e:
            print(f"Error in Twitter DM listener: {str(e)}")

    listener_thread = threading.Thread(target=listener_thread)
    listener_thread.daemon = True
    listener_thread.start()
