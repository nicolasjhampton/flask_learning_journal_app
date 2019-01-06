from peewee import *
import unittest

from functools import wraps

db = None

if __name__ == "__main__":
    db = SqliteDatabase(':memory:')
else:
    db = SqliteDatabase('journal.sqlite3')

class Entry(Model):
    #Title, Date, Time Spent, What You Learned, Resources to Remember
    title = CharField(unique=True)
    date = DateField(default=datetime.date.today())
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
def GET_ENTRY():
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

def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)


class EntryTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass



if __name__ == "__main__":
    unittest.main()