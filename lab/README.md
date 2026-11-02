# Laboratório

Material de laboratório **próprio** para testar o DIO Agent SecOps Expert. Nada aqui deve ser apontado para sistemas de terceiros.

| Arquivo | Para que serve |
|---------|----------------|
| `app.py` | API Flask **propositalmente vulnerável** (SQLi, command injection, SSTI, path traversal, pickle, segredos fixos, MD5, debug ligado, senha em log, rota admin sem autenticação). Alvo da skill `secure-code-review`. |
| `requirements.txt` | Dependência do app. |
| `hunting/` | Consultas KQL de Advanced Hunting (Microsoft Defender XDR) que detectam a exploração do `app.py`. Usadas na skill `defender-threat-hunting`. |

## Como rodar (opcional)

A análise do agente é estática e não exige rodar o app. Se quiser validar as consultas KQL num dispositivo de laboratório com Defender for Endpoint:

```bash
cd lab
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python app.py                 # sobe em http://127.0.0.1:5000
```

O servidor escuta só em `127.0.0.1`. Desligue com `Ctrl+C` e apague a pasta `.venv`, `lab.db` e `lab.log` ao terminar.

> ⚠️ Use apenas em máquina de laboratório sua. Não rode em máquina corporativa sem autorização da equipe de Segurança da Informação: o Defender pode (e deve) alertar.
