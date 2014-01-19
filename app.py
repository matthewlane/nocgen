#!/usr/bin/env python
from flask import Flask, g, render_template, request
import sqlite3
import json

app = Flask(__name__)
DATABASE = 'nocgen.db'


@app.route('/')
def index():
    return render_template('index.html', numbers=get_numbers())


@app.route("/numbers", methods=["GET"])
def get_numbers():
    numbers = query_db("SELECT * FROM numbers")
    return json.dumps(numbers)


# @app.route("/numbers/<int:id>")
# def get_number(id):
#     number = query_db("SELECT * FROM numbers WHERE id = ?", [id], one=True)
#     return json.dumps(number)


@app.route("/numbers", methods=["POST"])
def new_number():
    n = int(request.json["n"])

    def fib(n):
        if n <= 1:
            return n
        else:
            return fib(n - 1) + fib(n - 2)

    fib = fib(n)

    c = g.db.cursor()
    c.execute("INSERT INTO numbers VALUES(null, ?, ?)", (n, fib))
    g.db.commit()

    number = {"id": c.lastrowid, "n": n, "fib": fib}
    return json.dumps(number)


# @app.route("/users/<int:id>", methods=["PUT"])
# def edit_user(id):
#     firstname = request.json["firstname"]
#     lastname = request.json["lastname"]
#     age = int(request.json["age"])

#     c = g.db.cursor()
#     c.execute("UPDATE users SET firstname = ?, lastname = ?, age = ? WHERE id = ?",
#              (firstname, lastname, age, id))
#     g.db.commit()

#     return json.dumps(request.json)


@app.route("/numbers/<int:id>", methods=["DELETE"])
def delete_number(id):
    c = g.db.cursor()
    c.execute("DELETE FROM numbers WHERE id = ?", (id,))
    g.db.commit()

    return json.dumps(request.json)


def connect_db():
    return sqlite3.connect(DATABASE)


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def create_db():
    conn = connect_db()
    with conn:
        c = conn.cursor()
        c.executescript("""
            DROP TABLE IF EXISTS numbers;
            CREATE TABLE numbers (id integer primary key, n int, fib int);
            INSERT INTO numbers VALUES (1, 1, 1);
            INSERT INTO numbers VALUES (2, 2, 1);
            INSERT INTO numbers VALUES (3, 3, 2);
            INSERT INTO numbers VALUES (4, 4, 3);
            INSERT INTO numbers VALUES (5, 5, 5);
            """)
        conn.commit()

    print " * Database created\n" + "-" * 30


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
