from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)
    auth = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.String(30), default=datetime.utcnow)
#emergency command: record_date = datetime.strptime(record_date, '%Y-%m-%d')

class Denik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, db.ForeignKey(User.id))
    jazyk_id = db.Column(db.Integer, nullable=False)
    popis = db.Column(db.String(200), nullable=False)
    hodnoceni = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(200), nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)

class Jazyk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    barva = db.Column(db.String(100), nullable=False)
    popis = db.Column(db.String(100), nullable=False)

class Kategorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owned_id = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)

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