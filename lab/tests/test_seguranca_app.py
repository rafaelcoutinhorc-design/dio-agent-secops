"""
Testes de segurança do lab/app.py (skill security-testing).

Cada teste afirma o comportamento SEGURO esperado. Com o app vulnerável, eles
FALHAM: isso prova a vulnerabilidade. Depois da correção, eles PASSAM: isso prova
o controle. Usam o cliente de teste do Flask, sem abrir porta de rede, e só
entradas inofensivas.

Rodar (dentro de lab/, com o ambiente virtual ativo):
    pip install -r requirements.txt -r requirements-test.txt
    pytest tests -v
"""
import base64
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app as lab  # noqa: E402

MARCADOR = "SECOPS_MARCADOR_7f3a"


@pytest.fixture()
def client():
    lab.init_db()
    lab.app.config["TESTING"] = True
    with lab.app.test_client() as c:
        yield c


def test_ping_nao_executa_segundo_comando(client):
    # CWE-78: o separador "|" funciona em sh e cmd; o echo é inofensivo.
    resp = client.get("/ping", query_string={"host": f"127.0.0.1 | echo {MARCADOR}"})
    assert MARCADOR not in resp.get_data(as_text=True)


def test_hello_nao_avalia_template(client):
    # CWE-1336: se o nome for avaliado como template, {{7*7}} vira 49.
    resp = client.get("/hello", query_string={"name": "{{7*7}}"})
    assert "49" not in resp.get_data(as_text=True)


def test_login_nao_aceita_sql_injection(client):
    # CWE-89: comentar o resto da consulta não pode burlar a senha.
    resp = client.post("/login", data={"username": "aluno' --", "password": "senha-errada"})
    assert resp.status_code == 401


def test_login_nao_aceita_senha_fixa_de_admin(client):
    # CWE-798: a senha fixa no código não pode abrir o perfil admin.
    resp = client.post("/login", data={"username": "qualquer", "password": "admin123"})
    assert resp.status_code == 401


def test_cookie_de_sessao_nao_usa_pickle(client):
    # CWE-502: um cookie em pickle começa com o byte 0x80 depois do base64.
    resp = client.post("/login", data={"username": "aluno", "password": "aluno123"})
    cookie = resp.headers.get("Set-Cookie", "")
    if "session_data=" in cookie:
        valor = cookie.split("session_data=", 1)[1].split(";", 1)[0]
        assert not base64.b64decode(valor).startswith(b"\x80")


def test_download_bloqueia_path_traversal(client):
    # CWE-22: subir de diretório não pode ler o código do app.
    resp = client.get("/download", query_string={"file": "../app.py"})
    assert resp.status_code in (400, 403, 404)


def test_admin_users_exige_autenticacao(client):
    # CWE-862: rota administrativa sem sessão deve negar acesso.
    resp = client.get("/admin/users")
    assert resp.status_code in (401, 403)


def test_senhas_nao_usam_md5():
    # CWE-916: o hash guardado não pode ser MD5 (32 caracteres hexadecimais).
    import sqlite3

    lab.init_db()
    conn = sqlite3.connect(lab.DB)
    (pwd,) = conn.execute("SELECT password FROM users WHERE username = 'aluno'").fetchone()
    conn.close()
    assert not (len(pwd) == 32 and all(c in "0123456789abcdef" for c in pwd))
