from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, default=False)

    def activate(self):
        Message.query.filter_by(user_id=self.user_id).update({"active": False})
        self.active = True
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255))
    access_token_secret = db.Column(db.String(255))

    message = db.relationship('Message')

    user_id = db.Column(db.BigInteger)
    user_profile_picture_url = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    user_twitter_tag = db.Column(db.String(255))
    user_description = db.Column(db.String(1000))
    user_join_date = db.Column(db.DateTime)
    user_followers_count = db.Column(db.Integer)


class MessagedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    already_messaged_user = db.Column(
        db.String(255), unique=True, nullable=False)
