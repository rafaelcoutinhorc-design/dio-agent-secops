"""
App de LABORATÓRIO, propositalmente vulnerável.

Serve para o DIO Agent SecOps Expert demonstrar a skill secure-code-review.
NÃO use em produção, NÃO exponha na rede e NÃO reaproveite trechos deste código.
Roda apenas em 127.0.0.1. Todos os segredos abaixo são fictícios.
"""
import hashlib
import logging
import os
import pickle
import base64
import sqlite3

from flask import Flask, request, render_template_string, send_file, make_response

app = Flask(__name__)
app.secret_key = "lab-secret-nao-use-em-producao"  # segredo fixo no código
ADMIN_PASSWORD = "admin123"                        # credencial fixa no código

logging.basicConfig(filename="lab.log", level=logging.INFO)
DB = os.path.join(os.path.dirname(__file__), "lab.db")
FILES_DIR = os.path.join(os.path.dirname(__file__), "files")


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")
    conn.execute("DELETE FROM users")
    conn.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        ("aluno", hashlib.md5(b"aluno123").hexdigest(), "user"),
    )
    conn.commit()
    conn.close()
    os.makedirs(FILES_DIR, exist_ok=True)
    with open(os.path.join(FILES_DIR, "boas-vindas.txt"), "w", encoding="utf-8") as f:
        f.write("Arquivo de exemplo do laboratório.\n")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    logging.info("Tentativa de login: %s / %s", username, password)

    pwd_hash = hashlib.md5(password.encode()).hexdigest()
    conn = sqlite3.connect(DB)
    query = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{pwd_hash}'"
    row = conn.execute(query).fetchone()
    conn.close()

    if row or password == ADMIN_PASSWORD:
        session_data = {"user": row[0] if row else "admin", "role": row[1] if row else "admin"}
        resp = make_response("Login OK")
        resp.set_cookie("session_data", base64.b64encode(pickle.dumps(session_data)).decode())
        return resp
    return "Usuário ou senha inválidos", 401


@app.route("/profile")
def profile():
    raw = request.cookies.get("session_data", "")
    data = pickle.loads(base64.b64decode(raw)) if raw else {"user": "anônimo"}
    return f"Olá, {data['user']}"


@app.route("/hello")
def hello():
    name = request.args.get("name", "visitante")
    return render_template_string("<h1>Olá, " + name + "!</h1>")


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    output = os.popen("ping -n 1 " + host if os.name == "nt" else "ping -c 1 " + host).read()
    return f"<pre>{output}</pre>"


@app.route("/download")
def download():
    filename = request.args.get("file", "boas-vindas.txt")
    return send_file(os.path.join(FILES_DIR, filename))


@app.route("/admin/users")
def admin_users():
    conn = sqlite3.connect(DB)
    users = conn.execute("SELECT username, password, role FROM users").fetchall()
    conn.close()
    return {"users": users}


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
