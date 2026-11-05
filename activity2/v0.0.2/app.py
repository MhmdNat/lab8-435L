#!/usr/bin/python
import sqlite3
from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file
import os

# path of the SQLite file; can be overridden (the tests point it at a temp file)
DB_PATH = os.environ.get('USERS_DB_PATH', 'database.db')

# users inserted into the database the first time the app runs
DEFAULT_USERS = [
    {
        "name": "John Doe",
        "email": "jondoe@gamil.com",
        "phone": "067765434567",
        "address": "John Doe Street, Innsbruck",
        "country": "Austria"
    },
    {
        "name": "Jane Smith",
        "email": "janesmith@gmail.com",
        "phone": "0161234567",
        "address": "Baker Street, London",
        "country": "United Kingdom"
    },
    {
        "name": "Ali Hassan",
        "email": "alihassan@gmail.com",
        "phone": "70123456",
        "address": "Hamra Street, Beirut",
        "country": "Lebanon"
    },
]

def connect_to_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_db_table():
    conn = None
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')

        # first run: fill the new table with the default users
        conn.executemany(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            [(u['name'], u['email'], u['phone'], u['address'], u['country']) for u in DEFAULT_USERS]
        )
        conn.commit()
        print("User table created successfully")
    except:
        print("User table creation failed - Maybe table")
    finally:
        if conn:
            conn.close()

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)", (user['name'], user['email'], user['phone'], user['address'], user['country']) )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except:
        conn.rollback()

    finally:
        conn.close()

    return inserted_user

def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)

    except:
        users = []
    finally:
        conn.close()

    return users


def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]

    except:
        user = {}
    finally:
        conn.close()

    return user

def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id =?", (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"],))
        conn.commit()
        #return the user
        updated_user = get_user_by_id(user["user_id"])

    except:
        conn.rollback()
        updated_user = {}
    finally:
        conn.close()

    return updated_user

def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()

    return message

create_db_table()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route('/api/users/add', methods = ['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/update', methods = ['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

@app.route('/api/users/delete/<user_id>', methods = ['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))

def get_user_names():
    names = []
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users")
        names = [row[0] for row in cur.fetchall()]
    except:
        names = []
    finally:
        if conn:
            conn.close()

    return names

# Lab 8 v0.0.2: list of the names of all users in the database
@app.route('/get_users', methods=['GET'])
def api_get_user_names():
    return jsonify(get_user_names())

if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    # 0.0.0.0 so the API can be reached from outside the Docker container
    app.run(host='0.0.0.0', port=3000) #run app
