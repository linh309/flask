import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

"""
    1. Init app
        - Init db to create table in sql lite
    2. Build CLI command to execute a command from command line to init DB
"""

def init_db():
    db  = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_app_db(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)