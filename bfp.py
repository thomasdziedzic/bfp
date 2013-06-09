#!/usr/bin/env python2

import sqlite3
from flask import Flask, g, request, abort
from contextlib import closing
import json

DATABASE = '/tmp/bfp.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/problem', methods=['POST'])
def create_problem():
    req_dict = json.loads(request.data)
    cur = g.db.execute('INSERT INTO problem (description) VALUES (?)',
        [req_dict['description']])
    g.db.commit()

    return json.dumps(dict(
        id=cur.lastrowid
    ))

@app.route('/problems', methods=['GET'])
def read_problems():
    problem_rows = g.db.execute(
            'SELECT id, description FROM problem').fetchall()

    problems = [{'id': problem_row['id'],
            'description': problem_row['description']}
            for problem_row in problem_rows]

    return json.dumps(problems)

@app.route('/problem/<int:problem_id>', methods=['GET'])
def read_problem(problem_id):
    cur = g.db.execute('SELECT id, description FROM problem WHERE id=?',
        [problem_id]).fetchone()

    idea_rows = g.db.execute('''
        SELECT i.id, i.description
        FROM problemidea as pi
        INNER JOIN idea AS i
        ON pi.idea_id = i.Id
        WHERE pi.problem_id=?
        ''', [problem_id]).fetchall()
    ideas = [{'id': idea_row['id'], 'description': idea_row['description']}
            for idea_row in idea_rows]

    # if it doesn't exist then 404
    if cur is None:
        abort(404)
    else:
        return json.dumps(dict(
            description=cur['description'],
            ideas=ideas
        ))

@app.route('/problem/<int:problem_id>', methods=['PATCH'])
def update_problem(problem_id):
    req_dict = json.loads(request.data)
    g.db.execute('UPDATE problem SET description=? WHERE id=?',
            [req_dict['description'], problem_id])
    g.db.commit()
    return ''

@app.route('/problem/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    g.db.execute('DELETE FROM problem WHERE id=?', [problem_id])
    g.db.commit()
    return ''

@app.route('/idea', methods=['POST'])
def create_idea():
    req_dict = json.loads(request.data)
    cur = g.db.execute('INSERT INTO idea (description) VALUES (?)',
        [req_dict['description']])
    g.db.commit()

    return json.dumps(dict(
        id=cur.lastrowid
    ))

@app.route('/idea/<int:idea_id>', methods=['GET'])
def read_idea(idea_id):
    cur = g.db.execute('SELECT id, description FROM idea WHERE id=?',
        [idea_id]).fetchone()

    problem_rows = g.db.execute('''
        SELECT p.id, p.description
        FROM problemidea as pi
        INNER JOIN problem AS p
        ON pi.idea_id = p.Id
        WHERE pi.idea_id=?
        ''', [idea_id]).fetchall()
    problems = [{'id': problem_row['id'],
            'description': problem_row['description']}
            for problem_row in problem_rows]

    # if it doesn't exist then 404
    if cur is None:
        abort(404)
    else:
        return json.dumps(dict(
            description=cur['description'],
            problems=problems
        ))

@app.route('/idea/<int:idea_id>', methods=['PATCH'])
def update_idea(idea_id):
    req_dict = json.loads(request.data)
    g.db.execute('UPDATE idea SET description=? WHERE id=?',
            [req_dict['description'], idea_id])
    g.db.commit()
    return ''

@app.route('/idea/<int:idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    g.db.execute('DELETE FROM idea WHERE id=?', [idea_id])
    g.db.commit()
    return ''

@app.route('/problemidea/<int:problem_id>/<int:idea_id>', methods=['POST'])
def create_problemidea(problem_id, idea_id):
    existing_problemideas = g.db.execute('''
        SELECT id
        FROM problemidea
        WHERE problem_id=?
        AND idea_id=?
        ''', [problem_id, idea_id]).fetchall()

    if(len(existing_problemideas) == 0):
        g.db.execute(
                'INSERT INTO problemidea (problem_id, idea_id) VALUES (?, ?)',
                [problem_id, idea_id])
        g.db.commit()

    return ''

@app.route('/problemidea/<int:problem_id>/<int:idea_id>', methods=['DELETE'])
def delete_problemidea(problem_id, idea_id):
    g.db.execute(
            'DELETE FROM problemidea WHERE problem_id=? AND idea_id=?',
            [problem_id, idea_id])
    g.db.commit()
    return ''

@app.route('/search/problems', methods=['POST'])
def search_problems():
    query = json.loads(request.data)['query']
    problem_rows = g.db.execute('''
        SELECT id, description
        FROM problem
        WHERE description LIKE '%' || ? || '%'
        ''', [query]).fetchall()
    problems = [{'id': problem_row['id'],
            'description': problem_row['description']}
            for problem_row in problem_rows]
    return json.dumps(problems)

@app.route('/search/ideas', methods=['POST'])
def search_ideas():
    query = json.loads(request.data)['query']
    idea_rows = g.db.execute('''
        SELECT id, description
        FROM idea
        WHERE description LIKE '%' || ? || '%'
        ''', [query]).fetchall()
    ideas = [{'id': idea_row['id'],
            'description': idea_row['description']}
            for idea_row in idea_rows]
    return json.dumps(ideas)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
