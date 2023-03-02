import sqlite3
import json
from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from .models import Denik,Tags,User,Kategorie,Jazyk, Palettes
from flask import Blueprint
from flask_login import login_required, current_user
from .config import UI,Palette, Filter, obj_config_auth
from werkzeug.security import generate_password_hash
from . import db


main = Blueprint('main', __name__)

def resetPalette():
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

def setAdminAcc():
    admin_acc = User(id=0,name='admin', email='', password=generate_password_hash('1234', method='sha256'), auth=1)
    db.session.add(admin_acc)
    db.session.commit()
    

@main.route('/')
def index():
    db.create_all()
    try:
        admin_acc = User.query.get_or_404(0)
    except:
        setAdminAcc()
    languages = Jazyk.query.order_by(Jazyk.id).all()
    for language in languages:
        Filter.language_dict[int(language.id)] = "on"

    tags = Tags.query.order_by(Tags.id).all()
    for tag in tags:
        Filter.tag_dict[int(tag.id)] = "on"
    Filter.tag_dict[0] = "on"
    UI.active = "home"
    try:
        if current_user.name:
            resetPalette()
    except:
        pass
    return render_template('index.html', user = current_user,active=UI.active,palette=Palette)

@main.route('/settings/', methods=['POST', 'GET'])
@login_required
def settings():
    UI.active = 'settings'
    palettes = Palettes.query.order_by(Palettes.id).all()
    if request.method == 'GET':
        return render_template('settings.html', palette = Palette, active= UI.active, user=current_user)
    else:
        exist = False
        palette_base = request.form['base']
        palette_hover = request.form['hover']
        palette_selected = request.form['selected']
        palette_divone = request.form['divone']
        palette_divthree = request.form['divthree']
        palette_divtwo = request.form['divtwo']
        palette_body = request.form['body']
        palette_header = request.form['header']
        palette_text = request.form['text']
        palette_in_use = 'off'
        palette_in_use = request.form.get('in_use')
        for palette in palettes:
            if palette.user_id == current_user.id:
               palette.base = palette_base
               palette.hover = palette_hover
               palette.selected = palette_selected
               palette.divone = palette_divone
               palette.divthree = palette_divthree
               palette.divtwo = palette_divtwo
               palette.body = palette_body
               palette.header = palette_header
               palette.text = palette_text
               palette.in_use = palette_in_use
               db.session.commit()
               exist = True
        if not exist:
            new_palette = Palettes(base = palette_base,hover=palette_hover, selected=palette_selected, divone=palette_divone,divtwo=palette_divtwo,divthree=palette_divthree,body=palette_body,header=palette_header,text=palette_text, user_id=current_user.id, in_use=palette_in_use)
            db.session.add(new_palette)
            db.session.commit()
        resetPalette()
        return render_template('settings.html', palette = Palette, active= UI.active, user=current_user )

@main.route('/language/')
@login_required
def showLanguageTable():
    languages = Jazyk.query.order_by(Jazyk.id).all()
    UI.active = "language"
    return render_template('language/jazyky.html', user = current_user,active=UI.active,languages=languages,palette=Palette)

@main.route('/user/')
@login_required
def showTableUser():
    if not current_user.auth <= obj_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "user"
    users = User.query.order_by(User.id).all()
    users = User.query.order_by(User.id).all()
    return render_template('user/programatori.html', user = current_user,active=UI.active,users=users,palette=Palette)

@main.route('/cat/')
@login_required
def showCatTable():
    tags = Tags.query.order_by(Tags.id).all()
    UI.active = "cat"
    return render_template('cat/kategorie.html', user = current_user,active=UI.active, tags=tags,palette=Palette)

@main.route('/redirect/my/history/', methods=['GET'])
@login_required
def redirectHistory():
    Filter.name = current_user.id
    return redirect('/zaznamy/1/')
