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
error_dict = {'name':0, 'jazyk_id':0,'popis':0,'hodnoceni':0,'date':0,'time_spent':0}
    

class Denik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    jazyk_id = db.Column(db.Integer, nullable=False)
    popis = db.Column(db.String(200), nullable=False)
    hodnoceni = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(200), nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)

class Jazyk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    def __repr__(self):
        return '<Jazyk %r>' % self.id
        
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
    record_jazyk = request.form['jazyk_id']
    record_hodnoceni = request.form['hodnoceni']
    record_date = request.form['date']
    
    new_record = Denik(name=record_name,jazyk_id=record_jazyk ,popis=record_popis,hodnoceni=record_hodnoceni,time_spent=record_time, date=record_date)
    db.session.add(new_record)
    db.session.commit()
    return redirect('/zaznamy/')
@app.route('/form/')
def showForm():
    languages = Jazyk.query.order_by(Jazyk.id).all()
    return render_template('addZaznam.html',languages=languages)

def print_db():
  return(cur.fetchall())


@app.route('/zaznamy/')
def zaznamy():
    records = Denik.query.order_by(Denik.date).all()
    languages = Jazyk.query.order_by(Jazyk.id).all()
    return render_template('zaznamy.html', records=records,languages=languages)

@app.route('/update-form/<int:id>')
def updateRecord(id):
    record_to_update = Denik.query.get_or_404(id)
    languages = Jazyk.query.order_by(Jazyk.id).all()
    return render_template('update.html', record=record_to_update,languages=languages)

@app.route('/delete/<int:id>')
def deleteRecord(id):
    record_to_del = Denik.query.get_or_404(id)
    db.session.delete(record_to_del)
    db.session.commit()
    return redirect('/zaznamy/') 

@app.route('/update-add/<int:id>', methods=['POST', 'GET'])
def updateAddZaznam(id):  
    record_to_update = Denik.query.get_or_404(id)
    record_to_update.name = request.form['name']
    record_to_update.time_spent = request.form['time_spent']
    record_to_update.popis = request.form['popis']
    record_to_update.jazyk_id = request.form['jazyk_id']
    record_to_update.hodnoceni = request.form['hodnoceni']
    record_to_update.date = request.form['date']

    db.session.commit()
    return redirect('/zaznamy/')
if __name__ == '__main__':
    app.run(debug=true)
