
import datetime
import json
from io import StringIO

from peewee import *
from flask import g


db = SqliteDatabase('journal.sqlite3')

class Entry(Model):
    title = CharField(unique=True)
    date = DateField(default=datetime.date.today(), formats='%m-%d-%Y')
    time_spent = TimeField()
    notes = TextField()
    resources = TextField()

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
        except:
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