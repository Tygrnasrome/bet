# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Palettes, Denik, Jazyk
from .config import Palette, UI, user_config_auth
from . import db

auth = Blueprint('auth', __name__)

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

@auth.route('/login/')
def login():
    UI.active = "login"
    users = User.query.order_by(User.id).all()
    return render_template('user/login.html', user = current_user,active=UI.active, palette=Palette, users=users)

@auth.route('/login/', methods=['POST'])
def login_post():
    name = request.form.get('name')
    if name == '':
        flash('Vyplňte prosím povinná pole','error')
        return redirect(url_for('auth.login')) # pokud není zadáno jméno, nebo email správně
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user_name = User.query.filter_by(name=name).first()
    user_email = User.query.filter_by(email=name).first()
    user = user_name
    if not user_name and not user_email:
        flash('Špatné přihlašovací údaje','error')
        return redirect(url_for('auth.login')) # pokud není zadáno jméno, nebo email správně
    if not user_name:
        user = user_email
        if not check_password_hash(user_email.password, password):
            flash('Špatné heslo (emailový login)','error')
            return redirect(url_for('auth.login')) # špatné heslo u email loginu
    else:
        if not check_password_hash(user_name.password, password):
                    flash('Špatné heslo','error')
                    return redirect(url_for('auth.login')) # špatné heslo u name loginu


    # if the above check passes, then we know the user has the right credentials
    flash('Uživatel přihlášen','notice')
    login_user(user, remember=remember)
    resetPalette()
    return redirect(url_for('auth.profile'))

@auth.route('/signup/')
@login_required
def signup():
    UI.active = "signup"
    if current_user.auth > 1:
        flash('Na tuto akci nemáte oprávnění')
        redirect(url_for('main.index'))
    return render_template('user/signup.html', user = current_user,active=UI.active, palette=Palette)

@auth.route('/signup/', methods=['POST'])
@login_required
def signup_post():
    if current_user.auth > 1:
        redirect(url_for('main.index'))
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # pokud vrátí user, email je již v databázi

    if user and not email == '':
        flash('Tento email je již využívaný jiným účtem','error')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(name=name).first() # pokud vrátí user, jméno je již v databázi

    if user:
        flash('Toto jméno je již využívané','error')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), auth=2)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash('Účet byl vytvořen','message')
    return redirect(url_for('auth.signup'))

@auth.route('/change/email', methods=['GET','POST'])
@login_required
def changeEmail():
    UI.active = "profile"
    if request.method == 'GET':
        return render_template('user/changeEmail.html', user = current_user ,active=UI.active, palette=Palette)
    else:
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user and not email == '':
            flash('Tento email je již využívaný jiným účtem','error')
            return redirect(url_for('auth.changeEmail'))
        old_email = current_user.email
        current_user.email = email
        db.session.commit()
        msg = 'Email byl změněn z {old} na {new}'
        flash(msg.format(old=old_email, new=email),'message')
        return redirect(url_for('auth.profile'))

@auth.route('/change/email/<int:id>', methods=['GET','POST'])
@login_required
def changeEmailConfig(id):
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "none"
    user_profile = User.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('user/changeEmailConfig.html', user = current_user ,active=UI.active, palette=Palette, user_profile=user_profile)
    else:
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user and not email == '':
            flash('Tento email je již využívaný jiným účtem','error')
            return redirect(url_for('auth.changeEmailConfig', id=id))
        old_email = user_profile.email
        user_profile.email = email
        db.session.commit()
        msg = 'Email byl změněn z {old} na {new}'
        flash(msg.format(old=old_email, new=email),'message')
        return redirect(url_for('auth.profileConfig', id=id))

@auth.route('/change/password', methods=['GET','POST'])
@login_required
def changePassword():
    if request.method == 'GET':
        UI.active = "profile"
        return render_template('user/changePassword.html', user = current_user ,active=UI.active, palette=Palette)
    else:
        password = request.form.get('password')
        if not check_password_hash(current_user.password, password):
            flash('Špatné heslo','error')
            return redirect(url_for('auth.changePassword')) # špatné heslo 
        
        new_password = request.form.get('new_password')
        new_password_again = request.form.get('new_password_again')

        if not new_password == new_password_again:
            flash('Nově zadaná hesla se neshodují','error')
            return redirect(url_for('auth.changePassword')) # neshodují se nově zadaná hesla
        current_user.password = generate_password_hash(new_password, method='sha256') 
        db.session.commit()
        flash('Heslo bylo změněno','message')
        return redirect(url_for('auth.profile'))

