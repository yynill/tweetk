from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Response_message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    twitter_tag = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    response_message = db.relationship('Response_message')
