---
name: compliance-mapping
description: Use quando o estudante quiser saber qual controle da ISO/IEC 27001:2022 ou categoria do NIST CSF 2.0 cobre um risco, achado ou processo, montar um gap analysis, uma linha da Declaração de Aplicabilidade ou a lista de evidências para auditoria.
---

# Skill: Mapeamento de compliance (ISO 27001 + NIST CSF)

Traduz linguagem técnica em linguagem de governança, e vice-versa.

## Quando usar

"Qual controle da ISO cobre isso?", "Como provo isso pro auditor?", "Monta um gap analysis", "O que é SoA?". Se o estudante quiser entender a norma do zero, combine com `explain-concept`.

## Processo

### 1. Perguntas de contexto (uma por vez)

1. **Objetivo:** certificação ISO 27001, adequação ao NIST CSF, auditoria interna ou estudo?
2. **Escopo:** qual parte da organização/sistema está em análise? (ex.: "a aplicação web e o SOC")
3. **Maturidade atual:** já existe política, ferramenta ou registro para o tema?

### 2. Mapeie

Use `agent/knowledge/iso27001-annex-a.md` e `agent/knowledge/nist-csf-ssdf.md`. Para cada item, entregue:

| Risco/achado | Controle ISO 27001:2022 | NIST CSF 2.0 | Situação (atende / parcial / não atende) | Evidência esperada | Ação |
|--------------|-------------------------|--------------|------------------------------------------|--------------------|------|

Explique em uma frase por que aquele controle se aplica.

### 3. Pense como auditor

Para cada controle, verifique as 4 perguntas: está documentado? implementado? operando (há registros)? é melhorado? Aponte qual delas falha.

### 4. Conecte com a técnica

Quando possível, mostre como o Microsoft Defender gera evidência (ex.: regra de detecção personalizada → 8.16; Defender Vulnerability Management → 8.8; histórico de incidentes → 5.26/5.27).

### 5. Feche

Resuma em 3 linhas para um gestor (risco, impacto, ação) e lembre que a decisão de aceitar risco ou declarar conformidade é humana.

## Lembre-se

- Não reproduza o texto oficial da ISO (é protegido por direitos autorais); parafraseie.
- Se não tiver certeza do número do controle, diga e oriente a conferir na norma.
- Compliance não é segurança: um controle "no papel" sem evidência operando não atende.
