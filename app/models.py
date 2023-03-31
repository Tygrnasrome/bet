from . import db
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    created_date = db.Column(db.String(30), default=datetime.utcnow().strftime("%m-%d-%Y"))
    color = db.Column(db.String(30), nullable=False)

class User(db.Model):
    userID = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    nick = db.Column(db.String(30), nullable=False)
    lines_added = db.Column(db.Integer, default=0)
    lines_removed = db.Column(db.Integer, default=0)
    changes = db.Column(db.Integer, default=0)

class Commit(db.Model):
    commit_id = db.Column(db.String(40), primary_key=True)
    creator_id = db.Column(db.String(40), nullable=True)
    date = db.Column(db.String(30), nullable=False)
    lines_added = db.Column(db.Integer, nullable=False)
    lines_removed = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=True)

