#!/usr/bin/env python2

import os
import bfp
import unittest
import tempfile
import sqlite3

class BFPTestCase(unittest.TestCase):
    TEST_DESCRIPTION = 'test description'

    def setUp(self):
        self.db_fd, bfp.app.config['DATABASE'] = tempfile.mkstemp()
        bfp.app.config['TESTING'] = True
        self.app = bfp.app.test_client()
        self.db = bfp.connect_db()
        self.db.row_factory = sqlite3.Row
        bfp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(bfp.app.config['DATABASE'])

    def test_create_problem(self):
        rv = self.app.post('/problem', data=dict(
            description=self.TEST_DESCRIPTION
        ))
        self.assertEqual(200, rv.status_code, 'The response code should be 200')
        self.assertTrue(rv.data, 'The response should contain data')
        problem = self.db.execute(
                'SELECT id, description FROM problem WHERE id=?',
                [rv.data]).fetchone()
        self.assertIsNotNone(problem,
                'A problem should be inserted into the db')
        self.assertEqual(self.TEST_DESCRIPTION, problem['description'],
                'The description should match in the database')

if __name__ == '__main__':
    unittest.main()
