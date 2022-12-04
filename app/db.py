import click
from flask import current_app, g
from flask.cli import with_appcontext

import sqlite3

con = sqlite3.connect("records.db")

cur = con.cursor()
people = [
     "'Fairy', 'Tooth', '2022-10-08 09:15:10', 1",
     "'Ruprecht', 'Knecht', '2022-10-08 09:15:13', 1",
     "'Bunny', 'Easter', '2022-10-08 09:15:27', 1",
]

def init_db():
    """
    Inicializuje databázi dle schema.sql
    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        db.commit()

    insert_cmd = "INSERT INTO recordD (name, popis, jazyk, hodnoceni) VALUES ('Fairy', 'Tooth', '2022-10-08 09:15:10', 1)"
    con.execute(insert_cmd)
    con.commit()
    print("hej hou")


def print_db():
    cur.execute("SELECT * FROM records")
    records = cur.fetchall()
    for record in records:
        print(record)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()






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
