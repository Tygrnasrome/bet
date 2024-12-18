from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)
    auth = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.String(30), default=datetime.utcnow().strftime("%m-%d-%Y"))

class Palettes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    base = db.Column(db.String(20), nullable=False)
    selected = db.Column(db.String(20), nullable=False)
    hover = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(20), nullable=False)
    header = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(20), nullable=False)
    divone = db.Column(db.String(20), nullable=False)
    divtwo = db.Column(db.String(20), nullable=False)
    divthree = db.Column(db.String(20), nullable=False)
    in_use = db.Column(db.String(5), default='on')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_one_id = db.Column(db.Integer, db.ForeignKey(Team.id))
    team_two_id = db.Column(db.Integer, db.ForeignKey(Team.id))
    course_one = db.Column(db.Integer, nullable=False)
    course_two = db.Column(db.Integer, nullable=False)
