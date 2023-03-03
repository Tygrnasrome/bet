from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from .models import Denik,Tags,User,Kategorie,Jazyk, Palettes
from flask import Blueprint
from flask_login import login_required, current_user
from .config import UI,Palette, user_config_auth, backup_config_auth, obj_config_auth, Filter, cat_config_auth, backup_dict
from . import db
import csv
import os
from datetime import datetime
from werkzeug.utils import secure_filename

back = Blueprint('back', __name__)
def backupListUpKeep():
    filename = "app/static/backups/backup.csv"
    with open(os.path.abspath(filename), 'r') as f:
        csv_reader = csv.reader(f)
        header = True

        tmp_dict = {}
        for backup in backup_dict:
            tmp_dict[backup] = 0 # creating tmp dictionary so size wont change while erasing objects in next for loop
        for backup in tmp_dict:
            del backup_dict[backup] # erase existing dict

        for row in csv_reader:
            value_id = int(0)
            value_dict = {}
            if not header: # skips first call (header)
                for value in row: #every value in row
                    value_dict[value_id] = value #save value in dict so we can recall on it later    
                    value_id += int(1)
                backup_dict[value_dict[0]] = 1 # adds one backup in dict (time is value 0)
            header = False

def newBackup(name):
    backupListUpKeep()
    backup_dict[name] = 1
    filename = "app/static/backups/backup.csv"
    with open(os.path.abspath(filename), 'w') as f:
        out = csv.writer(f)
        out.writerow(['name'])
        for backup in backup_dict:
            out.writerow([backup])

def delBackup(name):
    backupListUpKeep()
    del backup_dict[name]
    filename = "app/static/backups/backup.csv"
    with open(os.path.abspath(filename), 'w') as f:
        out = csv.writer(f)
        out.writerow(['name'])
        for backup in backup_dict:
            out.writerow([backup])
        flash('Záloha byla smazána','message')

def exportCsv(name):
    filename = "app/static/backups/{name}.csv"
    backupListUpKeep()
    with open(os.path.abspath(filename.format(name = name)), 'w') as f:
        out = csv.writer(f)
        # records
        out.writerow(['obj_type','id', 'name', 'jazyk_id', 'popis', 'hodnoceni', 'date', 'time_spent'])
        for record in Denik.query.order_by(Denik.id).all():
            out.writerow(['record',record.id, record.name, record.jazyk_id, record.popis, record.hodnoceni, record.date, record.time_spent])
        # users
        out.writerow(['obj_type','id', 'name', 'email', 'password', 'auth', 'created_date'])
        for user in User.query.order_by(User.id).all():
            out.writerow(['user',user.id, user.name, user.email, user.password, user.auth, user.created_date])
        # languages
        out.writerow(['obj_type','id', 'name'])
        for language in Jazyk.query.order_by(Jazyk.id).all():
            out.writerow(['language',language.id, language.name])
        # tags
        out.writerow(['obj_type','id', 'name', 'barva', 'popis'])
        for tag in Tags.query.order_by(Tags.id).all():
            out.writerow(['tag',tag.id, tag.name, tag.barva, tag.popis])
        # cats
        out.writerow(['obj_type','id', 'owned_id', 'type_id'])
        for cat in Kategorie.query.order_by(Kategorie.id).all():
            out.writerow(['cat',cat.id, cat.owned_id, cat.type_id])
        # palettes
        out.writerow(['obj_type','id', 'user_id', 'base', 'selected', 'hover', 'text', 'header', 'body', 'divone', 'divtwo', 'divthree','in_use'])
        for palette in Palettes.query.order_by(Palettes.id).all():
            out.writerow(['palette',palette.id, palette.user_id, palette.base, palette.selected, palette.hover, palette.text, palette.header, palette.body, palette.divone, palette.divtwo, palette.divthree, palette.in_use])
    newBackup(name)
    flash('Záloha byla vytvořena','message')

