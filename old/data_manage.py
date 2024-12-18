from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from .models import User, Palettes
from flask import Blueprint
from flask_login import login_required, current_user
from .config import UI,Palette, user_config_auth, backup_config_auth, obj_config_auth, cat_config_auth, backup_dict
from . import db
import csv
import os
from datetime import datetime
from werkzeug.utils import secure_filename

data = Blueprint('data', __name__)

@data.route('/add/', methods=['POST', 'GET'])
@login_required
def addZaznam():
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
    flash('Záznam vytvořen','message')
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
@login_required
def showForm():
    users = User.query.order_by(User.id).all()
    languages = Jazyk.query.order_by(Jazyk.id).all()

    tags = Tags.query.order_by(Tags.id).all()
    UI.active = "addRecord"
    return render_template('record/addZaznam.html', user = current_user,active=UI.active,palette=Palette, languages=languages, users=users, tags=tags)

@data.route('/language/form/', methods=['POST', 'GET'])
@login_required
def showLanguageForm():
    if not current_user.auth <= obj_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "addLanguage"
    if request.method == 'GET':
        languages = Jazyk.query.order_by(Jazyk.id).all()
        return render_template('language/addJazyk.html', user = current_user,active=UI.active,languages=languages,palette=Palette)
    else:
        language_name = request.form['name']
        new_language = Jazyk(name=language_name)
        db.session.add(new_language)
        db.session.commit()
        flash('Programovací jazyk vytvořen','message')
        languages = Jazyk.query.order_by(Jazyk.id).all()
        request.method = "GET"
        for language in languages:
            Filter.language_dict[language.id] = "on"
        return render_template('language/addJazyk.html', user = current_user,active=UI.active,languages=languages,palette=Palette)

@data.route('/language/update/<int:id>', methods=['POST', 'GET'])
@login_required
def showLanguageUpdateForm(id):
    if not current_user.auth <= obj_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    languages = Jazyk.query.order_by(Jazyk.id).all()
    UI.active = "addJazyk"
    if request.method == 'GET':
        language_to_update = Jazyk.query.get_or_404(id)
        return render_template('language/updateJazyk.html', user = current_user,active=UI.active,languages=languages, language_to_update=language_to_update,palette=Palette)
    else:
        language_to_update = Jazyk.query.get_or_404(id)
        language_to_update.name = request.form['name']
        db.session.commit()
        flash('Programovací jazyk změněn','message')
        for language in languages:
            Filter.language_dict[language.id] = "on"
        return redirect('/language/form/')

@data.route('/language/delete/<int:id>')
@login_required
def delLanguage(id):
    if not current_user.auth <= obj_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    language_to_del = Jazyk.query.get_or_404(id)
    db.session.delete(language_to_del)
    db.session.commit()
    flash('Programovací jazyk smazán','message')
    return redirect('/language/form/')
"""
@data.route('/user/form/', methods=['POST', 'GET'])
@login_required
def showUserForm():
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "signup"
    if request.method == 'GET':
        users = User.query.order_by(User.id).all()
        return render_template('signup.html', user = current_user,active=UI.active,users=users,palette=Palette)
    else:
        user_name = request.form['name']
        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()
        flash('User přidán','message')
        users = User.query.order_by(User.id).all()
        request.method = "GET"
        return render_template('signup.html', user = current_user,active=UI.active,users=users,palette=Palette)

@data.route('/user/update/<int:id>', methods=['POST', 'GET'])
@login_required
def showUserUpdateForm(id):
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "signup"
    users = User.query.order_by(User.id).all()
    if request.method == 'GET':
        for usr in users:
            if(id == usr.id):
                return render_template('updateUser.html', user = current_user,active=UI.active,users=users, user_to_update=user,palette=Palette)
    else:
        for usr in users:
            if(id == usr.id):
                usr.name = request.form['name']
        db.session.commit()
        users = User.query.order_by(User.id).all()
        request.method = "GET"
        return render_template('signup.html', user = current_user,active=UI.active,users=users,palette=Palette)
"""
@data.route('/user/delete/<int:id>')
@login_required
def delUser(id):
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
     
    user_to_del = User.query.get_or_404(id)
    if user_to_del.auth > 1:
        records = Denik.query.order_by(Denik.id).all()
        for record in records:
            if(record.name == user_to_del.id):
                db.session.delete(record)
                db.session.commit()
        db.session.delete(user_to_del)
        db.session.commit()
        flash('Uživatel a jeho záznamy smazány','message')
    else:
        flash('Uživatel nemůže být smazán, kvůli vysokému oprávnění','error')
    return redirect('/user/')

