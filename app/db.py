import click
from flask import current_app, g
from flask.cli import with_appcontext

import sqlite3

con = sqlite3.connect("db.db")
cur = con.cursor()

def get_db():
    if 'db' not in g:
        db.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Inicializuje databázi dle schema.sql
    """
    with current_app.open_resource('schema.sql') as f:
        con.executescript(f.read().decode('utf8'))
        con.commit()

def print_db():
    cur.execute("SELECT * FROM person")
    records = cur.fetchall()
    for record in records:
        print(record)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Definujeme příkaz příkazové řádky
    """
    init_db()
    print_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
