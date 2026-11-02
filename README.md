# 🛡️ DIO Agent SecOps Expert

> Uma evolução do [DIO Agent](https://github.com/digitalinnovationone/dio-agent), especializada em **segurança defensiva**: revisão de código seguro, **threat hunting no Microsoft Defender XDR** e **governança com ISO/IEC 27001:2022 e NIST CSF 2.0**.

---

## 🎯 A especialização, e por quê

O DIO Agent original é um mentor de estudos generalista. Esta versão vira um **mentor de Blue Team + GRC**, que olha cada problema por três lentes:

| Lente | Pergunta | Ferramenta/referência |
|-------|----------|-----------------------|
| **AppSec** | Onde o código abre a porta? | OWASP Top 10, CWE |
| **SOC / Threat Hunting** | Como eu veria o ataque acontecendo? | Microsoft Defender XDR, KQL, MITRE ATT&CK |
| **GRC** | Qual controle prova que a porta está fechada? | ISO/IEC 27001:2022 (Anexo A), NIST CSF 2.0, NIST SSDF |

**Por quê:** no mercado essas competências costumam estar separadas. O dev corrige o bug mas não sabe qual controle atende; o analista de SOC detecta mas não conversa com auditoria; o time de compliance pede evidência mas não sabe gerá-la. Um achado só está completo quando tem **correção + detecção + controle**, e é isso que o agente entrega e ensina.

Um chat genérico responde "isso tem SQL injection". O SecOps Expert **pergunta o contexto primeiro** (exposição, dados, licença do Defender, meta de certificação), ajusta a severidade a ele e devolve a correção, a KQL de detecção e o controle ISO/NIST com a evidência que um auditor aceitaria.

---

## 🗂️ O que foi criado ou alterado

### Alterados

| Arquivo | Mudança |
|---------|---------|
| [`AGENTS.md`](AGENTS.md) | Nova identidade (SecOps Expert), nova base de conhecimento, 3 skills novas na tabela, regra "contexto antes de diagnóstico", formato obrigatório de achado e **limites éticos** (só laboratório, sem exploit pronto, sem evasão de EDR, sem dados sensíveis). |
| [`agent/persona.md`](agent/persona.md) | Persona de analista sênior de SOC que já passou por auditoria ISO 27001: valores de evidência, contexto e defesa ética. |
| [`README.md`](README.md) | Este arquivo. |

### Criados

| Tipo | Arquivo | O que tem |
|------|---------|-----------|
| **Skill** | [`skills/secure-code-review/SKILL.md`](skills/secure-code-review/SKILL.md) | Revisão de código com perguntas de contexto, tabela de achados (linha, CWE, severidade, ISO, NIST), correção, KQL e plano de ação. |
| **Skill** | [`skills/defender-threat-hunting/SKILL.md`](skills/defender-threat-hunting/SKILL.md) | Hunting guiado por hipótese no Defender XDR: KQL em camadas, validação em lab, promoção a custom detection. |
| **Skill** | [`skills/compliance-mapping/SKILL.md`](skills/compliance-mapping/SKILL.md) | Mapeamento de risco → ISO 27001 + NIST CSF, visão de auditor e evidências. |
| Conhecimento | [`agent/knowledge/iso27001-annex-a.md`](agent/knowledge/iso27001-annex-a.md) | Estrutura da norma, controles do Anexo A mais usados em achados técnicos, como o auditor avalia. |
| Conhecimento | [`agent/knowledge/nist-csf-ssdf.md`](agent/knowledge/nist-csf-ssdf.md) | NIST CSF 2.0 (6 funções e categorias), SSDF (SP 800-218), SP 800-61r3 e equivalência com a ISO. |
| Conhecimento | [`agent/knowledge/defender-xdr-hunting.md`](agent/knowledge/defender-xdr-hunting.md) | Tabelas e colunas do Advanced Hunting, boas práticas de KQL, licenças e técnicas ATT&CK. |
| Conhecimento | [`agent/knowledge/cwe-owasp-quickref.md`](agent/knowledge/cwe-owasp-quickref.md) | CWE × OWASP × correção × ISO × NIST, e critério de severidade. |
| Laboratório | [`lab/app.py`](lab/app.py) | API Flask **propositalmente vulnerável**, só em `127.0.0.1`, com segredos fictícios. Alvo da análise. |
| Laboratório | [`lab/hunting/`](lab/hunting/) | 2 consultas KQL que detectam a exploração do `app.py` no Defender. |
| Melhoria do harness | [`.claude/commands/`](.claude/commands/) e [`.claude/settings.json`](.claude/settings.json) | Ver abaixo. |
| Evidências | [`docs/evidencias/`](docs/evidencias/) | Análise do `app.py`, comparativo com chat genérico e prints. |

As skills originais do DIO Agent foram mantidas, e o [`CLAUDE.md`](CLAUDE.md) continua importando o `AGENTS.md`.

---

## 🚀 Como rodar no harness

1. Instale um harness compatível com `AGENTS.md` (testado no **Claude Code**; também funciona no Google Antigravity, Codex, OpenCode).
2. Clone o repositório e abra a pasta:

   ```bash
   git clone https://github.com/rafaelcoutinhorc-design/dio-agent-secops.git
   ```

   ```bash
   cd dio-agent-secops
   ```

   ```bash
   claude
   ```

3. Converse naturalmente ou use os comandos:

| Peça | O agente usa |
|------|--------------|
| "Analise a segurança do `lab/app.py`" ou `/analisar-codigo lab/app.py` | `secure-code-review` |
| "Como detecto command injection num app Python no Defender?" ou `/hunt T1059 a partir de python` | `defender-threat-hunting` |
| "Qual controle da ISO 27001 cobre senha em log?" ou `/mapear-controle senha em log` | `compliance-mapping` |

Rodar o `lab/app.py` é opcional (a análise é estática). Veja [`lab/README.md`](lab/README.md).

---

## 🔧 A melhoria escolhida no harness

**Comandos de atalho + guardrails de segurança no Claude Code.**

1. **Slash commands** em [`.claude/commands/`](.claude/commands/): `/analisar-codigo`, `/hunt` e `/mapear-controle` chamam direto a skill certa, com argumento. Isso padroniza a entrada e torna a demonstração reproduzível.
2. **Permissões** em [`.claude/settings.json`](.claude/settings.json), coerentes com a especialização:
   - **deny:** leitura de `.env`, chaves (`*.pem`, `*.key`) e pastas `secrets/`; ferramentas de rede/ataque (`curl`, `wget`, `nmap`, `sqlmap`, `hydra`). O agente de segurança **não consegue** vazar segredo nem atacar alvo externo, mesmo que alguém peça.
   - **ask:** `python` e `pip install` pedem confirmação antes de rodar.

É o princípio do menor privilégio (ISO 27001 8.2 / NIST CSF PR.AA) aplicado ao próprio agente.

---

## 📸 Evidências

| Evidência | Arquivo |
|-----------|---------|
| Perguntas de contexto que o agente faz | `docs/evidencias/01-perguntas-contexto.png` |
| Análise do `app.py` (tabela de achados) | `docs/evidencias/02-tabela-achados.png` |
| Mesma pergunta num chat genérico | `docs/evidencias/03-chat-generico.png` |
| Saída completa da análise | [`docs/evidencias/analise-app-py.md`](docs/evidencias/analise-app-py.md) |
| Resposta completa do chat genérico | [`docs/evidencias/resposta-chat-generico.md`](docs/evidencias/resposta-chat-generico.md) |
| Comparativo Expert × chat genérico | [`docs/evidencias/comparativo-chat-generico.md`](docs/evidencias/comparativo-chat-generico.md) |

![Perguntas de contexto](docs/evidencias/01-perguntas-contexto.png)
![Tabela de achados](docs/evidencias/02-tabela-achados.png)
![Chat genérico](docs/evidencias/03-chat-generico.png)

---

## ⚖️ Ética e escopo

- Todos os testes usam **apenas código e servidor próprios, de laboratório** (`lab/app.py` em `127.0.0.1`).
- Nenhum segredo, tenant, IP ou dado real está no repositório; as credenciais do `app.py` são fictícias.
- O texto da ISO/IEC 27001 é protegido por direitos autorais: a base de conhecimento usa títulos parafraseados. Consulte a norma oficial (ISO/ABNT) e as fontes públicas do NIST e do Microsoft Learn.
- O conteúdo gerado pelo agente é recomendação: decisões de risco e de conformidade são humanas.

---

## 🗂️ Estrutura

```
dio-agent-secops/
├── AGENTS.md                 Definição do agente (alterado)
├── CLAUDE.md                 Atalho para o Claude Code
├── .claude/
│   ├── commands/             /analisar-codigo, /hunt, /mapear-controle
│   └── settings.json         Guardrails de permissão
├── agent/
│   ├── persona.md            Persona SecOps (alterado)
│   └── knowledge/            ISO 27001, NIST, Defender XDR, CWE/OWASP + base DIO
├── skills/                   3 skills novas + skills originais
├── lab/
│   ├── app.py                App vulnerável de laboratório
│   └── hunting/              Consultas KQL
└── docs/
    ├── evidencias/           Prints, análise e comparativo
    ├── glossary.md
    └── youcom-mcp.md
```

Baseado em [digitalinnovationone/dio-agent](https://github.com/digitalinnovationone/dio-agent).
