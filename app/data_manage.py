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

data = Blueprint('data', __name__)
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
                backup_dict[value_dict[0]] = value_dict[1] # adds one backup in dict (time is value 0, name is value 1)
            header = False

def newBackup(name, desc):
    backupListUpKeep()
    backup_dict[name] = desc
    filename = "app/static/backups/backup.csv"
    with open(os.path.abspath(filename), 'w') as f:
        out = csv.writer(f)
        out.writerow(['name','desc'])
        for backup in backup_dict:
            out.writerow([backup,backup_dict[backup]])

def delBackup(name):
    backupListUpKeep()
    del backup_dict[name]
    filename = "app/static/backups/backup.csv"
    with open(os.path.abspath(filename), 'w') as f:
        out = csv.writer(f)
        out.writerow(['name','desc'])
        for backup in backup_dict:
            out.writerow([backup,backup_dict[backup]])
        flash('Záloha byla úspěšně smazána','message')

def exportCsv(name, desc):
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
    newBackup(name,desc)
    flash('Záloha byla úspěšně vytvořena','message')

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
    flash('Záloha byla úspěšně nahrána','message')
            
@data.route('/backup/use/<string:name>', methods=['POST', 'GET'])
@login_required
def backupUse(name):
    if current_user.auth == backup_config_auth:
        UI.active = "backup"
        importCsv(name)
        
        return redirect('/backup/')
    flash("Na tuto akci nemáte oprávnění","error")
    return redirect('/')

@data.route('/backup/', methods=['POST', 'GET'])
@login_required
def backup():
    if current_user.auth == backup_config_auth:
        UI.active = "backup"
        if request.method == 'GET':
            backupListUpKeep()
            return render_template('backup/downloadBackUp.html', user = current_user,active=UI.active,palette=Palette, backup_dict=backup_dict)
        else:
            desc = request.form["desc"]
            name = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
            exportCsv(name,desc)
            request.method = 'GET'
            return redirect('/backup/')
    flash("Na tuto akci nemáte oprávnění","error")
    return redirect('/')

@data.route('/backup/download/<string:name>')
@login_required
def downloadFile(name):
    if not current_user.auth <= backup_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    path = "app/static/backups/{name}.csv"
    flash('Stahování by mělo každou chvíli začít','notice')
    return send_file(os.path.abspath(path.format(name = name)), as_attachment=True)

@data.route('/backup/delete/<string:name>')
@login_required
def deleteFile(name):
    if not current_user.auth <= backup_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    path = "app/static/backups/{name}.csv"
    path = path.format(name=name)
    os.remove(path)
    delBackup(name)
    flash('Záloha byla smazána','message')
    return redirect('/backup/')

@data.route('/upload/', methods = ['POST'])
@login_required
def upload_file():
    f = request.files['file']
    desc = request.form['desc']
    f.save(os.path.join('app/static/backups/',secure_filename(f.filename)))
    
    
    newBackup(f.filename.replace('.csv',''),desc)
    flash('soubor importován úspěšně','meassage')
    return redirect('/backup/')

@data.route('/add/', methods=['POST', 'GET'])
@login_required
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