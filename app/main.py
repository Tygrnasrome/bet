import sqlite3
import json
from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from . import db, api_commits, api_users, api_sys
from .models import User, Commit

main = Blueprint('main', __name__)

def saveApi():
    for user in api_users:
        data_dict = {}
        i = 0
        for data in user:
            data_dict[i] = data 
            i += 1
        if not User.query.filter_by(userID=data_dict[4]).first():
            # add the new user to the database
            new_user = User(name=data_dict[0], surname=data_dict[1], nick=data_dict[2], userID=data_dict[4])
            db.session.add(new_user)
            db.session.commit()
    for commit in api_commits:
        data_dict = {}
        i = 0
        for data in commit:
            data_dict[i] = data 
            i += 1
        db_commit = Commit.query.filter_by(commit_id=data_dict[5]).first()
        if not db_commit:
            # add the new commit to the database
            new_commit = Commit(creator_id=data_dict[0], date=data_dict[1], lines_added=data_dict[2], lines_removed=data_dict[3], description=data_dict[4], commit_id=data_dict[5])
            db.session.add(new_commit)
            db.session.commit()
        author = User.query.filter_by(userID=data_dict[0]).first()
        if author:
            author.lines_added += db_commit.lines_added
            author.lines_removed += db_commit.lines_removed
            db.session.commit()
        else:
            return data_dict[0]


@main.route('/')
def index():
    db.create_all()
    return render_template('index.html')

@main.route('/stats/')
def stats():
    db.create_all()
    #data = api_users.text
    #parse_json = json.loads(data)
    saveApi()
    labels = []
    data = []
    for user in User.query.order_by(User.name).all():
        fullname = "{name} {surname}"
        fullname.format(name= user.name, surname=user.surname)
        labels.append(fullname)
        data.append(user.lines_added)
        data.append(user.lines_removed)
    
    return render_template('stat.html',labels = labels, data = data)