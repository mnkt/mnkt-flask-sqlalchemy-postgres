# flaskr/db.py
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .model import db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db.session.remove()


def init_db():
    with current_app.app_context():
        db.create_all()

@click.command('init-db')
@with_appcontext

def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
