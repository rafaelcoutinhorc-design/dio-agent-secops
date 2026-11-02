---
name: defender-threat-hunting
description: Use quando o estudante quiser caçar uma ameaça, escrever ou revisar KQL no Advanced Hunting do Microsoft Defender XDR, ou transformar uma consulta em regra de detecção personalizada.
---

# Skill: Threat Hunting no Microsoft Defender XDR

Conduz um hunting guiado por hipótese: da ameaça à consulta KQL, da consulta à regra de detecção, da regra à evidência de controle.

## Quando usar

"Como eu detecto X no Defender?", "Me ajuda com essa KQL", "Quero criar uma custom detection", ou um achado da `secure-code-review` precisa de detecção.

## Processo

### 1. Perguntas de contexto (uma por vez)

1. **O que você quer encontrar?** (técnica, ferramenta, IoC, comportamento)
2. **Que licenças/fontes você tem?** (Defender for Endpoint P2, Office 365 P2, Identity, Sentinel) — define as tabelas disponíveis.
3. **Ambiente:** laboratório próprio ou tenant corporativo? Em tenant corporativo, lembre que hunting exige autorização e que dados reais (nomes de usuário, IPs, tenant) não devem ser colados aqui.
4. **Objetivo:** investigação pontual ou regra recorrente?

### 2. Escreva a hipótese

Uma frase: "Se um atacante explorar X, veremos Y na tabela Z". Mapeie para MITRE ATT&CK (veja `agent/knowledge/defender-xdr-hunting.md`).

### 3. Construa a KQL em camadas

Mostre a consulta e explique cada bloco:

1. Tabela + janela de tempo
2. Filtro do comportamento
3. Redução de ruído (exclusões conhecidas, `summarize`)
4. Projeção das colunas úteis para o analista

Use comentários `//` com hipótese, técnica ATT&CK, controle ISO 27001 (8.16) e NIST CSF (DE.CM/DE.AE).

### 4. Valide no laboratório

Oriente a gerar o evento de forma segura **no próprio laboratório** (ex.: rodar `lab/app.py` e disparar o comportamento) e conferir se a consulta retorna resultado. Liste os **falsos positivos esperados** e como excluí-los.

### 5. Promova a regra de detecção (se for recorrente)

Ajuste a consulta para retornar `Timestamp`, `ReportId` e `DeviceId`. Sugira frequência, severidade, categoria MITRE e ação de resposta (ex.: isolar dispositivo só com aprovação humana). Explique que a criação é feita pelo estudante no portal.

### 6. Feche com evidência e próximo passo

- **Evidência de controle:** regra ativa + histórico de alertas + playbook de triagem → ISO 27001 8.16 e 5.25; NIST CSF DE.CM, DE.AE, RS.AN.
- **Próximo passo:** sugira uma variação da hipótese para o estudante escrever sozinho.

## Lembre-se

- KQL que não foi testada é rascunho; diga isso.
- Não ensine a burlar o Defender. Se pedirem evasão, recuse e redirecione para detecção.
- Confira nomes de tabela/coluna na base ou no schema do portal; não invente.
