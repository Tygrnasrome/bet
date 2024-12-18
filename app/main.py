import sqlite3
import json
from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from .models import User, Palettes
from flask import Blueprint
from flask_login import login_required, current_user
from .config import UI,Palette, obj_config_auth
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
    admin_acc = User(id=0,name='admin', email='', password=generate_password_hash('1234', method='pbkdf2:sha256'), auth=1)
    db.session.add(admin_acc)
    db.session.commit()


@main.route('/')
def index():
    global admin_acc
    db.create_all()
    try:
        admin_acc = User.query.get_or_404(0)
    except:
        setAdminAcc()
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
