import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from .models import Programator,Denik,Tags,User,Kategorie,Jazyk
from flask import Blueprint
from flask_login import login_required, current_user
from .config import UI,Palette
from . import db

data = Blueprint('data', __name__)

@data.route('/add/', methods=['POST', 'GET'])
def addZaznam():

    tags = Tags.query.order_by(Tags.id).all()

    #pokud nekdo prida neco do databaze, tak se spusti tato cast, a pak se přeseměruje na view /zaznamy/
    record_name = str(request.form['name'])
    record_time = int(request.form['time_spent'])
    record_popis = str((request.form['popis']))
    record_jazyk = int(request.form['jazyk_id'])
    record_hodnoceni = int(request.form['hodnoceni'])
    record_date = str(request.form['date'])



    new_record = Denik(name=record_name,jazyk_id=record_jazyk ,popis=record_popis,hodnoceni=record_hodnoceni,time_spent=record_time, date=record_date)
    db.session.add(new_record)
    db.session.commit()
    for tag in tags:
        try:
            request.form[str(tag.id)]
            new_cat = Kategorie(type_id=tag.id, owned_id=new_record.id)
            db.session.add(new_cat)
            db.session.commit()
        except:
            pass

    return redirect('/zaznamy/1')
@data.route('/form/')
def showForm():
    programmers = Programator.query.order_by(Programator.id).all()
    languages = Jazyk.query.order_by(Jazyk.id).all()

    tags = Tags.query.order_by(Tags.id).all()
    UI.active = "addRecord"
    return render_template('addZaznam.html',active=UI.active,palette=Palette, languages=languages, programmers=programmers, tags=tags)

@data.route('/language/form/', methods=['POST', 'GET'])
def showLanguageForm():
    UI.active = "addLanguage"
    if request.method == 'GET':
        languages = Jazyk.query.order_by(Jazyk.id).all()
        return render_template('addJazyk.html',active=UI.active,languages=languages,palette=Palette)
    else:
        language_name = request.form['name']
        new_language = Jazyk(name=language_name)
        db.session.add(new_language)
        db.session.commit()
        languages = Jazyk.query.order_by(Jazyk.id).all()
        request.method = "GET"
        for language in languages:
            Filter.language_dict[language.id] = "on"
        return render_template('addJazyk.html',active=UI.active,languages=languages,palette=Palette)

@data.route('/language/update/<int:id>', methods=['POST', 'GET'])
def showLanguageUpdateForm(id):
    languages = Jazyk.query.order_by(Jazyk.id).all()
    UI.active = "addJazyk"
    if request.method == 'GET':
        language_to_update = Jazyk.query.get_or_404(id)
        return render_template('updateJazyk.html',active=UI.active,languages=languages, language_to_update=language_to_update,palette=Palette)
    else:
        language_to_update = Jazyk.query.get_or_404(id)
        language_to_update.name = request.form['name']
        db.session.commit()
        for language in languages:
            Filter.language_dict[language.id] = "on"
        return redirect('/language/form/')

@data.route('/language/delete/<int:id>')
def delLanguage(id):
    language_to_del = Jazyk.query.get_or_404(id)
    db.session.delete(language_to_del)
    db.session.commit()
    return redirect('/language/form/')

@data.route('/programmer/form/', methods=['POST', 'GET'])
def showProgrammerForm():
    UI.active = "addProgrammer"
    if request.method == 'GET':
        programmers = Programator.query.order_by(Programator.id).all()
        return render_template('addProgramator.html',active=UI.active,programmers=programmers,palette=Palette)
    else:
        programmer_name = request.form['name']
        new_programmer = Programator(name=programmer_name)
        db.session.add(new_programmer)
        db.session.commit()
        programmers = Programator.query.order_by(Programator.id).all()
        request.method = "GET"
        return render_template('addProgramator.html',active=UI.active,programmers=programmers,palette=Palette)

@data.route('/programmer/update/<int:id>', methods=['POST', 'GET'])
def showProgrammerUpdateForm(id):
    UI.active = "addProgrammer"
    programmers = Programator.query.order_by(Programator.id).all()
    if request.method == 'GET':
        for programmer in programmers:
            if(id == programmer.id):
                return render_template('updateProgramator.html',active=UI.active,programmers=programmers, programmer_to_update=programmer,palette=Palette)
    else:
        for programmer in programmers:
            if(id == programmer.id):
                programmer.name = request.form['name']
        db.session.commit()
        programmers = Programator.query.order_by(Programator.id).all()
        request.method = "GET"
        return render_template('addProgramator.html',active=UI.active,programmers=programmers,palette=Palette)

