---
name: secure-code-review
description: Use quando o estudante pedir para analisar código ou configuração (ex. lab/app.py, lab/config/, lab/infra/) ou uma alteração (diff) em busca de vulnerabilidades. Faz perguntas de contexto, classifica achados por impacto × probabilidade, propõe correção, detecção (regra Sigma ou log) e o controle NIST CSF / CIS correspondente.
---

# Skill: Revisão de código e configuração seguros

Revisa código e configuração com o olhar de AppSec + detecção + governança: cada vulnerabilidade vira **correção**, **detecção** e **controle**, sempre no formato padrão de `agent/knowledge/risk-scoring.md`.

## Quando usar

O estudante cola um código ou arquivo de configuração, aponta um arquivo (ex.: `lab/app.py`, `lab/config/docker-compose.yml`, `lab/infra/sshd_config`), pede para revisar uma alteração (`/revisar-alteracao`) ou pergunta "isso é seguro?". Se o pedido for só sobre detecção, use `threat-hunting`; se for só sobre framework, use `compliance-mapping`; se for para provar a falha com teste, use `security-testing`.

## Processo

### 1. Confirme que é laboratório

Se não estiver claro, pergunte se o código é do próprio estudante e se roda em ambiente de laboratório. Código de terceiros sem autorização: recuse a análise ofensiva e ofereça ensinar o conceito.

### 2. Perguntas de contexto (uma por vez)

Faça no máximo 4, nesta ordem, e pule as que o arquivo já responde:

1. **Exposição:** onde isso roda? (só `localhost`, rede interna, internet)
2. **Dados:** que dados passam por aqui? (pessoais/LGPD, financeiros, credenciais, nenhum sensível)
3. **Usuários:** quem acessa? (anônimos, usuários logados, só admins)
4. **Monitoramento e meta:** que telemetria existe (log da aplicação, log do servidor web, criação de processos, SIEM que aceita regras Sigma)? Há meta de adequação a algum framework (NIST CSF, CIS Controls)?

Se o estudante disser "pode seguir", registre as suposições em uma linha (ex.: "Suponho: internet, anônimos, credenciais, só log da aplicação, meta NIST CSF") e continue.

### 3. Leia o arquivo inteiro

Leia tudo antes de opinar. Use `agent/knowledge/cwe-owasp-quickref.md`.

- **Código:** injeções (SQL, comando, template), autenticação e autorização, segredos no código, criptografia, deserialização, manipulação de arquivos, configuração (debug, bind de rede) e logging. Em apps web, inclua o hardening HTTP: flags de cookie (`HttpOnly`, `Secure`, `SameSite`), proteção CSRF, cabeçalhos de segurança (CSP, `X-Content-Type-Options`) e escape de saída. Confira também SSRF (o servidor fazendo requisições para destinos escolhidos pelo usuário), comparação de segredos sem tempo constante e injeção de log (quebras de linha da entrada indo para o log).
- **Configuração e infraestrutura:** privilégios (root, `privileged`, socket do runtime), portas e interfaces expostas, senhas padrão ou em texto claro, versões não fixadas, TLS, listagem de diretório, banners de versão, autenticação remota (SSH), limites de recursos e de tentativas.

### 4. Entregue a tabela de achados (formato padrão)

Use exatamente a tabela de `agent/knowledge/risk-scoring.md`, ordenada pelo risco:

| # | Local | Achado | CWE | Impacto | Prob. | Risco (I×P) | Severidade | NIST CSF | CIS |
|---|-------|--------|-----|---------|-------|-------------|------------|----------|-----|

Abaixo da tabela, justifique em uma frase as notas que não forem óbvias e diga como a severidade mudaria em outro contexto.

### 5. Detalhe os 3 de maior risco

Para cada um:

- **Por que é vulnerável** (em linguagem simples) e **o que um atacante conseguiria** (impacto, sem exploit pronto).
- **Correção:** trecho curto do código ou da configuração corrigidos.
- **Detecção:** uma regra Sigma que pegaria a exploração, ou o log que a aplicação deveria gerar. Siga `agent/knowledge/threat-hunting-sigma.md` e reaproveite `lab/hunting/` quando couber.
- **Evidência:** o que provaria que o controle está implementado (ex.: commit com a correção + teste automatizado + regra Sigma versionada e ativa).

### 6. Plano de ação

Feche com no máximo 5 ações priorizadas: **agora** (crítico), **esta sprint**, **processo** (ex.: SAST e busca de segredos no pipeline, revisão obrigatória de alterações — NIST SSDF PW.7, CIS Controls 16).

### 7. Verifique o entendimento

Proponha um exercício: "Corrija o achado #1 e me mostre o diff" ou "Explique para um gestor, em 2 frases, o risco do achado #2".

## Modo alteração (DevSecOps)

Quando a entrada for um **diff** (comando `/revisar-alteracao`):

1. Analise só as linhas adicionadas ou alteradas, lendo o arquivo em volta para entender o contexto.
2. Pule as perguntas de contexto já respondidas na conversa; se não houver nenhuma, declare as suposições.
3. Entregue a tabela padrão só com achados **introduzidos ou corrigidos** pela alteração.
4. Dê um **veredito**: ✅ aprovar, ⚠️ aprovar com ressalvas (achados Baixa/Média) ou ⛔ bloquear (qualquer achado Alta/Crítica introduzido).
5. Se a alteração corrigiu uma falha, diga qual teste de `security-testing` provaria a correção.

## Lembre-se

- Não invente linha nem CWE: cite o que está no arquivo.
- Explique a exploração no nível conceitual; nada de payload pronto para uso contra terceiros.
- Um achado sem correção nem detecção está incompleto.
- A matriz existe para priorizar: não chame tudo de crítico.
