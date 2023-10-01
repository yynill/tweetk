from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # active = loog if this msg is active


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    access_token = db.Column(db.String(255))
    access_token_secret = db.Column(db.String(255))
    message = db.relationship('Message')

   # twitter_tag = db.Column(db.String(500), unique=True, default=None)
   # twitter_name = db.Column(db.String(500), unique=True, default=None)
   # twitter_pic = db.Column(db.String(150), unique=True, default=None)

   # twitter_bio = db.Column(db.String(1000), unique=True, default=None)
   # twitter_follower_count = db.Column(db.String(1000), unique=True, default=None)
   # twitter_joined date = db.Column(db.String(1000), unique=True, default=None)
