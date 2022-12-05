import os

import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denik.db'
db = SQLAlchemy(app)


# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
class Denik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    jazyk = db.Column(db.String(200), nullable=False)
    popis = db.Column(db.String(200), nullable=False)
    hodnoceni = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Denik %r>' % self.id
@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')

@app.route('/add/', methods=['POST', 'GET'])
def addZaznam():  
    #pokud nekdo prida neco do databaze, tak se spusti tato cast, jinak se zobrazi stranka
    record_name = request.form['name']
    record_time = request.form['time_spent']
    record_popis = request.form['popis']
    record_jazyk = request.form['jazyk']
    record_hodnoceni = request.form['hodnoceni']
    new_record = Denik(name=record_name,jazyk=record_jazyk ,popis=record_popis,hodnoceni=record_hodnoceni,time_spent=record_time)
    db.session.add(new_record)
    db.session.commit()
    return redirect('/zaznamy/')
@app.route('/form/')
def showForm():
    return render_template('addZaznam.html')

def print_db():
  return(cur.fetchall())


@app.route('/zaznamy/')
def zaznamy():
    records = Denik.query.order_by(Denik.name).all()

    return render_template('zaznamy.html', records=records)

if __name__ == '__main__':
    app.run(debug=true)
