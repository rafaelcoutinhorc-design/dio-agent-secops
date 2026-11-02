---
name: threat-hunting
description: Use quando o estudante quiser caçar uma ameaça, escrever ou revisar uma regra de detecção em Sigma (formato aberto), mapear um comportamento para o MITRE ATT&CK ou transformar uma hipótese em regra recorrente.
---

# Skill: Threat hunting com Sigma e MITRE ATT&CK

Conduz um hunting guiado por hipótese: da ameaça à regra Sigma, da regra ao alerta, do alerta à evidência de controle. Tudo em formato aberto, sem depender de fornecedor.

## Quando usar

"Como eu detecto X?", "Me ajuda com essa regra Sigma", "Quero criar uma regra de detecção", ou um achado da `secure-code-review` precisa de detecção.

## Processo

### 1. Perguntas de contexto (uma por vez)

1. **O que você quer encontrar?** (técnica, ferramenta, indicador, comportamento)
2. **Que telemetria você tem?** (log da aplicação, log do servidor web, criação de processos, acesso a arquivos, conexões de rede) — define quais categorias de `logsource` funcionam.
3. **Ambiente:** laboratório próprio ou ambiente corporativo? Em ambiente corporativo, lembre que hunting exige autorização e que dados reais (usuários, IPs, nomes de host) não devem ser colados aqui.
4. **Objetivo:** investigação pontual ou regra recorrente?

### 2. Escreva a hipótese

Uma frase: "Se um atacante explorar X, veremos Y na telemetria Z". Mapeie para MITRE ATT&CK (veja `agent/knowledge/threat-hunting-sigma.md`).

### 3. Construa a regra Sigma

Mostre a regra e explique cada bloco:

1. Metadados (`title`, `description` com a hipótese, `tags` ATT&CK)
2. `logsource` (categoria da telemetria)
3. `selection` (o comportamento)
4. `filter_*` (o legítimo que deve ser excluído)
5. `condition`, `falsepositives` e `level`

Se a telemetria disponível não cobrir o comportamento, diga isso e proponha o **log que a aplicação deveria gerar** (campos, nível, sem dados sensíveis).

### 4. Valide no laboratório

Oriente a gerar o evento de forma segura **no próprio laboratório** (ex.: rodar `lab/app.py` em `127.0.0.1` e disparar o comportamento) e conferir se a regra, convertida com `sigma convert`, retorna resultado. Liste os **falsos positivos esperados** e como excluí-los.

### 5. Promova a regra (se for recorrente)

Sugira `level`, frequência de execução, playbook curto de triagem (o que olhar primeiro, quando escalar) e ação de resposta, sempre com aprovação humana para ações como isolar um host. A ativação no SIEM é feita pelo estudante.

### 6. Feche com evidência e próximo passo

- **Evidência de controle:** regra versionada + ativa + histórico de alertas triados → NIST CSF DE.CM, DE.AE, RS.AN; CIS Controls 8, 13 e 17.
- **Próximo passo:** sugira uma variação da hipótese para o estudante escrever sozinho.

## Lembre-se

- Regra que não foi testada é rascunho; diga isso.
- Não ensine a burlar ferramentas de monitoramento. Se pedirem evasão, recuse e redirecione para detecção.
- Use os campos da taxonomia Sigma; não invente campo.