@data.route('/programmer/delete/<int:id>')
def delProgrammer(id):
    programmer_to_del = Programator.query.get_or_404(id)
    records = Denik.query.order_by(Denik.id).all()
    for record in records:
        if(record.name == programmer_to_del.id):
            db.session.delete(record)
            db.session.commit()
    db.session.delete(programmer_to_del)
    db.session.commit()
    return redirect('/programmer/form/')

@data.route('/cat/form/', methods=['POST', 'GET'])
def showCatForm():
    UI.active = "addCat"
    if request.method == 'GET':
        tags = Tags.query.order_by(Tags.id).all()
        return render_template('addKategorie.html',active=UI.active, tags=tags,palette=Palette)
    else:
        tag_name = request.form['name']
        tag_barva = request.form['barva']
        tag_popis = request.form['popis']

        new_tag = Tags(name=tag_name, barva=tag_barva, popis=tag_popis)
        db.session.add(new_tag)
        db.session.commit()
        tags = Tags.query.order_by(Tags.id).all()
        request.method = "GET"
        tags = Tags.query.order_by(Tags.id).all()
        Filter.tag_dict[0] = "on"
        for tag in tags:
            Filter.tag_dict[tag.id] = "on"
        return render_template('addKategorie.html',active=UI.active, tags=tags,palette=Palette)

@data.route('/cat/delete/<int:id>')
def delCat(id):
    cats = Kategorie.query.order_by(Kategorie.id).all()
    tag_to_del = Tags.query.get_or_404(id)
    for cat in cats:
        if (cat.type_id == tag_to_del.id):
            cat_to_del = Kategorie.query.get_or_404(cat.id)
            db.session.delete(cat_to_del)
            db.session.commit()

    db.session.delete(tag_to_del)
    db.session.commit()
    return redirect('/cat/form/')

@data.route('/cat/update/<int:id>', methods=['POST', 'GET'])
def updateCatForm(id):
    tags = Tags.query.order_by(Tags.id).all()
    UI.active = "addCat"
    if request.method == 'GET':
        for tag in tags:
            if(id == tag.id):
                return render_template('updateKategorie.html',active=UI.active, tags=tags, tag_to_update=tag,palette=Palette)
    else:
        tag_to_update = Tags.query.get_or_404(id)
        tag_to_update.name = request.form['name']
        tag_to_update.barva = request.form['barva']
        tag_to_update.popis = request.form['popis']

        db.session.commit()
        return redirect('/cat/form/')
@data.route('/update-form/<int:id>')
def updateRecord(id):
    record_to_update = Denik.query.get_or_404(id)
    languages = Jazyk.query.order_by(Jazyk.id).all()
    cats = Kategorie.query.order_by(Kategorie.id).all()
    tags = Tags.query.order_by(Tags.id).all()
    programmers = Programator.query.order_by(Programator.id).all()
    UI.active = "addRecord"
    return render_template('update.html',active=UI.active, record=record_to_update,languages=languages, tags=tags, cats=cats, programmers=programmers,palette=Palette)

@data.route('/delete/<int:id>')
def deleteRecord(id):
    record_to_del = Denik.query.get_or_404(id)

    cats = Kategorie.query.order_by(Kategorie.id).all()
    for cat in cats:
        if (cat.owned_id == record_to_del.id):
            cat_to_del = Kategorie.query.get_or_404(cat.id)
            db.session.delete(cat_to_del)
            db.session.commit()
    db.session.delete(record_to_del)
    db.session.commit()
    return redirect('/zaznamy/1')

@data.route('/update-add/<int:id>', methods=['POST', 'GET'])
def updateAddZaznam(id):
    record_to_update = Denik.query.get_or_404(id)
    record_to_update.name = request.form['name']
    record_to_update.time_spent = request.form['time_spent']
    record_to_update.popis = request.form['popis']
    record_to_update.jazyk_id = request.form['jazyk_id']
    record_to_update.hodnoceni = request.form['hodnoceni']
    record_to_update.date = request.form['date']

    cats = Kategorie.query.order_by(Kategorie.id).all()
    for cat in cats:
        if (cat.owned_id == record_to_update.id):
            cat_to_del = Kategorie.query.get_or_404(cat.id)
            db.session.delete(cat_to_del)
            db.session.commit()

    tags = Tags.query.order_by(Tags.id).all()
    for tag in tags:
        try:
            request.form[str(tag.id)]
            new_cat = Kategorie(type_id=tag.id, owned_id=record_to_update.id)
            db.session.add(new_cat)
            db.session.commit()
        except:
            pass


    db.session.commit()
    return redirect('/zaznamy/1')