#!/usr/bin/env python3

from flask import Flask, render_template, g, redirect, url_for
from peewee import SqliteDatabase
from .models import initialize, ALL_ENTRIES, GET_ENTRY

app = Flask(__name__)

DEBUG = True
PORT = 4000
HOST = "0.0.0.0"

app.config.from_object(__name__)
app.config.update(dict(
    DATABASE='journal.sqlite3',
    SEED_DB=False
))


@app.before_request
def before_request():
    """Connect to database"""
    g.db ,_ = initialize(
        database=SqliteDatabase(app.config['DATABASE']),
        seed_db=app.config['SEED_DB']
    )

@app.after_request
def after_request(response):
    """Close database connection"""
    g.db.close()
    return response

@app.route("/")
def index():
    return redirect(url_for('list_entries'))

@app.route("/entries")
def list_entries():
    entries = ALL_ENTRIES()
    return render_template('index.html', entries=entries)

@app.route("/entries/<slug>")
def details(slug=None):
    entry = GET_ENTRY(entry_id=slug)
    return render_template('detail.html', entry=entry)

@app.route("/entries/edit/<slug>")
def edit():
    pass

@app.route("/entries/delete/<slug>")
def delete():
    pass

@app.route("/entry")
def add():
    pass

def run():
    initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)

if __name__ == "__main__":
    run()