@main.route('/zaznamy/<int:serazeni>/', methods=['POST', 'GET'])
@login_required
def zaznamy(serazeni):
    cats = Kategorie.query.order_by(Kategorie.id).all()
    languages = Jazyk.query.order_by(Jazyk.id).all()
    records = db.session.query(Denik).order_by(Denik.date).all()
    users = User.query.order_by(User.id).all()
    tags = Tags.query.order_by(Tags.id).all()
    if(serazeni == 1):
        #datum od nejdříve
        records = db.session.query(Denik).order_by(Denik.date)
    if(serazeni == 2):
        #datum od nejpozději
        records = db.session.query(Denik).order_by(Denik.date.desc())
    if(serazeni == 3):
        #čas od nejvíce
        records = db.session.query(Denik).order_by(Denik.time_spent.desc())
    if(serazeni == 4):
        #čas od nejméně
        records = db.session.query(Denik).order_by(Denik.time_spent)
    if(serazeni == 5):
        #hodnocení od nejvíce
        records = db.session.query(Denik).order_by(Denik.hodnoceni.desc())
    if(serazeni == 6):
        #hodnocení od nejvíce
        records = db.session.query(Denik).order_by(Denik.hodnoceni)
    if(serazeni == 7):
        #programovací jazyk
        records = db.session.query(Denik).order_by(Denik.jazyk_id)
    if(serazeni == 8):
        #programovací jazyk naopak (nemáme v provozu)
        records = Denik.query.order_by(Denik.jazyk_id).all()

    for r in records:
        #před porovnáváním hodnoty stringů se musí dostat do proměnných nějaká hodnota
        Filter.date_from = r.date
        Filter.date_to = r.date
        Filter.time_from = r.time_spent
        Filter.time_to = r.time_spent
        Filter.hodnoceni_to = r.hodnoceni
        Filter.hodnoceni_from = r.hodnoceni

    for r in records:
        if(str(Filter.date_to) < str(r.date)):
            Filter.date_to = r.date
        if(str(Filter.date_from) > str(r.date)):
            Filter.date_from = r.date
        if(int(Filter.time_to) < int(r.time_spent)):
            Filter.time_to = r.time_spent
        if(int(Filter.time_from) > int(r.time_spent)):
            Filter.time_from = r.time_spent
        if(int(Filter.hodnoceni_from) > int(r.hodnoceni)):
            Filter.hodnoceni_from = r.hodnoceni
        if(int(Filter.hodnoceni_to) < int(r.hodnoceni)):
            Filter.hodnoceni_to = r.hodnoceni


    if request.method == 'POST':
        for language in languages:
            try:
                #try protoze pokud neni oznacen, tak by to melo hodit exception
                Filter.language_dict[int(language.id)] = request.form[str(language.name)]
            except:
                Filter.language_dict[int(language.id)] = 0

        for tag in tags:
            try:
                #try protoze pokud neni oznacen, tak by to melo hodit exception
                Filter.tag_dict[int(tag.id)] = request.form[str(tag.name)]
            except:
                Filter.tag_dict[int(tag.id)] = 0
        try:
            Filter.tag_dict[0] = request.form[str(0)]
        except:
            Filter.tag_dict[0] = int(0)

        Filter.time_from = request.form['time_from']
        Filter.time_to = request.form['time_to']
        Filter.date_from = request.form['date_from']
        Filter.date_to = request.form['date_to']
        Filter.hodnoceni_from = request.form['hodnoceni_from']
        Filter.hodnoceni_to = request.form['hodnoceni_to']
        Filter.hodnoceni_from = request.form['hodnoceni_from']
        Filter.hodnoceni_to = request.form['hodnoceni_to']
        try:
            Filter.name = request.form['name']
        except:
            Filter.name = current_user.id

    #zde se provádí filtrace
    if (int(Filter.name) != int(-1)):
        records = records.filter(Denik.name == Filter.name)
    records = records.filter(Denik.date <= Filter.date_to).filter(Denik.date >= Filter.date_from)
    records = records.filter(Denik.time_spent >= Filter.time_from).filter(Denik.time_spent <= Filter.time_to)
    records = records.filter(Denik.hodnoceni <= Filter.hodnoceni_to).filter(Denik.hodnoceni >= Filter.hodnoceni_from)
    if(not Filter.tag_dict[0]):
        for record in records:
            has = False
            for cat in cats:
                if (int(record.id) == int(cat.owned_id)):
                    has = True
            if (has == False):
                records = records.filter(Denik.id !=  int(record.id))
    for language in languages:
        if(not Filter.language_dict[int(language.id)]):
            records = records.filter(Denik.jazyk_id !=  language.id)
    for tag in tags:
        if(not Filter.tag_dict[int(tag.id)]):
            for record in records:
                has = False
                for cat in cats:
                    if (int(cat.owned_id) == int(record.id) and int(cat.type_id) == int(tag.id)):
                        has = True
                if (has == True):
                    records = records.filter(Denik.id != record.id)
    UI.active = "records"
    return render_template('record/zaznamy.html', user = current_user,active=UI.active, records=records, languages=languages, users=users, tags=tags, cats=cats, \
    filtered_languages=Filter.language_dict, filtered_tags=Filter.tag_dict, min_date=Filter.date_from, max_date=Filter.date_to, min_time=Filter.time_from, max_time=Filter. \
    time_to, max_hod=Filter.hodnoceni_to, min_hod=Filter.hodnoceni_from, sel_name=int(Filter.name), serazeni=serazeni,palette=Palette)


@main.route('/zaznamy/set-serazeni/', methods=['POST', 'GET'])
@login_required
def setSerazeniZaznamy():
    serazeni = request.form['serazeni']
    return redirect('/zaznamy/' + serazeni)
@main.route('/zaznamy/reset-filter', methods=['POST', 'GET'])
@login_required
def OGzaznamy():
    languages = Jazyk.query.order_by(Jazyk.id).all()
    for language in languages:
        Filter.language_dict[language.id] = "on"
    tags = Tags.query.order_by(Tags.id).all()
    for tag in tags:
        Filter.tag_dict[tag.id] = "on"
    records = Denik.query.order_by(Denik.date).all()
    Filter.name = 0
    for r in records:
        Filter.date_from = r.date
        Filter.date_to = r.date
        Filter.time_from = r.time_spent
        Filter.time_to = r.time_spent
        Filter.hodnoceni_to = r.hodnoceni
        Filter.hodnoceni_from = r.hodnoceni
    try:
        for r in records:
            if(Filter.date_to < r.date):
                Filter.date_to = r.date
            if(Filter.date_from > r.date):
                Filter.date_from = r.date
            if(Filter.time_to < r.time_spent):
                Filter.time_to = r.date
            if(Filter.time_from > r.time_spent):
                Filter.time_from = r.time_spent
            if(int(Filter.hodnoceni_from) > int(r.hodnoceni)):
                Filter.hodnoceni_from = r.hodnoceni
            if(int(Filter.hodnoceni_to) < int(r.hodnoceni)):
                Filter.hodnoceni_to = r.hodnoceni
    except:
        pass

    return redirect('/zaznamy/1/')

