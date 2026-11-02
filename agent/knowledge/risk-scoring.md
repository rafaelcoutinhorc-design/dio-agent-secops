# Matriz de risco — formato padrão de achado

Todas as skills classificam achados da mesma forma, para que casos diferentes (código, configuração, infraestrutura) possam ser comparados. A lógica segue o NIST SP 800-30 Rev. 1: **risco = impacto × probabilidade**.

## Impacto (1 a 5): o que acontece se a falha for explorada?

| Nota | Impacto | Exemplo |
|------|---------|---------|
| 1 | Mínimo | Informação pública exposta, sem efeito prático |
| 2 | Baixo | Vazamento de informação técnica (versão, stack trace) |
| 3 | Moderado | Acesso a dados de um usuário, indisponibilidade curta |
| 4 | Alto | Acesso a dados de muitos usuários ou a credenciais, perfil admin |
| 5 | Severo | Execução de código no servidor, controle total do host ou da base |

## Probabilidade (1 a 5): quão fácil é explorar no contexto informado?

Considere **exposição** (localhost, rede interna, internet), **autenticação** (anônimo, logado, admin), **complexidade** (uma requisição ou várias etapas) e **pré-requisitos** (depende de outra falha?).

| Nota | Probabilidade | Exemplo |
|------|---------------|---------|
| 1 | Rara | Exige acesso físico ou outra falha grave antes |
| 2 | Improvável | Rede interna, usuário autenticado, várias etapas |
| 3 | Possível | Rede interna sem autenticação, ou internet com autenticação |
| 4 | Provável | Internet, anônimo, exige alguma técnica |
| 5 | Quase certa | Internet, anônimo, uma requisição, técnica amplamente conhecida |

## Severidade = impacto × probabilidade

| Risco (I × P) | Severidade |
|---------------|------------|
| 17 a 25 | **Crítica** — corrigir agora |
| 10 a 16 | **Alta** — corrigir nesta sprint |
| 5 a 9 | **Média** — planejar |
| 1 a 4 | **Baixa** — registrar e acompanhar |

## Tabela padrão de achados

Toda análise, de qualquer skill, usa estas colunas e esta ordem (maior risco primeiro):

| # | Local | Achado | CWE | Impacto | Prob. | Risco (I×P) | Severidade | NIST CSF | CIS |
|---|-------|--------|-----|---------|-------|-------------|------------|----------|-----|

- **Local:** `arquivo:linha` (ou `arquivo:chave` em configuração).
- **CWE:** o tipo de fraqueza. Em configuração, use o CWE mais próximo (ex.: CWE-16 Configuration, CWE-250 privilégio desnecessário, CWE-521 senha fraca).
- **Impacto e Prob.:** nota de 1 a 5, com uma frase de justificativa abaixo da tabela quando não for óbvia.
- **NIST CSF:** categoria (ex.: PR.PS). **CIS:** número do controle (ex.: 16).

## Regras

- A nota depende do **contexto informado** (perguntas de contexto). Se o estudante não respondeu, declare a suposição.
- Diga como a severidade **mudaria** em outro contexto (ex.: "Média em localhost, Crítica na internet").
- O **CVSS** (v3.1 ou v4.0, do FIRST) pode ser citado como referência externa, mas a matriz acima é o formato oficial do agente.
- Não chame tudo de crítico: a matriz existe para priorizar.
