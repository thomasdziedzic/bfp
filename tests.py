#!/usr/bin/env python2

import os
import bfp
import unittest
import tempfile
import sqlite3
import json

class BFPTestCase(unittest.TestCase):
    TEST_DESCRIPTION = 'test description'
    NEW_TEST_DESCRIPTION = 'new %s' % TEST_DESCRIPTION
    OTHER_DESCRIPTION = 'other description'

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

    def create_problem(self):
        problem_id = self.db.execute(
                'INSERT INTO problem (description) VALUES (?)',
                [self.TEST_DESCRIPTION]).lastrowid
        self.db.commit()
        return problem_id

    def test_create_problem(self):
        rv = self.app.post('/problem', data=dict(
            description=self.TEST_DESCRIPTION
        ))
        self.assertEqual(200, rv.status_code, 'The http code should be 200')
        self.assertTrue(rv.data, 'The response should contain data')

        resp_dict = json.loads(rv.data)
        self.assertEqual(type(resp_dict), dict,
                'Response body should be a json dict')
        self.assertIn('problem_id', resp_dict,
                'The problem id should be returned with the response')

        problem = self.db.execute(
                'SELECT id, description FROM problem WHERE id=?',
                [resp_dict['problem_id']]).fetchone()
        self.assertIsNotNone(problem,
                'A problem should be inserted into the db')
        self.assertEqual(self.TEST_DESCRIPTION, problem['description'],
                'The description should match in the database')

    def test_read_problem(self):
        problem_id = self.create_problem()
        rv = self.app.get('/problem/%s' % problem_id)
        self.assertEqual(200, rv.status_code, 'The http code should be 200')

        resp_dict = json.loads(rv.data)
        self.assertEqual(type(resp_dict), dict,
                'Response body should be a json dict')
        self.assertIn('description', resp_dict,
                'The description should be returned with the response')
        self.assertEqual(self.TEST_DESCRIPTION, resp_dict['description'],
                'The data should contain the test description')

    def test_read_problem_does_not_exist(self):
        rv = self.app.get('/problem/1')
        self.assertEqual(404, rv.status_code, 'The problem should not be found')

    def test_update_problem(self):
        problem_id = self.create_problem()
        rv = self.app.patch('/problem/%s' % problem_id, data=json.dumps(dict(
            description=self.NEW_TEST_DESCRIPTION
        )))
        self.assertEqual(200, rv.status_code, 'The http code should be 200')
        problem = self.db.execute(
                'SELECT id, description FROM problem WHERE id=?',
                [problem_id]).fetchone()
        self.assertEqual(self.NEW_TEST_DESCRIPTION, problem['description'],
                'The description should match in the database')

    def test_delete_problem(self):
        problem_id = self.create_problem()
        rv = self.app.delete('/problem/%s' % problem_id)
        problem = self.db.execute(
                'SELECT id, description FROM problem WHERE id=?',
                [problem_id]).fetchone()
        self.assertIsNone(problem, 'The problem should be deleted')

if __name__ == '__main__':
    unittest.main()
