# Comparativo: SecOps Expert × chat genérico

Os dois testes usaram **o mesmo modelo** e a mesma pergunta sobre o mesmo arquivo:

```
Analise a segurança deste código: [lab/app.py]
```

- **Chat genérico:** sem `AGENTS.md`, persona, skills ou base de conhecimento. Resposta completa em [resposta-chat-generico.md](resposta-chat-generico.md). Print: `03-chat-generico.png`.
- **SecOps Expert:** com o projeto carregado, via `/analisar-codigo lab/app.py`. Transcrição completa em [analise-app-py.md](analise-app-py.md). Prints: `01-perguntas-contexto.png` e `02-tabela-achados.png`.

## Resultado

| Critério | Chat genérico | SecOps Expert |
|----------|---------------|---------------|
| Pergunta o contexto antes de analisar | ❌ Responde direto | ✅ Infere o que o código já mostra e faz 2 perguntas, uma por vez (quem acessa; Defender e norma) |
| Encontra as vulnerabilidades principais | ✅ Encontra todas as 11 | ✅ Encontra todas as 11 |
| Aponta itens extras de hardening | ✅ Flags de cookie, CSRF, cabeçalhos, log injection | ⚠️ Não lista esses itens |
| Linha e CWE por achado | ⚠️ Linha sim, CWE não | ✅ Linha e CWE |
| Severidade ajustada ao contexto | ⚠️ Fixa (`debug=True` aparece como Crítica mesmo em `127.0.0.1`) | ✅ Justificada pelas premissas informadas |
| Correção em código | ✅ Sim | ✅ Sim, para os 3 mais graves |
| Detecção no Microsoft Defender (KQL, ATT&CK) | ❌ Não tem | ✅ Reaproveita `lab/hunting/` e cria uma consulta nova em `DeviceNetworkEvents` |
| Mapeamento ISO 27001:2022 e NIST CSF 2.0 | ❌ Não tem | ✅ Por achado, mais o NIST SSDF |
| Evidência para auditoria | ❌ Não tem | ✅ Por achado: PR, teste, regra ativa |
| Plano de ação priorizado | ⚠️ Lista de prioridade | ✅ Tabela com prazo, achado e controle |
| Exercício para fixar o aprendizado | ❌ Oferece reescrever o código | ✅ Propõe um exercício técnico e um de governança |
| Lembrete de dados sensíveis e limites | ⚠️ Só "mantenha local" | ✅ Pede para não colar dados reais e deixa a decisão de risco com o dono do risco e o auditor |

## Leitura honesta

O modelo base já é bom em **achar** vulnerabilidades: nos dois testes as 11 foram encontradas, e o chat genérico ainda trouxe itens de hardening que o agente não listou. A especialização não melhora a detecção de falhas. O ganho está em **transformar o achado em trabalho de segurança de verdade**:

1. **Contexto:** a severidade passa a depender de exposição, usuários e dados, em vez de ser fixa.
2. **Detecção:** cada falha ganha uma consulta KQL para o Defender XDR. A própria análise ainda encontrou um falso positivo na consulta do projeto, que foi corrigido.
3. **Governança:** cada falha vira controle ISO 27001 e NIST CSF, com a evidência que um auditor aceitaria.
4. **Ensino:** a conversa termina com um exercício, e não com "quer que eu reescreva?".

**Melhoria aplicada depois do teste:** o passo 3 da skill `secure-code-review` passou a incluir um checklist de hardening HTTP (flags de cookie, CSRF, cabeçalhos de segurança, escape de saída), que foi o ponto em que o chat genérico se saiu melhor.
