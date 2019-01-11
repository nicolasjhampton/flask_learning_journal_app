import unittest
import html
from peewee import SqliteDatabase
from journal.models import initialize, get_seed_json, GET_ENTRY, Entry
from journal import journal
from contextlib import contextmanager
from flask import appcontext_pushed, g


class JournalTests(unittest.TestCase):

    def setUp(self):
        journal.app.config['DATABASE'] = 'journal_test.sqlite3'
        journal.app.config['WTF_CSRF_ENABLED'] = False
        journal.app.config['SEED_DB'] = True
        journal.app.testing = True
        journal.init_db()
        journal.db.drop_tables([Entry])
        self.app = journal.app
        self.seed_data = get_seed_json()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.test_client().get('/')
        self.assertEqual("302 FOUND", rv.status)
        self.assertIn(b"redirected", rv.data)
        self.assertIn(b"/entries", rv.data)

    def test_entries(self):
        rv = self.app.test_client().get('/entries')
        self.assertEqual("200 OK", rv.status)
        for idx, entry in enumerate(self.seed_data):
            title = entry.get('title')
            self.assertIn(title, html.unescape(str(rv.data)))
            self.assertIn('href="/entries/' + str(idx + 1) + '"', str(rv.data))
            self.assertIn('>' + entry.get('date') + '<', str(rv.data))

    def test_details(self):
        rv = self.app.test_client().get('/entries/2')
        self.assertEqual("200 OK", rv.status)
        for key, value in self.seed_data[1].items():
            if key == "resources":
                for resource in value.split(','):
                    self.assertIn(str(resource), html.unescape(str(rv.data)))
            else:
                self.assertIn(str(value), html.unescape(str(rv.data)))

    def test_new_entry(self):
        mock_entry = {
            'title': "This is a very big title that I should be able to find",
            'date': "2-18-1984",
            'time_spent': 6,
            'notes': "I cried some, but overall it was cool",
            'resources-0': "http://www.google.com",
        }
        self.app.test_client().post('/entry', data=mock_entry,
                                    follow_redirects=True)
        journal.db.connect()
        entry = GET_ENTRY(8)
        for key, value in mock_entry.items():
            if key == 'resources-0':
                self.assertEqual(value, getattr(entry, 'resources'))
            else:
                self.assertEqual(value, getattr(entry, key))

    def test_edit_entry(self):
        mock_entry = self.seed_data[0]
        del mock_entry['title']
        del mock_entry['resources']
        mock_entry['title'] = "New title"
        mock_entry['resources-0'] = "anything"
        rv = self.app.test_client().post('/entries/edit/1', data=mock_entry,
                                         follow_redirects=True)
        journal.db.connect()
        self.assertIn("New title", html.unescape(str(rv.data)))
