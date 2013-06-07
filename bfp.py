#!/usr/bin/env python2

import sqlite3
from flask import Flask, g, request, abort
from contextlib import closing

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

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/problem', methods=['POST'])
def create_problem():
    g.db.execute('INSERT INTO problem (description) VALUES (?)',
        [request.form['description']])
    g.db.commit()
    return ''

@app.route('/problem/<int:problem_id>', methods=['GET'])
def read_problem(problem_id):
    cur = g.db.execute('SELECT id, description FROM problem WHERE id=?',
        [problem_id]).fetchone()

    # if it doesn't exist then 404
    if cur is None:
        abort(404)
    else:
        return '%s;%s' % (cur[0], cur[1])

@app.route('/problem/<int:problem_id>', methods=['PATCH'])
def update_problem(problem_id):
    g.db.execute('UPDATE problem SET description=? WHERE id=?',
            [request.form['description'], problem_id])
    g.db.commit()
    return ''

@app.route('/problem/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    g.db.execute('DELETE FROM problem WHERE id=?', [problem_id])
    g.db.commit()
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
