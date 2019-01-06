import unittest
import datetime
import json
from io import StringIO

from peewee import *
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

# / /entries /entries/<slug> /entries/edit/<slug> /entries/delete/<slug> /entry

def to_dictionary(func):
    @wraps(func)
    def inner(**kwargs):
        return func(**kwargs).dicts()
    return inner

# /entries
@to_dictionary
def ALL_ENTRIES():
    pass

# /entries/<slug>
@to_dictionary
def GET_ENTRY(**kwargs):
    pass

# /entries/edit/<slug>
@to_dictionary
def EDIT_ENTRY(**kwargs):
    pass

# /entries/delete/<slug>
@to_dictionary
def DELETE_ENTRY(**kwargs):
    pass

# /entry
@to_dictionary
def NEW_ENTRY(**kwargs):
    pass

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
        self.assertCountEqual(entries, self.seed_data)

    def test_GET_ENTRY(self):
        entry1 = Entry.get(Entry.title == self.seed_data[3].title)[0]
        entry2 = GET_ENTRY(id=entry1.id)
        for key, value in entry2.items():
            self.assertEqual(value, self.seed_data[3][key])

    def test_EDIT_ENTRY(self):
        entry1 = Entry.get(Entry.title == self.seed_data[2].title)[0]
        EDIT_ENTRY(id=entry1.id, time_spent=72)
        entry2 = Entry.get(Entry.title == self.seed_data[2].title)[0].dicts()
        self.assertNotEqual(entry1, entry2['time_spent'])
        self.assertEqual(entry2['time_spent'], 72)
        for key, value in entry2.items():
            if key != "time_spent":
                self.assertEqual(value, entry1[key])
        pass

    def test_DELETE_ENTRY(self):
        DELETE_ENTRY(id=3)
        with self.assertRaises(DoesNotExist):
            entry = Entry.get_by_id(3)

    def test_NEW_ENTRY(self):
        NEW_ENTRY(**self.sample_entry)
        entry = Entry.get(Entry.title == self.sample_entry.get('title')).dicts()
        for key, value in entry.items():
            self.assertEqual(value, self.sample_entry.get(key))


if __name__ == "__main__":
    unittest.main()