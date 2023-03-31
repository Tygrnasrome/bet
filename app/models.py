from . import db
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    created_date = db.Column(db.String(30), default=datetime.utcnow().strftime("%m-%d-%Y"))