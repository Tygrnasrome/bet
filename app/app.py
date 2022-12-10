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

class Programator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    def __repr__(self):
        return '<Programator %r>' % self.id

class Kategorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    type = db.Column(db.String(100), nullable=False) 
    def __repr__(self):
        return '<Kategorie %r>' % self.id
        
@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')

@app.route('/add/', methods=['POST', 'GET'])
def addZaznam():  
    #pokud nekdo prida neco do databaze, tak se spusti tato cast, a pak se přeseměruje na view /zaznamy/
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

@app.route('/language/form/', methods=['POST', 'GET'])
def showLanguageForm():
    if request.method == 'GET':
        languages = Jazyk.query.order_by(Jazyk.id).all()
        return render_template('addJazyk.html',languages=languages)
    else:
        language_name = request.form['name']
        new_language = Jazyk(name=language_name)
        db.session.add(new_language)
        db.session.commit()
        languages = Jazyk.query.order_by(Jazyk.id).all()
        request.method = "GET"
        return render_template('addJazyk.html',languages=languages)

@app.route('/language/delete/<int:id>')
def delLanguage(id):
    language_to_del = Jazyk.query.get_or_404(id)
    db.session.delete(language_to_del)
    db.session.commit()
    return redirect('/language/form/') 
    
@app.route('/programmer/form/', methods=['POST', 'GET'])
def showProgrammerForm():
    if request.method == 'GET':
        programmers = Programator.query.order_by(Programator.id).all()
        return render_template('addProgramator.html',programmers=programmers)
    else:
        programmer_name = request.form['name']
        new_programmer = Programator(name=programmer_name)
        db.session.add(new_programmer)
        db.session.commit()
        programmers = Programator.query.order_by(Programator.id).all()
        request.method = "GET"
        return render_template('addProgramator.html',programmers=programmers)

@app.route('/programmer/delete/<int:id>')
def delProgrammer(id):
    programmer_to_del = Programator.query.get_or_404(id)
    db.session.delete(programmer_to_del)
    db.session.commit()
    return redirect('/programmer/form/') 

@app.route('/cat/form/', methods=['POST', 'GET'])
def showCatForm():
    if request.method == 'GET':
        cats = Kategorie.query.order_by(Kategorie.id).all()
        return render_template('addKategorie.html',cats=cats)
    else:
        cat_name = request.form['name']
        cat_type = request.form['type']
        new_cat = Kategorie(name=cat_name, type=cat_type)
        db.session.add(new_cat)
        db.session.commit()
        cats = Kategorie.query.order_by(Kategorie.id).all()
        request.method = "GET"
        return render_template('addKategorie.html',cats=cats)

@app.route('/cat/delete/<int:id>')
def delCat(id):
    cat_to_del = Kategorie.query.get_or_404(id)
    db.session.delete(cat_to_del)
    db.session.commit()
    return redirect('/cat/form/') 

def print_db():
  return(cur.fetchall())


@app.route('/zaznamy/')
def zaznamy():
    records = Denik.query.order_by(Denik.date).all()
    languages = Jazyk.query.order_by(Jazyk.id).all()
    cats = Kategorie.query.order_by(Kategorie.id).all()
    return render_template('zaznamy.html', records=records,languages=languages, cats=cats)

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
