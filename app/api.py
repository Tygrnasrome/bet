from flask import Blueprint

api = Blueprint('api', __name__)

import json
from flask import Flask, render_template, request, redirect, jsonify
from .models import Denik,Tags,User,Kategorie,Jazyk, Palettes
from flask_login import login_required, current_user
from .config import UI,Palette, Filter
from . import db


@api.route('/API', methods=['GET'])
def get_API():
    data = []
    language_dict = {}
    records = db.session.query(Denik).order_by(Denik.id).all()
    languages = db.session.query(Jazyk).order_by(Jazyk.id).all()
    for language in languages:
        language_dict[language.id] = language.name
    for record in records:
        data.append([record.id,record.date,record.time_spent,language_dict[record.jazyk_id],record.hodnoceni, record.popis])
    return jsonify(data)
@api.route('/API/ID/<int:id>')
def get_API_by_ID(id):
    data = []
    language_dict = {}
    records = db.session.query(Denik).filter_by(id=id)
    languages = db.session.query(Jazyk).order_by(Jazyk.id).all()
    for language in languages:
        language_dict[language.id] = language.name
    for record in records:
        data.append([record.id,record.date,record.time_spent,language_dict[record.jazyk_id],record.hodnoceni, record.popis])
    return jsonify(data)

@api.route('/API/PL/<string:prog_lang>')
def get_API_by_prog_lang_name(prog_lang):
    data = []
    language_dict = {}
    language = db.session.query(Jazyk).filter_by(name=prog_lang).first()
    records = db.session.query(Denik).filter_by(jazyk_id=language.id)
    languages = db.session.query(Jazyk).order_by(Jazyk.id).all()
    for language in languages:
        language_dict[language.id] = language.name
    for record in records:
        data.append([record.id,record.date,record.time_spent,language_dict[record.jazyk_id],record.hodnoceni, record.popis])
    return jsonify(data)

@api.route('/API/PL/<int:prog_lang>')
def get_API_by_prog_lang_id(prog_lang):
    data = []
    language_dict = {}

    records = db.session.query(Denik).filter_by(jazyk_id=prog_lang)
    languages = db.session.query(Jazyk).order_by(Jazyk.id).all()
    for language in languages:
        language_dict[language.id] = language.name
    for record in records:
        data.append([record.id,record.date,record.time_spent,language_dict[record.jazyk_id],record.hodnoceni, record.popis])
    return jsonify(data)

@api.route('/API/DATE/<string:date>')
def get_API_by_date(date):
    data = []
    language_dict = {}

    records = db.session.query(Denik).filter_by(date=date)
    languages = db.session.query(Jazyk).order_by(Jazyk.id).all()
    for language in languages:
        language_dict[language.id] = language.name
    for record in records:
        data.append([record.id,record.date,record.time_spent,language_dict[record.jazyk_id],record.hodnoceni, record.popis])
    return jsonify(data)

@api.route('/API/SCORE/<int:score>')
def get_API_by_score(score):
    data = []
    language_dict = {}

    records = db.session.query(Denik).filter_by(hodnoceni=score)
    languages = db.session.query(Jazyk).order_by(Jazyk.id).all()
    for language in languages:
        language_dict[language.id] = language.name
    for record in records:
        data.append([record.id,record.date,record.time_spent,language_dict[record.jazyk_id],record.hodnoceni, record.popis])
    return jsonify(data)