def importCsv(name):
    filename = "app/static/backups/{name}.csv"
    backupListUpKeep()
    with open(os.path.abspath(filename.format(name = name)), 'r') as f:
        csv_reader = csv.reader(f)
        db.drop_all() # drops all tables (clean isn't it)
        db.create_all() # creates the tables which are non existant 
        for row in csv_reader: #every row
            value_id = int(0)
            value_dict = {}
            for value in row: #every value in row
                value_dict[value_id] = value #save value in dict so we can recall on it later
                value_id += int(1)
            # every obj_type constructs
            if value_dict[0] == 'record':
                db.session.add(Denik(id=value_dict[1],name=value_dict[2],jazyk_id=value_dict[3] ,popis=value_dict[4],hodnoceni=value_dict[5],date=value_dict[6], time_spent=value_dict[7]))
                db.session.commit()
            if value_dict[0] == 'user':
                db.session.add(User(id=value_dict[1],name=value_dict[2],email=value_dict[3] ,password=value_dict[4],auth=value_dict[5],created_date=value_dict[6]))
                db.session.commit()
            if value_dict[0] == 'language':
                db.session.add(Jazyk(id=value_dict[1],name=value_dict[2]))
                db.session.commit()
            if value_dict[0] == 'tag':
                db.session.add(Tags(id=value_dict[1],name=value_dict[2],barva=value_dict[3] ,popis=value_dict[4]))
                db.session.commit()
            if value_dict[0] == 'cat':
                db.session.add(Kategorie(id=value_dict[1],owned_id=value_dict[2],type_id=value_dict[3]))
                db.session.commit()
            if value_dict[0] == 'palette':
                db.session.add(Palettes(id=value_dict[1],user_id=value_dict[2],base=value_dict[3] ,selected=value_dict[4],hover=value_dict[5],text=value_dict[6], header=value_dict[7], body=value_dict[8], divone=value_dict[9], divtwo=value_dict[10], divthree=value_dict[11], in_use=value_dict[12]))
                db.session.commit()
    # declaration necessities (init functions)
    languages = Jazyk.query.order_by(Jazyk.id).all()
    for language in languages:
        Filter.language_dict[int(language.id)] = "on"

    tags = Tags.query.order_by(Tags.id).all()
    for tag in tags:
        Filter.tag_dict[int(tag.id)] = "on"
    Filter.tag_dict[0] = "on"
    try: # reset palette 
        if current_user.name:
                palettes = Palettes.query.order_by(Palettes.id).all()
        used = False
        for palette in palettes:
            if palette.user_id == current_user.id and palette.in_use == 'on':
                Palette.base = palette.base
                Palette.hover = palette.hover
                Palette.selected = palette.selected
                Palette.divone = palette.divone
                Palette.divthree = palette.divthree
                Palette.divtwo = palette.divtwo
                Palette.body = palette.body
                Palette.header = palette.header
                Palette.text = palette.text
                used = True
        if not used:
            Palette.base = Palette.def_base
            Palette.hover = Palette.def_hover
            Palette.selected = Palette.def_selected
            Palette.divone = Palette.def_divone
            Palette.divthree = Palette.def_divthree
            Palette.divtwo = Palette.def_divtwo
            Palette.body = Palette.def_body
            Palette.header = Palette.def_header
            Palette.text = Palette.def_text
    except:
        pass
    flash('Záloha byla nahrána','message')
            
@back.route('/backup/use/<string:name>', methods=['POST', 'GET'])
@login_required
def backupUse(name):
    if current_user.auth == backup_config_auth:
        UI.active = "backup"
        importCsv(name)
        
        return redirect('/backup/')
    flash("Na tuto akci nemáte oprávnění","error")
    return redirect('/')

@back.route('/backup/', methods=['POST', 'GET'])
@login_required
def backup():
    if current_user.auth == backup_config_auth:
        UI.active = "backup"
        if request.method == 'GET':
            backupListUpKeep()
            return render_template('backup/downloadBackUp.html', user = current_user,active=UI.active,palette=Palette, backup_dict=backup_dict)
        else:
            name = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
            exportCsv(name)
            request.method = 'GET'
            return redirect('/backup/')
    flash("Na tuto akci nemáte oprávnění","error")
    return redirect('/')

@back.route('/backup/download/<string:name>')
@login_required
def downloadFile(name):
    if not current_user.auth <= backup_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    path = "app/static/backups/{name}.csv"
    return send_file(os.path.abspath(path.format(name = name)), as_attachment=True)

@back.route('/backup/delete/<string:name>')
@login_required
def deleteFile(name):
    if not current_user.auth <= backup_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    name = name.replace(' ','')
    path = "app/static/backups/{name}.csv"
    path = path.format(name=name)
    os.remove(path)
    delBackup(name)
    return redirect('/backup/')

@back.route('/upload/', methods = ['POST'])
@login_required
def upload_file():
    f = request.files['file']
    f.save(os.path.join('app/static/backups/',secure_filename(f.filename)))
    newBackup(secure_filename(f.filename).replace('.csv','').replace(' ',''))
    flash('Soubor importován','message')
    return redirect('/backup/')