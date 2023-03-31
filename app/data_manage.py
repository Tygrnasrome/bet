from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from . import db
import csv
import os
from .models import Note
from datetime import datetime

data = Blueprint('data', __name__)

@data.route('/', methods=['POST'])
def post():
    content = request.form['content']
    podpis = request.form['podpis']
    color =  request.form['color']
    new_note = Note(content=content,name=podpis,color=color)
    db.session.add(new_note)
    db.session.commit()
    return redirect('/')