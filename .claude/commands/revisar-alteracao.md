---
description: Revisão de segurança de uma alteração (git diff) antes de ir para produção, com veredito
argument-hint: [opcional: ramo ou commit de comparação, ex. main]
---

Obtenha a alteração a revisar:

- Se um ramo ou commit foi informado ($ARGUMENTS), use `git diff $ARGUMENTS...HEAD`.
- Senão, use `git diff --staged`; se estiver vazio, use `git diff`.

Depois, abra e siga o **Modo alteração (DevSecOps)** de `skills/secure-code-review/SKILL.md`.
Entregue a tabela padrão de `agent/knowledge/risk-scoring.md` só com o que a alteração introduz ou corrige, e termine com o veredito: aprovar, aprovar com ressalvas ou bloquear.
