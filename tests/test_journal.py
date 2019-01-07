import unittest
import html
from peewee import SqliteDatabase
from journal.models import initialize, get_seed_json
from journal import journal

class JournalTests(unittest.TestCase):
    db = SqliteDatabase(":memory:")

    def setUp(self):
        journal.app.config['DATABASE'] = ":memory:"
        journal.app.config['SEED_DB'] = True
        journal.app.testing = True
        self.app = journal.app.test_client()
        self.seed_data = get_seed_json()

    def tearDown(self):
        self.db.close()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual("302 FOUND", rv.status)
        self.assertIn(b"redirected", rv.data)
        self.assertIn(b"/entries", rv.data)

    def test_entries(self):
        rv = self.app.get('/entries')
        self.assertEqual("200 OK", rv.status)
        for idx, entry in enumerate(self.seed_data):
            title = entry.get('title')
            self.assertIn(title, html.unescape(str(rv.data)))
            self.assertIn('href="/entries/' + str(idx + 1) + '"', str(rv.data))
            self.assertIn('>' + entry.get('date') + '<', str(rv.data))

    def test_details(self):
        rv = self.app.get('/entries/2')
        self.assertEqual("200 OK", rv.status)
        for key, value in self.seed_data[1].items():
            if key == "resources":
                for resource in value.split(','):
                    self.assertIn(str(resource), html.unescape(str(rv.data)))
            else:
                self.assertIn(str(value), html.unescape(str(rv.data)))