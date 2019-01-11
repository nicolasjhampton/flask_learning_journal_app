import unittest

from peewee import *

from journal.models import *


class EntryTests(unittest.TestCase):
    db = SqliteDatabase(":memory:")

    sample_entry = {
        "title": "Sample Entry",
        "date": "1-2-2019",
        "time_spent": 1,
        "notes": "This is a test entry.",
        "resources": "http://testing.com,http://testing.org,http://testing.gov"
    }

    seed_data = None

    def setUp(self):
        _, self.seed_data = initialize(database=self.db, seed_db=True)

    def tearDown(self):
        self.db.close()

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
            Entry.get_by_id(3)

    def test_NEW_ENTRY(self):
        NEW_ENTRY(**self.sample_entry)
        entry = Entry.get(Entry.title == self.sample_entry.get('title'))
        for key, value in self.sample_entry.items():
            self.assertEqual(value, getattr(entry, key))


if __name__ == "__main__":
    unittest.main()
