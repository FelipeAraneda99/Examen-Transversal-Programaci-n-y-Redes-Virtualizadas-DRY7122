
#!/usr/bin/env python3
# user_auth_hash.py - Puerto 5800

import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                  (username, hash_pw(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

@app.route('/')
def index():
    return '<h1>Sistema de Autenticacion con Hash</h1><p>Usuarios: Felipe Araneda, Angelo Boitano</p>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or request.form
    u = data.get('username')
    p = data.get('password')
    if not u or not p:
        return jsonify({"error": "Faltan datos"}), 400
    ok = add_user(u, p)
    return jsonify({"success": ok, "message": "Registrado" if ok else "Ya existe"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or request.form
    u = data.get('username')
    p = data.get('password')
    if not u or not p:
        return jsonify({"error": "Faltan datos"}), 400
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (u,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_pw(p):
        return jsonify({"success": True, "message": "Login exitoso"})
    return jsonify({"success": False, "message": "Credenciales invalidas"})

@app.route('/users', methods=['GET'])
def list_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, password_hash FROM users")
    users = [{"username": r[0], "hash": r[1]} for r in c.fetchall()]
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    init_db()
    # Registrar a los integrantes automaticamente
    for u, p in [("felipe.araneda", "pass123"), ("angelo.boitano", "pass456")]:
        if add_user(u, p):
            print(f"Usuario registrado: {u}")
    print("Servidor en https://0.0.0.0:5800")
    app.run(host='0.0.0.0', port=5800, ssl_context='adhoc', debug=False)
