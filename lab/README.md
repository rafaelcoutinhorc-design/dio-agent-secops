# Laboratório

Material de laboratório **próprio** para testar o DIO Agent SecOps Expert. Nada aqui deve ser apontado para sistemas de terceiros. Todas as senhas e chaves citadas são fictícias.

| Arquivo | Cenário | Para que serve |
|---------|---------|----------------|
| `app.py` | Código | API Flask **propositalmente vulnerável** (SQLi, command injection, SSTI, path traversal, pickle, segredos fixos, MD5, debug ligado, senha em log, rota admin sem autenticação). Alvo da skill `secure-code-review`. |
| `config/docker-compose.yml` | Configuração insegura | Containers com `privileged`, root, socket do runtime montado, portas abertas, senhas padrão e imagens `latest`. |
| `config/nginx.conf` | Configuração insegura | Proxy reverso com TLS antigo, listagem de diretório, versão exposta, `/admin` e `/backup` publicados. |
| `infra/sshd_config` | Infraestrutura | Servidor SSH com login root, senha vazia permitida, muitas tentativas, cifras fracas e log desligado. |
| `tests/test_seguranca_app.py` | Testes | Testes de segurança que **falham hoje** (provam as falhas) e **passam depois da correção**. Skill `security-testing`. |
| `hunting/*.yml` | Detecção | Regras **Sigma** (formato aberto) que detectam a exploração do `app.py`. Skill `threat-hunting`. |
| `requirements.txt` / `requirements-test.txt` | — | Dependências do app e dos testes. |

## Como rodar (opcional)

A análise do agente é estática e não exige rodar nada. Para rodar os testes de segurança:

```bash
cd lab
python -m venv .venv
.venv\Scripts\activate        # (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt -r requirements-test.txt
pytest tests -v               # hoje: todos falham, provando as vulnerabilidades
```

Para subir o app e validar as regras Sigma:

```bash
python app.py                 # sobe em http://127.0.0.1:5000
```

Converta as regras para o seu SIEM de laboratório com a ferramenta aberta `sigma-cli` (`sigma convert -t <alvo> hunting/*.yml`).

O servidor escuta só em `127.0.0.1`. Desligue com `Ctrl+C` e apague a pasta `.venv`, `lab.db` e `lab.log` ao terminar. Os arquivos de `config/` e `infra/` são só para análise: **não** os aplique em nenhum servidor.

> ⚠️ Use apenas em máquina de laboratório sua. Não rode em máquina corporativa sem autorização da equipe de Segurança da Informação: as ferramentas de monitoramento podem (e devem) alertar.
