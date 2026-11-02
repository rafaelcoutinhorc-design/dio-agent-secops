---
name: secure-code-review
description: Use quando o estudante pedir para analisar um código (ex. lab/app.py) em busca de vulnerabilidades. Faz perguntas de contexto, aponta achados com CWE e severidade, propõe correção, detecção no Microsoft Defender (KQL) e o controle ISO 27001 / NIST CSF correspondente.
---

# Skill: Revisão de código seguro

Revisa código com o olhar de AppSec + SOC + GRC: cada vulnerabilidade vira **correção**, **detecção** e **controle**.

## Quando usar

O estudante cola um código, aponta um arquivo (ex.: `lab/app.py`) ou pergunta "esse código é seguro?". Se o pedido for só sobre KQL, use `defender-threat-hunting`; se for só sobre norma, use `compliance-mapping`.

## Processo

### 1. Confirme que é laboratório

Se não estiver claro, pergunte se o código é do próprio estudante e se roda em ambiente de laboratório. Código de terceiros sem autorização: recuse a análise ofensiva e ofereça ensinar o conceito.

### 2. Perguntas de contexto (uma por vez)

Faça no máximo 4, nesta ordem, e pule as que o código já responde:

1. **Exposição:** onde isso roda? (só `localhost`, rede interna, internet)
2. **Dados:** que dados passam por aqui? (pessoais/LGPD, financeiros, credenciais, nenhum sensível)
3. **Usuários:** quem acessa? (anônimos, usuários logados, só admins)
4. **Monitoramento:** o host tem Microsoft Defender for Endpoint? Há meta de ISO 27001 ou NIST?

Se o estudante disser "pode seguir", registre as suposições em uma linha (ex.: "Suponho: exposto à internet, dados pessoais, sem Defender") e continue.

### 3. Leia o código inteiro

Leia o arquivo completo antes de opinar. Procure, no mínimo: injeções (SQL, comando, template), autenticação e autorização, segredos no código, criptografia, deserialização, manipulação de arquivos, configuração (debug, bind de rede) e logging. Em apps web, inclua o hardening HTTP: flags de cookie (`HttpOnly`, `Secure`, `SameSite`), proteção CSRF, cabeçalhos de segurança (CSP, `X-Content-Type-Options`) e escape de saída. Use `agent/knowledge/cwe-owasp-quickref.md`.

### 4. Entregue a tabela de achados

Ordene por severidade. Uma linha por achado:

| # | Local | Achado | CWE | Severidade (contexto) | ISO 27001 | NIST CSF |
|---|-------|--------|-----|-----------------------|-----------|----------|

Severidade: Crítica, Alta, Média ou Baixa, sempre ajustada ao contexto do passo 2, com uma frase de justificativa.

### 5. Detalhe os 3 mais graves

Para cada um:

- **Por que é vulnerável** (em linguagem simples) e **o que um atacante conseguiria** (impacto, sem exploit pronto).
- **Correção:** trecho curto do código corrigido.
- **Detecção:** uma consulta KQL de Advanced Hunting que pegaria a exploração no host, ou o log que a aplicação deveria gerar. Siga `agent/knowledge/defender-xdr-hunting.md`.
- **Evidência para auditoria:** o que provaria que o controle está implementado (ex.: PR com a correção + teste automatizado + regra de detecção ativa).

### 6. Plano de ação

Feche com no máximo 5 ações priorizadas: **agora** (crítico), **esta sprint**, **processo** (ex.: SAST no pipeline, revisão de código obrigatória — ISO 8.25/8.29, SSDF PW.7).

### 7. Verifique o entendimento

Proponha um exercício: "Corrija o achado #1 e me mostre o diff" ou "Explique para um gestor, em 2 frases, o risco do achado #2".

## Lembre-se

- Não invente linha nem CWE: cite o que está no código.
- Explique a exploração no nível conceitual; nada de payload pronto para uso contra terceiros.
- Um achado sem correção nem detecção está incompleto.
- Não chame tudo de crítico.
