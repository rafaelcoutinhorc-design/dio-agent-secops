# Evidência: resposta de um chat genérico

Mesma pergunta feita ao **mesmo modelo**, sem `AGENTS.md`, persona, skills nem base de conhecimento, e sem acesso aos arquivos do projeto: só o código colado na mensagem.

```
Analise a segurança deste código: [conteúdo do lab/app.py]
```

A resposta está sem edição, com duas exceções marcadas entre colchetes: o nome de um produto comercial de nuvem e o nome de uma empresa foram omitidos, para manter o projeto neutro em fornecedores e sem dados corporativos. Print: `03-chat-generico.png`.

---

## Revisão de segurança: app Flask de laboratório

O código reúne quase todas as classes de vulnerabilidade do OWASP Top 10. **Quatro falhas permitem execução remota de código (RCE)** sem autenticação. Rodar apenas em `127.0.0.1` reduz a exposição, mas não elimina o risco. Outros processos locais, malware e ataques de DNS rebinding a partir do navegador ainda conseguem chegar à aplicação.

> Lembrete: mesmo em laboratório, cole em ferramentas de IA apenas código com segredos fictícios, como neste caso. Nunca inclua credenciais, tokens ou dados reais. Esta análise é uma recomendação e deve ser revisada e validada antes de qualquer uso.

---

## Resumo das falhas

| # | Severidade | Onde | Vulnerabilidade | CWE |
|---|---|---|---|---|
| 1 | Crítica | `/profile` | Desserialização insegura (`pickle.loads` de cookie), que permite RCE | CWE-502 |
| 2 | Crítica | `/ping` | Injeção de comando no sistema operacional (`os.popen` com concatenação) | CWE-78 |
| 3 | Crítica | `/hello` | Server-Side Template Injection (SSTI) no Jinja2, que permite RCE (e também XSS) | CWE-1336 / CWE-79 |
| 4 | Crítica | `/login` | SQL Injection (f-string na query), que permite burlar a autenticação | CWE-89 |
| 5 | Alta | `/download` | Path traversal: leitura de qualquer arquivo | CWE-22 |
| 6 | Alta | `/admin/users` | Endpoint administrativo sem autenticação nem autorização, que expõe os hashes | CWE-306 / CWE-862 |
| 7 | Alta | `/login` | Backdoor: qualquer usuário com a senha `admin123` vira admin | CWE-798 |
| 8 | Alta | global | Segredos fixos no código (`secret_key`, `ADMIN_PASSWORD`) | CWE-798 |
| 9 | Alta | `init_db` / `login` | Senhas guardadas com MD5 sem salt | CWE-916 / CWE-327 |
| 10 | Alta | `login` | Senha em texto claro gravada no log | CWE-532 |
| 11 | Alta | `login` / `profile` | Cookie de sessão sem assinatura (dá para alterar o `role`) e sem `HttpOnly`, `Secure` e `SameSite` | CWE-565 / CWE-1004 |
| 12 | Alta | `app.run` | `debug=True`: o debugger do Werkzeug dá um console Python interativo e vaza stack traces | CWE-489 / CWE-215 |
| 13 | Média | `/profile`, `/ping` | XSS refletido: dados do cookie e saída do comando vão para o HTML sem escape | CWE-79 |
| 14 | Média | `/ping` | Uso como SSRF ou varredura da rede interna | CWE-918 |
| 15 | Média | `/login` | Sem limite de tentativas nem bloqueio (força bruta) e sem proteção CSRF | CWE-307 / CWE-352 |
| 16 | Baixa | `/login` | Comparação de senha que não é em tempo constante (timing) | CWE-208 |
| 17 | Baixa | `/login` | Injeção de log (quebras de linha no `username`) | CWE-117 |
| 18 | Baixa | sessão | Sessão sem expiração e sem logout ou invalidação | CWE-613 |

---

## Detalhamento e correções

### 1. Desserialização insegura com `pickle` (crítica)
```python
data = pickle.loads(base64.b64decode(raw))
```
O cookie é controlado pelo cliente. `pickle` executa código durante a desserialização (por meio do método `__reduce__`), então quem montar um cookie malicioso executa comandos no servidor.

