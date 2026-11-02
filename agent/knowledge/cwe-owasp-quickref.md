# CWE e OWASP Top 10 — referência rápida

- **CWE** (https://cwe.mitre.org): catálogo de tipos de fraqueza de software.
- **OWASP Top 10:2021** (https://owasp.org/Top10): as 10 categorias de risco mais comuns em aplicações web. Se o estudante citar uma edição mais nova, confirme com a skill de pesquisa na web.

## Código

| Fraqueza | CWE | OWASP 2021 | Correção típica (Python/Flask) | NIST CSF | CIS |
|----------|-----|-----------|--------------------------------|----------|-----|
| SQL Injection | CWE-89 | A03 Injection | Consultas parametrizadas (`?`) ou ORM | PR.PS | 16 |
| OS Command Injection | CWE-78 | A03 Injection | `subprocess.run([...], shell=False)` + validação por lista permitida | PR.PS | 16 |
| XSS / SSTI | CWE-79 / CWE-1336 | A03 Injection | `render_template` com autoescape; nunca montar template com entrada do usuário | PR.PS | 16 |
| Path Traversal | CWE-22 | A01 Broken Access Control | `send_from_directory` + `secure_filename` | PR.AA | 16 |
| Falta de autorização | CWE-862 | A01 Broken Access Control | Verificar sessão e perfil em cada rota | PR.AA | 6 |
| Credenciais no código | CWE-798 | A07 Identification and Authentication Failures | Variáveis de ambiente ou cofre de segredos | PR.AA | 16 |
| Hash fraco de senha | CWE-916 / CWE-327 | A02 Cryptographic Failures | `werkzeug.security.generate_password_hash` (scrypt/pbkdf2), argon2 ou bcrypt | PR.DS | 3 |
| Deserialização insegura | CWE-502 | A08 Software and Data Integrity Failures | JSON em vez de `pickle`; assinar dados | PR.PS | 16 |
| Debug em produção | CWE-489 / CWE-215 | A05 Security Misconfiguration | `debug=False`, configuração por ambiente | PR.PS | 4 |
| Senha em log | CWE-532 | A09 Security Logging and Monitoring Failures | Nunca logar segredos; mascarar | PR.DS, DE.CM | 3, 8 |
| Sem limite de tentativas | CWE-307 | A07 | Rate limiting, bloqueio progressivo, MFA | PR.AA | 6 |
| Dependência vulnerável | CWE-1104 | A06 Vulnerable and Outdated Components | Fixar versões, `pip-audit`, atualização automatizada de dependências | ID.RA | 7 |

## Configuração e infraestrutura

| Fraqueza | CWE | OWASP 2021 | Correção típica | NIST CSF | CIS |
|----------|-----|-----------|-----------------|----------|-----|
| Container privilegiado / socket do runtime montado | CWE-250 | A05 | Remover `privileged`, não montar o socket, usuário não-root | PR.PS | 4 |
| Serviço exposto em `0.0.0.0` sem necessidade | CWE-668 | A05 | Publicar só a porta necessária, em interface interna | PR.IR | 12 |
| Senha padrão ou em texto claro na configuração | CWE-798 / CWE-521 | A07 | Segredo injetado em tempo de execução, senha forte | PR.AA | 5 |
| Imagem ou pacote sem versão fixa (`latest`) | CWE-1104 | A06 | Fixar versão ou digest | ID.RA | 2, 7 |
| TLS antigo (1.0/1.1) ou cifras fracas | CWE-327 | A02 | Só TLS 1.2+ | PR.DS | 12 |
| Listagem de diretório / versão do servidor exposta | CWE-548 / CWE-200 | A05 | Desligar `autoindex` e banner de versão | PR.PS | 4 |
| Cabeçalhos de segurança ausentes | CWE-693 | A05 | CSP, `X-Content-Type-Options`, `X-Frame-Options`, HSTS | PR.PS | 16 |
| SSH com login root ou senha | CWE-250 / CWE-307 | A07 | `PermitRootLogin no`, só chave, `MaxAuthTries` baixo | PR.AA | 5, 6 |
| Senha vazia permitida | CWE-258 | A07 | `PermitEmptyPasswords no` | PR.AA | 5 |

## Severidade

Use a matriz de `risk-scoring.md` (impacto × probabilidade). O mesmo SQLi pode ser Crítico numa API exposta à internet com dados pessoais e Médio num script local de laboratório. Sempre explique o porquê da nota.
