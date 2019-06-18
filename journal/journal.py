#!/usr/bin/env python3

import os
from flask import Flask, render_template, g, redirect, url_for, flash, request
from peewee import PostgresqlDatabase
from playhouse.db_url import connect
from .models import (initialize, ALL_ENTRIES, GET_ENTRY,
                     NEW_ENTRY, DELETE_ENTRY, EDIT_ENTRY)
from .forms import EntryForm

app = Flask(__name__)

DEBUG = True
PORT = int(os.getenv('PORT', '4000'))
HOST = os.getenv('HOST', "0.0.0.0")

app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.getenv('DATABASE', 'peewee_diary'),
    USER=os.getenv('USER', 'postgres'),
    DB_HOST=os.getenv('DB_HOST', 'localhost'),
    SEED_DB=True,
    SECRET_KEY=os.getenv('SECRET', 'shh...it\'s a secret!'),
    KEEP_OPEN=False,
))




db = None


def init_db():
    global db
    db = connect(os.getenv('DATABASE_URL','sqlite:///journal.sqlite3'))
    # PostgresqlDatabase(
    #     app.config['DATABASE'],
    #     user=app.config['USER'],
    #     host=app.config['DB_HOST']
    # )


@app.before_request
def before_request():
    """Connect to database"""
    g.db, _ = initialize(
        database=db,
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


@app.route("/entries/edit/<slug>", methods=('GET', 'POST'))
def edit(slug=None):
    form = EntryForm()
    if form.validate_on_submit():
        flash("Update Successful!", "success")
        resources = ",".join([f.data for f in form.resources.entries])
        EDIT_ENTRY(
            entry_id=slug,
            title=form.title.data,
            date=form.date.data,
            time_spent=int(form.time_spent.data),
            notes=form.notes.data,
            resources=resources,
        )
        return redirect("/entries/" + slug)
    if request.method == 'GET':
        entry = GET_ENTRY(entry_id=slug)
        form = EntryForm(
            title=entry.title,
            date=entry.date,
            time_spent=int(entry.time_spent),
            notes=entry.notes,
            resources=entry.resources.split(','),
        )
    return render_template('edit.html', form=form, id=slug,
                           getattr=getattr, str=str)


@app.route("/entries/delete/<slug>")
def delete(slug=None):
    DELETE_ENTRY(entry_id=slug)
    return redirect(url_for('list_entries'))


@app.route("/entry", methods=("GET", "POST"))
def add():
    form = EntryForm()
    if form.validate_on_submit():
        flash("Entry Successful!", "success")
        resources = ",".join([f.data for f in form.resources.entries])
        NEW_ENTRY(
            title=form.title.data,
            date=form.date.data,
            time_spent=int(form.time_spent.data),
            notes=form.notes.data,
            resources=resources,
        )
        return redirect(url_for('list_entries'))
    return render_template('new.html', form=form)


def run(env, req):
    init_db()
    initialize()
    app.run(env, req)


if __name__ == "__main__":
    run()
