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

    # Add additional fields for user information
    user_id = db.Column(db.BigInteger)
    user_profile_picture_url = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    user_twitter_tag = db.Column(db.String(255))
    user_description = db.Column(db.String(255))
    user_join_date = db.Column(db.DateTime)
    user_followers_count = db.Column(db.Integer)
