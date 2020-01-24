# app/models.py
from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(280))
    email = db.Column(db.String(280))
    api_key = db.Column(db.String(280))
    #children = db.relationship("tweets")

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Tweet #{self.id}>"



