# DevSecOps: revisão antes da produção

Exemplos para levar a revisão de segurança para o fluxo de desenvolvimento, em três momentos. Tudo com ferramentas de código aberto e sem depender de um fornecedor de CI.

| Momento | O que roda | Arquivo |
|---------|-----------|---------|
| **Durante o desenvolvimento** | O agente revisa só o que mudou e dá um veredito (aprovar, aprovar com ressalvas, bloquear) | Comando `/revisar-alteracao` (`.claude/commands/revisar-alteracao.md`) |
| **Antes do commit** | Busca de segredos e análise estática | [`pre-commit-config.exemplo.yaml`](pre-commit-config.exemplo.yaml) |
| **No pipeline** | Segredos, SAST, dependências, configuração e testes de segurança; bloqueia a entrega se algo falhar | [`security-gate.sh`](security-gate.sh) |

## Como encaixar no seu CI

Qualquer ferramenta de CI que execute um passo de shell serve. O passo é sempre o mesmo:

```bash
sh devsecops/security-gate.sh
```

O passo precisa ter as ferramentas listadas no cabeçalho do script instaladas no ambiente de execução.

## Resultado esperado neste projeto

O `lab/` é vulnerável de propósito, então hoje o portão **bloqueia**. Esse é o ponto da demonstração: as falhas encontradas na revisão não chegariam à produção. Depois de corrigir o `app.py` e as configurações, o portão deve liberar.

## Ligação com os frameworks

- **NIST SSDF:** PW.7 (revisar e analisar o código) e PW.8 (testar o executável).
- **NIST CSF 2.0:** PR.PS (software e plataforma seguros) e ID.RA (vulnerabilidades identificadas).
- **CIS Controls v8.1:** 7 (gestão contínua de vulnerabilidades) e 16 (segurança de software de aplicação).

> Ferramentas de varredura devem rodar só no seu próprio código e laboratório.
