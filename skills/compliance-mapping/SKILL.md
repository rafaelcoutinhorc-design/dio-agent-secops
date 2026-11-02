---
name: compliance-mapping
description: Use quando o estudante quiser saber qual categoria do NIST CSF 2.0, controle do CIS Controls v8.1 ou prática do NIST SSDF cobre um risco, achado ou processo, montar um gap analysis (perfil atual × alvo) ou a lista de evidências para uma avaliação. A ISO 27001 entra só como equivalência de referência.
---

# Skill: Mapeamento de controles (NIST CSF + CIS Controls)

Traduz linguagem técnica em linguagem de governança, e vice-versa, usando frameworks públicos.

## Quando usar

"Qual controle cobre isso?", "Como provo isso numa avaliação?", "Monta um gap analysis", "O que é um Profile do CSF?". Se o estudante quiser entender um framework do zero, combine com `explain-concept`.

## Processo

### 1. Perguntas de contexto (uma por vez)

1. **Objetivo:** adequação ao NIST CSF, implantação do CIS Controls, avaliação interna ou estudo?
2. **Escopo:** qual parte da organização/sistema está em análise? (ex.: "a aplicação web e o monitoramento")
3. **Maturidade atual:** já existe política, ferramenta ou registro para o tema?

Se a empresa do estudante já usa ISO 27001, anote: no fim você indica a equivalência.

### 2. Mapeie

Use `agent/knowledge/nist-csf-ssdf.md` e `agent/knowledge/frameworks-referencia.md`. Para cada item, entregue:

| Risco/achado | Severidade | NIST CSF 2.0 | CIS Controls v8.1 | NIST SSDF (se for desenvolvimento) | Situação (atende / parcial / não atende) | Evidência esperada | Ação |
|--------------|------------|--------------|-------------------|------------------------------------|------------------------------------------|--------------------|------|

A severidade vem da matriz de `agent/knowledge/risk-scoring.md`. Explique em uma frase por que aquele controle se aplica.

### 3. Pense como avaliador

Para cada controle, verifique as 4 perguntas: está documentado? implementado? operando (há registros)? é melhorado? Aponte qual delas falha.

### 4. Conecte com a técnica

Mostre como a prática técnica gera evidência, sem depender de ferramenta específica: regra Sigma versionada e ativa → DE.CM / CIS 8 e 13; varredura de dependências no pipeline → ID.RA / CIS 7; teste de segurança automatizado → PR.PS / SSDF PW.8 / CIS 16; registro de incidentes e lições aprendidas → RS.MA, ID.IM / CIS 17.

### 5. Equivalência (só se pedirem)

Se a organização usa ISO 27001, acrescente uma coluna com o tema equivalente do Anexo A, usando a tabela de referência de `frameworks-referencia.md`, e avise que é um atalho didático.

### 6. Feche

Resuma em 3 linhas para um gestor (risco, impacto, ação) e lembre que a decisão de aceitar risco ou declarar adequação é humana.

## Lembre-se

- Cite o número do controle CIS com segurança; o número de uma salvaguarda, só se conferir na publicação oficial.
- Não reproduza texto de normas pagas; parafraseie.
- Compliance não é segurança: um controle "no papel" sem evidência operando não atende.
