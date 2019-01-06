import unittest
import datetime
import json
from io import StringIO

from peewee import *
from playhouse.shortcuts import model_to_dict
from flask import g


from functools import wraps

db = None

if __name__ == "__main__":
    db = SqliteDatabase(':memory:')
else:
    db = SqliteDatabase('journal.sqlite3')
    # adds database connection to flask global namespace
    g.db = db

class Entry(Model):
    #Title, Date, Time Spent, What You Learned, Resources to Remember
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

def seed():
    entries = None
    with open('entries.json', 'r') as raw_entries:
        data = json.load(raw_entries)
        entries = data.get('entries')
        for entry in entries:
            Entry.create(**entry)
    return entries

def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)


class EntryTests(unittest.TestCase):
    sample_entry = {
        "title": "Sample Entry",
        "date": "1-2-2019",
        "time_spent": 1,
        "notes": "This is a test entry.",
        "resources": "http://testing.com,http://testing.org,http://testing.gov"
    }
    seed_data = None

    def setUp(self):
        db.connect()
        db.create_tables([Entry], safe=True)
        self.seed_data = seed()

    def tearDown(self):
        db.close()

    def test_ALL_ENTRIES(self):
        entries = ALL_ENTRIES()
        self.assertEqual(len(entries), len(self.seed_data))

    def test_GET_ENTRY(self):
        entry1 = Entry.get(Entry.title == self.seed_data[3]['title'])
        entry2 = GET_ENTRY(entry1.id)
        for key, value in self.seed_data[3].items():
            self.assertEqual(value, getattr(entry2, key))

    def test_EDIT_ENTRY(self):
        entry1 = Entry.get(Entry.title == self.seed_data[2]['title'])
        EDIT_ENTRY(entry1.id, time_spent=72)
        entry2 = Entry.get(Entry.title == self.seed_data[2]['title'])
        self.assertNotEqual(entry1, entry2.time_spent)
        self.assertEqual(entry2.time_spent, 72)
        for key, value in self.seed_data[2].items():
            if key != "time_spent":
                self.assertEqual(getattr(entry2, key), getattr(entry1, key))
                self.assertEqual(getattr(entry2, key), value)

    def test_DELETE_ENTRY(self):
        DELETE_ENTRY(3)
        with self.assertRaises(DoesNotExist):
            entry = Entry.get_by_id(3)

    def test_NEW_ENTRY(self):
        NEW_ENTRY(**self.sample_entry)
        entry = Entry.get(Entry.title == self.sample_entry.get('title'))
        for key, value in self.sample_entry.items():
            self.assertEqual(value, getattr(entry, key))


if __name__ == "__main__":
    unittest.main()