**Correção:** nunca use `pickle` com dados que não são confiáveis. Use a `session` nativa do Flask, que é assinada com HMAC, ou JSON assinado (`itsdangerous`).

### 2. Injeção de comando em `/ping` (crítica)
```python
os.popen("ping -c 1 " + host)
```
Um `host` como `127.0.0.1; <comando>` (ou `&` / `|` no Windows) executa um comando qualquer.

**Correção:** valide a entrada como IP ou hostname (`ipaddress.ip_address`, ou uma regex restrita para hostname) e use `subprocess.run([...], shell=False, timeout=...)` com a lista de argumentos. Melhor ainda: remova a funcionalidade se ela não for necessária.

### 3. SSTI em `/hello` (crítica)
```python
render_template_string("<h1>Olá, " + name + "!</h1>")
```
A entrada vira parte do template. Expressões como `{{ 7*7 }}` são avaliadas, e a partir delas é possível chegar a objetos Python e executar código.

**Correção:** passe a entrada como variável. O autoescape cuida do XSS:
```python
render_template_string("<h1>Olá, {{ name }}!</h1>", name=name)
```

### 4. SQL Injection em `/login` (crítica)
```python
f"... WHERE username = '{username}' AND password = '{pwd_hash}'"
```
Um `username` como `aluno' --` comenta a checagem de senha e autentica sem credencial.

**Correção:** use uma query parametrizada (o próprio `init_db` já faz isso):
```python
conn.execute("SELECT username, role, password FROM users WHERE username = ?", (username,))
```

### 5. Path traversal em `/download` (alta)
`os.path.join(FILES_DIR, "../app.py")` sai do diretório. Com um caminho absoluto (`/etc/passwd`, `C:\...`), o `join` descarta o `FILES_DIR` de vez.

**Correção:** use `send_from_directory(FILES_DIR, filename)`, que usa `safe_join`. Se possível, combine com uma allowlist de nomes ou IDs.

### 6. `/admin/users` sem controle de acesso (alta)
Qualquer pessoa lista usuários, hashes e papéis.

**Correção:** exija sessão autenticada com `role == "admin"` (por exemplo, com um decorator) e **nunca** devolva hashes de senha na resposta.

### 7 e 8. Credencial e segredo fixos no código, com backdoor (alta)
`if row or password == ADMIN_PASSWORD` concede admin para **qualquer** `username`. Além disso, os segredos ficam no repositório.

**Correção:** remova o atalho e trate o admin como um usuário comum do banco, com hash forte. Carregue `SECRET_KEY` de variável de ambiente ou de um cofre de segredos (Vault, [produto de nuvem omitido]) e gere o valor com `secrets.token_hex(32)`. Se o segredo já foi versionado, faça a rotação.

### 9. MD5 sem salt (alta)
MD5 é rápido e sem salt, o que facilita rainbow tables e força bruta em GPU.

**Correção:** use `argon2-cffi`, `bcrypt` ou `werkzeug.security.generate_password_hash` / `check_password_hash` (scrypt ou PBKDF2 com salt). A verificação de hash dessas bibliotecas já é feita em tempo constante.

### 10 e 17. Logs (alta e baixa)
`logging.info("... %s / %s", username, password)` grava a senha em claro.

**Correção:** nunca registre senhas. Registre só o usuário (já sanitizado, sem `\r` e `\n`), o resultado da tentativa e o IP. Proteja e rotacione o arquivo de log.

### 11. Cookie de sessão sem assinatura e sem flags (alta)
Mesmo sem o `pickle`, base64 não é proteção: o cliente pode trocar `role` para `admin`.

**Correção:** use `flask.session` com:
```python
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,      # quando houver HTTPS
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
)
```
Chame `session.clear()` no login para evitar session fixation e também no logout.

### 12. `debug=True` (alta)
O debugger do Werkzeug abre um console Python no navegador quando ocorre uma exceção. O PIN existe, mas é uma proteção fraca. O modo debug também vaza código e caminhos nos stack traces.

