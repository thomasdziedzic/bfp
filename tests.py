#!/usr/bin/env python2

import os
import bfp
import unittest
import tempfile
import sqlite3
import json

class BFPTestCase(unittest.TestCase):
    PROBLEM_DESCRIPTION = 'test description'
    NEW_PROBLEM_DESCRIPTION = 'new %s' % PROBLEM_DESCRIPTION
    IDEA_DESCRIPTION = 'other description'
    NEW_IDEA_DESCRIPTION = 'new %s' % IDEA_DESCRIPTION

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
                [self.PROBLEM_DESCRIPTION]).lastrowid
        self.db.commit()
        return problem_id

    def create_idea(self):
        idea_id = self.db.execute(
                'INSERT INTO idea (description) VALUES (?)',
                [self.IDEA_DESCRIPTION]).lastrowid
        self.db.commit()
        return idea_id

    def create_problemidea(self, problem_id, idea_id):
        problemidea_id = self.db.execute(
                'INSERT INTO problemidea (problem_id, idea_id) VALUES (?, ?)',
                [problem_id, idea_id]).lastrowid
        self.db.commit()
        return problemidea_id

    def test_create_problem(self):
        rv = self.app.post('/problem', data=json.dumps(dict(
            description=self.PROBLEM_DESCRIPTION
        )))
        self.assertEqual(200, rv.status_code, 'The http code should be 200')
        self.assertTrue(rv.data, 'The response should contain data')

        resp_dict = json.loads(rv.data)
        self.assertEqual(type(resp_dict), dict,
                'Response body should be a json dict')
        self.assertIn('id', resp_dict,
                'The problem id should be returned with the response')

        problem = self.db.execute(
                'SELECT id, description FROM problem WHERE id=?',
                [resp_dict['id']]).fetchone()
        self.assertIsNotNone(problem,
                'A problem should be inserted into the db')
        self.assertEqual(self.PROBLEM_DESCRIPTION, problem['description'],
                'The description should match in the database')

    def test_read_problem(self):
        problem_id = self.create_problem()
        idea_id = self.create_idea()
        problemidea_id = self.create_problemidea(problem_id, idea_id)
        rv = self.app.get('/problem/%s' % problem_id)
        self.assertEqual(200, rv.status_code, 'The http code should be 200')

        resp_dict = json.loads(rv.data)
        self.assertEqual(type(resp_dict), dict,
                'Response body should be a json dict')
        self.assertIn('description', resp_dict,
                'The description should be returned with the response')
        self.assertEqual(self.PROBLEM_DESCRIPTION, resp_dict['description'],
                'The data should contain the test description')
        self.assertIn('ideas', resp_dict,
                'The ideas related to the problem should be sent')
        ideas = resp_dict['ideas']
        self.assertEqual(type(ideas), list, 'The ideas should be a list')
        self.assertEqual(len(ideas), 1, 'There should be 1 idea')
        idea = ideas[0]
        self.assertEqual(type(idea), dict, 'The idea should be a dict')
        self.assertIn('id', idea, 'The id should be returned')
        self.assertEqual(idea_id, idea['id'], 'The idea id should match')
        self.assertIn('description', idea, 'The description should be returned')
        self.assertEqual(self.IDEA_DESCRIPTION, idea['description'],
                'The idea description should match')

    def test_read_problem_does_not_exist(self):
        rv = self.app.get('/problem/1')
        self.assertEqual(404, rv.status_code, 'The problem should not be found')

    def test_update_problem(self):
        problem_id = self.create_problem()
        rv = self.app.patch('/problem/%s' % problem_id, data=json.dumps(dict(
            description=self.NEW_PROBLEM_DESCRIPTION
        )))
        self.assertEqual(200, rv.status_code, 'The http code should be 200')
        problem = self.db.execute(
                'SELECT id, description FROM problem WHERE id=?',
                [problem_id]).fetchone()
        self.assertEqual(self.NEW_PROBLEM_DESCRIPTION, problem['description'],
                'The description should match in the database')

    def test_delete_problem(self):
        problem_id = self.create_problem()
        rv = self.app.delete('/problem/%s' % problem_id)
        problem = self.db.execute(
                'SELECT id, description FROM problem WHERE id=?',
                [problem_id]).fetchone()
        self.assertIsNone(problem, 'The problem should be deleted')

    def test_create_idea(self):
        rv = self.app.post('/idea', data=json.dumps(dict(
            description=self.IDEA_DESCRIPTION
        )))
        self.assertEqual(200, rv.status_code, 'The http code should be 200')
        self.assertTrue(rv.data, 'The response should contain data')

        resp_dict = json.loads(rv.data)
        self.assertEqual(type(resp_dict), dict,
                'Response body should be a json dict')
        self.assertIn('id', resp_dict,
                'The idea id should be returned with the response')

        idea = self.db.execute(
                'SELECT id, description FROM idea WHERE id=?',
                [resp_dict['id']]).fetchone()
        self.assertIsNotNone(idea,
                'An idea should be inserted into the db')
        self.assertEqual(self.IDEA_DESCRIPTION, idea['description'],
                'The description should match in the database')

    def test_read_idea(self):
        idea_id = self.create_idea()
        problem_id = self.create_problem()
        problemidea_id = self.create_problemidea(problem_id, idea_id)
        rv = self.app.get('/idea/%s' % idea_id)
        self.assertEqual(200, rv.status_code, 'The http code should be 200')

        resp_dict = json.loads(rv.data)
        self.assertEqual(type(resp_dict), dict,
                'Response body should be a json dict')
        self.assertIn('description', resp_dict,
                'The description should be returned with the response')
        self.assertEqual(self.IDEA_DESCRIPTION, resp_dict['description'],
                'The data should contain the test description')
        self.assertIn('problems', resp_dict,
                'The problems related to the idea should be sent')
        problems = resp_dict['problems']
        self.assertEqual(type(problems), list, 'The problems should be a list')
        self.assertEqual(len(problems), 1, 'There should be 1 problem')
        problem = problems[0]
        self.assertEqual(type(problem), dict, 'The problem should be a dict')
        self.assertIn('id', problem, 'The id should be returned')
        self.assertEqual(problem_id, problem['id'],
                'The problem id should match')
        self.assertIn('description', problem,
                'The description should be returned')
        self.assertEqual(self.PROBLEM_DESCRIPTION, problem['description'],
                'The problem description should match')

    def test_read_idea_does_not_exist(self):
        rv = self.app.get('/idea/1')
        self.assertEqual(404, rv.status_code, 'The idea should not be found')

    def test_update_idea(self):
        idea_id = self.create_idea()
        rv = self.app.patch('/idea/%s' % idea_id, data=json.dumps(dict(
            description=self.NEW_IDEA_DESCRIPTION
        )))
        self.assertEqual(200, rv.status_code, 'The http code should be 200')
        idea = self.db.execute(
                'SELECT id, description FROM idea WHERE id=?',
                [idea_id]).fetchone()
        self.assertEqual(self.NEW_IDEA_DESCRIPTION, idea['description'],
                'The description should match in the database')

    def test_delete_idea(self):
        idea_id = self.create_idea()
        rv = self.app.delete('/idea/%s' % idea_id)
        idea = self.db.execute(
                'SELECT id, description FROM idea WHERE id=?',
                [idea_id]).fetchone()
        self.assertIsNone(idea, 'The idea should be deleted')

if __name__ == '__main__':
    unittest.main()
