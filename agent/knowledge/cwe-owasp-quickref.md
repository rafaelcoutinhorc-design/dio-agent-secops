# CWE e OWASP Top 10 — referência rápida

- **CWE** (https://cwe.mitre.org): catálogo de tipos de fraqueza de software.
- **OWASP Top 10:2021** (https://owasp.org/Top10): as 10 categorias de risco mais comuns em aplicações web. Se o estudante citar uma edição mais nova, confirme com a skill de pesquisa na web.

| Fraqueza | CWE | OWASP 2021 | Correção típica (Python/Flask) | ISO 27001 | NIST CSF |
|----------|-----|-----------|--------------------------------|-----------|----------|
| SQL Injection | CWE-89 | A03 Injection | Consultas parametrizadas (`?`) ou ORM | 8.28 | PR.PS |
| OS Command Injection | CWE-78 | A03 Injection | `subprocess.run([...], shell=False)` + validação por lista permitida | 8.28 | PR.PS |
| XSS / SSTI | CWE-79 / CWE-1336 | A03 Injection | `render_template` com autoescape; nunca montar template com entrada do usuário | 8.28 | PR.PS |
| Path Traversal | CWE-22 | A01 Broken Access Control | `send_from_directory` + `secure_filename` | 8.3 | PR.AA |
| Falta de autorização | CWE-862 | A01 Broken Access Control | Verificar sessão e perfil em cada rota | 5.15, 8.2 | PR.AA |
| Credenciais no código | CWE-798 | A07 Identification and Authentication Failures | Variáveis de ambiente / cofre (Key Vault) | 5.17, 8.4 | PR.AA |
| Hash fraco de senha | CWE-916 / CWE-327 | A02 Cryptographic Failures | `werkzeug.security.generate_password_hash` (scrypt/pbkdf2), argon2 ou bcrypt | 8.24 | PR.DS |
| Deserialização insegura | CWE-502 | A08 Software and Data Integrity Failures | JSON em vez de `pickle`; assinar dados | 8.28 | PR.PS |
| Debug em produção | CWE-489 / CWE-215 | A05 Security Misconfiguration | `debug=False`, configuração por ambiente | 8.9, 8.31 | PR.PS |
| Senha em log | CWE-532 | A09 Security Logging and Monitoring Failures | Nunca logar segredos; mascarar | 8.15, 8.11 | PR.DS, DE.CM |
| Sem limite de tentativas | CWE-307 | A07 | Rate limiting, bloqueio progressivo, MFA | 8.5 | PR.AA |
| Dependência vulnerável | CWE-1104 | A06 Vulnerable and Outdated Components | Fixar versões, `pip-audit`, Dependabot | 8.8 | ID.RA |

## Severidade

Use **CVSS v3.1** (ou v4.0) como referência e ajuste ao contexto: o mesmo SQLi é Crítico numa API exposta à internet com dados pessoais e Médio num script local de laboratório. Sempre explique o porquê da nota.
