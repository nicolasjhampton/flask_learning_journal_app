import os
import datetime
import json
from io import StringIO

from peewee import *
from flask import g


# db = SqliteDatabase('journal.sqlite3')
db = PostgresqlDatabase(
    os.getenv('DATABASE', 'peewee_diary'),
    user=os.getenv('USER', 'postgres'),
    host=os.getenv('DB_HOST', 'localhost'),
)


class Entry(Model):
    title = CharField()
    date = DateField(default=datetime.date.today, formats='%m-%d-%Y')
    time_spent = IntegerField()
    notes = TextField()
    resources = CharField()

    class Meta:
        database = db


# /entries
def ALL_ENTRIES():
    return Entry.select()


# /entries/<slug>
def GET_ENTRY(entry_id):
    return Entry.get_by_id(entry_id)


# /entries/edit/<slug>
def EDIT_ENTRY(entry_id, **kwargs):
    Entry.set_by_id(entry_id, kwargs)


# /entries/delete/<slug>
def DELETE_ENTRY(entry_id):
    Entry.delete_by_id(entry_id)


# /entry
def NEW_ENTRY(**kwargs):
    Entry.create(**kwargs)


def get_seed_json():
    with open('entries.json', 'r') as raw_entries:
        data = json.load(raw_entries)
        entries = data.get('entries')
    return entries


def seed():
    entries = get_seed_json()
    for entry in entries:
        try:
            Entry.create(**entry)
        except Exception:
            pass
    return entries


def initialize(database=None, seed_db=False):
    entries = None
    if not database:
        database = db
        database.connect()
    else:
        database.connect()
        database.bind([Entry])
    database.create_tables([Entry], safe=True)
    if seed_db:
        entries = seed()
    return database, entries