@data.route('/cat/form/', methods=['POST', 'GET'])
@login_required
def showCatForm():
    if not current_user.auth <= cat_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "addCat"
    if request.method == 'GET':
        tags = Tags.query.order_by(Tags.id).all()
        return render_template('cat/addKategorie.html', user = current_user,active=UI.active, tags=tags,palette=Palette)
    else:
        tag_name = request.form['name']
        tag_barva = request.form['barva']
        tag_popis = request.form['popis']

        new_tag = Tags(name=tag_name, barva=tag_barva, popis=tag_popis)
        db.session.add(new_tag)
        db.session.commit()
        flash('Štítek vytvořen','message')
        tags = Tags.query.order_by(Tags.id).all()
        request.method = "GET"
        tags = Tags.query.order_by(Tags.id).all()
        Filter.tag_dict[0] = "on"
        for tag in tags:
            Filter.tag_dict[tag.id] = "on"
        return render_template('cat/addKategorie.html', user = current_user,active=UI.active, tags=tags,palette=Palette)

@data.route('/cat/delete/<int:id>')
@login_required
def delCat(id):
    if not current_user.auth <= cat_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    cats = Kategorie.query.order_by(Kategorie.id).all()
    tag_to_del = Tags.query.get_or_404(id)
    for cat in cats:
        if (cat.type_id == tag_to_del.id):
            cat_to_del = Kategorie.query.get_or_404(cat.id)
            db.session.delete(cat_to_del)
            db.session.commit()
    flash('Štítek smazán včetně zmínek v záznamech','message')
    db.session.delete(tag_to_del)
    db.session.commit()
    return redirect('/cat/form/')

@data.route('/cat/update/<int:id>', methods=['POST', 'GET'])
@login_required
def updateCatForm(id):
    if not current_user.auth <= cat_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    tags = Tags.query.order_by(Tags.id).all()
    UI.active = "addCat"
    if request.method == 'GET':
        for tag in tags:
            if(id == tag.id):
                return render_template('cat/updateKategorie.html', user = current_user,active=UI.active, tags=tags, tag_to_update=tag,palette=Palette)
    else:
        tag_to_update = Tags.query.get_or_404(id)
        tag_to_update.name = request.form['name']
        tag_to_update.barva = request.form['barva']
        tag_to_update.popis = request.form['popis']

        db.session.commit()
        flash('Štítek změněn','message')
        return redirect('/cat/form/')
@data.route('/update-form/<int:id>')
@login_required
def updateRecord(id):
    if not current_user.auth <= obj_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    record_to_update = Denik.query.get_or_404(id)
    languages = Jazyk.query.order_by(Jazyk.id).all()
    cats = Kategorie.query.order_by(Kategorie.id).all()
    tags = Tags.query.order_by(Tags.id).all()
    users = User.query.order_by(User.id).all()
    UI.active = "addRecord"
    return render_template('record/update.html', user = current_user,active=UI.active, record=record_to_update,languages=languages, tags=tags, cats=cats, users=users,palette=Palette)

@data.route('/delete/<int:id>')
@login_required
def deleteRecord(id):
    if not current_user.auth <= obj_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    record_to_del = Denik.query.get_or_404(id)

    cats = Kategorie.query.order_by(Kategorie.id).all()
    for cat in cats:
        if (cat.owned_id == record_to_del.id):
            cat_to_del = Kategorie.query.get_or_404(cat.id)
            db.session.delete(cat_to_del)
            db.session.commit()
    db.session.delete(record_to_del)
    db.session.commit()
    flash('Záznam smazán','message')
    return redirect('/zaznamy/1')

@data.route('/update-add/<int:id>', methods=['POST', 'GET'])
@login_required
def updateAddZaznam(id):
    if not current_user.auth <= obj_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
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

    flash('Záznam změněn','message')
    db.session.commit()
    return redirect('/zaznamy/1')