**Correção:** use `debug=False` e controle o modo por variável de ambiente. Em produção, rode com Gunicorn ou Waitress atrás de um proxy reverso.

### 13. XSS refletido (média)
`f"Olá, {data['user']}"` e `f"<pre>{output}</pre>"` devolvem HTML sem escape.

**Correção:** use `markupsafe.escape()` ou templates com autoescape.

### 14. SSRF ou varredura via `/ping` (média)
Mesmo corrigida a injeção, o endpoint permite sondar hosts internos.

**Correção:** use uma allowlist de destinos ou remova o endpoint.

### 15. Força bruta e CSRF (média)
**Correção:** aplique limite de tentativas (`Flask-Limiter`), bloqueio progressivo e tokens CSRF (`Flask-WTF`). Use mensagens de erro genéricas, que o código já tem.

---

## Esboço corrigido dos trechos principais

```python
import os, ipaddress, subprocess, logging, sqlite3
from datetime import timedelta
from functools import wraps
from flask import Flask, request, session, render_template_string, send_from_directory, abort
from markupsafe import escape
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                  PERMANENT_SESSION_LIFETIME=timedelta(minutes=30))

def require_role(role):
    def deco(f):
        @wraps(f)
        def wrapper(*a, **kw):
            if session.get("role") != role:
                abort(403)
            return f(*a, **kw)
        return wrapper
    return deco

@app.post("/login")
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    with sqlite3.connect(DB) as conn:
        row = conn.execute("SELECT username, role, password FROM users WHERE username = ?",
                           (username,)).fetchone()
    if row and check_password_hash(row[2], password):
        session.clear()
        session.update(user=row[0], role=row[1])
        logging.info("Login OK: %r", username)
        return "Login OK"
    logging.warning("Falha de login: %r", username)
    return "Usuário ou senha inválidos", 401

@app.get("/profile")
def profile():
    return f"Olá, {escape(session.get('user', 'anônimo'))}"

@app.get("/hello")
def hello():
    return render_template_string("<h1>Olá, {{ name }}!</h1>",
                                  name=request.args.get("name", "visitante"))

@app.get("/ping")
def ping():
    try:
        ip = str(ipaddress.ip_address(request.args.get("host", "127.0.0.1")))
    except ValueError:
        abort(400)
    flag = "-n" if os.name == "nt" else "-c"
    out = subprocess.run(["ping", flag, "1", ip], capture_output=True, text=True,
                         timeout=5, shell=False).stdout
    return f"<pre>{escape(out)}</pre>"

@app.get("/download")
def download():
    return send_from_directory(FILES_DIR, request.args.get("file", "boas-vindas.txt"))

@app.get("/admin/users")
@require_role("admin")
def admin_users():
    with sqlite3.connect(DB) as conn:
        users = conn.execute("SELECT username, role FROM users").fetchall()
    return {"users": users}

if __name__ == "__main__":
    init_db()  # gravar senhas com generate_password_hash, não MD5
    app.run(host="127.0.0.1", port=5000, debug=False)
```

---

## Prioridade de correção
1. **Imediato (RCE):** `pickle` (1), injeção de comando (2), SSTI (3), `debug=True` (12).
2. **Autenticação e acesso:** SQL Injection (4), backdoor `admin123` (7), `/admin/users` (6), cookie sem assinatura (11).
3. **Dados:** path traversal (5), MD5 (9), senha no log (10), segredos fixos (8).
4. **Endurecimento:** XSS, SSRF, rate limiting, CSRF, expiração de sessão e cabeçalhos de segurança (`Content-Security-Policy`, `X-Content-Type-Options`).

**Ferramentas recomendadas para automatizar:** `bandit` (SAST para Python, que detecta `pickle`, `os.popen`, MD5, `debug=True` e SQL montado com string), `semgrep` (regras para Flask), `pip-audit` (dependências) e `gitleaks` (segredos no repositório).

Antes de aplicar qualquer correção em um sistema real [da empresa — nome omitido], valide com a área de Segurança da Informação.
