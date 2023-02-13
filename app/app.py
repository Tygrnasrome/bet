#import os

#import sqlite3
#from flask import Flask, render_template, request, redirect
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime

#app = Flask(__name__)

#app.config.from_mapping(
#    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
#)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denik.db'
#db = SQLAlchemy(app)


# ensure the instance folder exists
#try:
#    os.makedirs(app.instance_path)
#except OSError:
#    pass



#if __name__ == '__main__':
#    app.run(debug=true)