@auth.route('/change/password/<int:id>', methods=['GET','POST'])
@login_required
def changePasswordConfig(id):
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "none"
    user_profile = User.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('user/changePasswordConfig.html', user = current_user ,active=UI.active, palette=Palette, user_profile=user_profile)
    else:
        password = request.form.get('password')
        if not check_password_hash(current_user.password, password):
            flash('Špatné heslo','error')
            return redirect(url_for('auth.changePasswordConfig', id=id)) # špatné heslo admina
        
        new_password = request.form.get('new_password')
        new_password_again = request.form.get('new_password_again')

        if not new_password == new_password_again:
            flash('Nově zadaná hesla se neshodují','error')
            return redirect(url_for('auth.changePasswordConfig', id=id)) # neshodují se nově zadaná hesla 
        user_profile.password = generate_password_hash(new_password, method='sha256') 
        db.session.commit()
        flash('Heslo bylo změněno','message')
        return redirect(url_for('auth.profileConfig', id=id))

@auth.route('/change/name/<int:id>', methods=['GET','POST'])
@login_required
def changeNameConfig(id):
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "none"
    user_profile = User.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('user/changeNameConfig.html', user = current_user ,active=UI.active, palette=Palette, user_profile=user_profile)
    else:
        name = request.form.get('name')
        user = User.query.filter_by(name=name).first()
        if user:
            flash('Toto jméno je již využívané jiným účtem','error')
            return redirect(url_for('auth.changeNameConfig', id=id))
        old_name = user_profile.name
        user_profile.name = name
        db.session.commit()
        msg = 'Jméno bylo změněno z {old} na {new}'
        flash(msg.format(old=old_name, new=name),'message')
        return redirect(url_for('auth.profileConfig', id=id))

@auth.route('/change/auth/<int:id>', methods=['GET','POST'])
@login_required
def changeAuthConfig(id):
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "none"
    user_profile = User.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('user/changeAuthConfig.html', user = current_user ,active=UI.active, palette=Palette, user_profile=user_profile)
    else:
        auth = request.form.get('auth')
        user_profile.auth = auth
        db.session.commit()
        flash('Pravomoc byla změněna','message')
        return redirect(url_for('auth.profileConfig', id=id))

@auth.route('/profile/')
@login_required
def profile():
    palettes = Palettes.query.order_by(Palettes.id).all()
    languages = Jazyk.query.order_by(Jazyk.id).all()
    records = Denik.query.filter_by(name=current_user.id).all()
    stat = {'num':0, 'time':0}
    UI.active = "profile"
    for language in languages:
        stat[int(language.id)] = int(0)
    for record in records:
        stat['num'] += 1
        stat['time'] += record.time_spent
        stat[int(record.jazyk_id)] += record.time_spent
    for palette in palettes:
        if palette.user_id == current_user.id:
            return render_template('user/profile.html', user = current_user ,active=UI.active, palette=Palette, user_palette=palette, stat=stat, languages=languages)
    return render_template('user/profile.html', user = current_user ,active=UI.active, palette=Palette, user_palette=Palette, stat=stat, languages=languages)

@auth.route('/profile/config/<int:id>')
@login_required
def profileConfig(id):
    if not current_user.auth <= user_config_auth:
        flash("Na tuto akci nemáte oprávnění","error")
        return redirect('/')
    UI.active = "none"
    palettes = Palettes.query.order_by(Palettes.id).all()
    languages = Jazyk.query.order_by(Jazyk.id).all()
    records = Denik.query.filter_by(name=id).all()
    user_profile = User.query.filter_by(id=id).first()
    stat = {'num':0, 'time':0}
    for language in languages:
        stat[int(language.id)] = int(0)
    for record in records:
        stat['num'] += 1
        stat['time'] += record.time_spent
        stat[int(record.jazyk_id)] += record.time_spent
    for palette in palettes:
        if palette.user_id == user_profile.id:
            return render_template('user/profileConfig.html', user = current_user ,active=UI.active, palette=Palette, user_palette=palette, stat=stat, languages=languages, user_profile=user_profile)
    return render_template('user/profileConfig.html', user = current_user ,active=UI.active, palette=Palette, user_palette=Palette, stat=stat, languages=languages, user_profile=user_profile)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Uživatel odhlášen','message')
    Palette.base = Palette.def_base
    Palette.hover = Palette.def_hover
    Palette.selected = Palette.def_selected
    Palette.divone = Palette.def_divone
    Palette.divthree = Palette.def_divthree
    Palette.divtwo = Palette.def_divtwo
    Palette.body = Palette.def_body
    Palette.header = Palette.def_header
    Palette.text = Palette.def_text
    return redirect(url_for('main.index'))

