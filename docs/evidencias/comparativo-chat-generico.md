# Comparativo: SecOps Expert × chat genérico

Os dois testes usaram **o mesmo modelo** e a mesma pergunta sobre o mesmo arquivo:

```
Analise a segurança deste código: [lab/app.py]
```

- **Chat genérico:** sem `AGENTS.md`, persona, skills ou base de conhecimento, só com o código colado. Resposta completa em [resposta-chat-generico.md](resposta-chat-generico.md). Print: `03-chat-generico.png`.
- **SecOps Expert:** com o projeto carregado, via `/analisar-codigo lab/app.py`. Transcrição completa em [analise-app-py.md](analise-app-py.md). Prints: `01-perguntas-contexto.png` e `02-tabela-achados.png`.

Um terceiro teste, só com o agente, rodou a mesma skill sobre **configuração e infraestrutura** ([analise-config-infra.md](analise-config-infra.md), print `04-config-infra.png`).

## Resultado

| Critério | Chat genérico | SecOps Expert |
|----------|---------------|---------------|
| Pergunta o contexto antes de analisar | ❌ Responde direto | ✅ Infere o que o código já mostra e faz só a pergunta que falta (telemetria e meta) |
| Encontra as vulnerabilidades principais | ✅ 18 itens, incluindo SSRF, timing e log injection | ✅ 14 itens; agrupa alguns e não lista SSRF, timing e log injection |
| Linha e CWE por achado | ⚠️ Rota e CWE, sem linha | ✅ `arquivo:linha` e CWE |
| Severidade explicada | ⚠️ Fixa, sem critério | ✅ Impacto × probabilidade, com justificativa e "como mudaria" em outro contexto |
| Mesmo formato em outro cenário | — | ✅ A análise de configuração e infraestrutura usou a mesma tabela, o que permite comparar os casos |
| Correção em código | ✅ Para todos, mais um esboço do app corrigido | ✅ Para os 3 de maior risco |
| Detecção (regra Sigma, ATT&CK) | ❌ Não tem | ✅ Reaproveita as regras de `lab/hunting/` e cria uma regra nova para o SSTI |
| Teste que prova a correção | ❌ Não tem | ✅ Aponta o teste de `lab/tests/` de cada achado |
| Mapeamento NIST CSF 2.0 e CIS Controls | ❌ Não tem | ✅ Por achado, mais NIST SSDF no plano |
| Evidência verificável | ❌ Não tem | ✅ Por achado: commit, teste, regra ativa |
| Neutro em fornecedor | ⚠️ Cita um produto comercial de nuvem | ✅ Só padrões abertos e ferramentas de código aberto |
| Plano de ação priorizado | ✅ 4 grupos por prioridade | ✅ 5 ações com prazo, achados e frameworks |
| Exercício para fixar o aprendizado | ❌ Não tem | ✅ Corrigir o #1 com o teste falhando antes e passando depois |
| Lembrete de dados sensíveis e limites | ✅ Sim | ✅ Sim, e deixa a decisão de risco com o dono do risco e o avaliador |

## Leitura honesta

O modelo base já é bom em **achar** vulnerabilidades. Neste teste o chat genérico listou até mais itens e entregou um esboço completo do app corrigido. A especialização não melhora a detecção de falhas. O ganho está em **transformar o achado em trabalho de segurança de verdade**:

1. **Contexto e comparabilidade:** a severidade sai de uma matriz explícita (impacto × probabilidade), no mesmo formato para código e para configuração.
2. **Detecção:** cada falha ganha uma regra Sigma, que funciona em qualquer SIEM. A própria análise criou uma regra nova, que entrou no laboratório (`lab/hunting/web-ssti-hello.yml`).
3. **Prova:** cada correção tem um teste que falha antes e passa depois.
4. **Governança:** cada falha vira categoria do NIST CSF e controle do CIS, com a evidência esperada.
5. **Ensino:** a conversa termina com um exercício, e não com uma lista para copiar.

**Melhoria aplicada depois do teste:** o chat genérico trouxe SSRF no `/ping`, comparação de senha sem tempo constante e injeção de log, que o agente não listou. Esses três itens entraram no checklist do passo 3 da skill `secure-code-review`. As transcrições acima são da versão anterior a essa melhoria.
