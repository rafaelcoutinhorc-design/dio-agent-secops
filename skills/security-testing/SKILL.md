---
name: security-testing
description: Use quando o estudante quiser provar com testes que uma vulnerabilidade existe e que a correção funciona, montar testes de segurança automatizados (testes de unidade, análise estática, dependências, segredos) ou levar esses testes para o pipeline. Só em código e ambiente de laboratório próprios.
---

# Skill: Testes de segurança

Transforma achados em **testes que falham enquanto a falha existe e passam depois da correção**. É assim que uma correção vira evidência e que a falha não volta.

## Quando usar

"Como eu provo que corrigi?", "Escreve um teste para esse achado", "Que ferramenta de SAST eu uso?", "Quero rodar testes de segurança no pipeline", ou depois de uma `secure-code-review`.

## Processo

### 1. Confirme o escopo

Testes de segurança só em código e ambiente **do próprio estudante, de laboratório**. Nada de apontar ferramenta de varredura para sistema de terceiros ou de produção sem autorização formal. Se for o caso, recuse e explique.

### 2. Perguntas de contexto (uma por vez)

1. **Linguagem e framework de teste** já usados? (ex.: Python + pytest)
2. **Quais achados** quer cobrir? (se veio da `secure-code-review`, use a tabela de lá, do maior risco para o menor)
3. **Onde vai rodar?** Só na máquina, num hook antes do commit ou no pipeline de CI?

### 3. Escolha a camada de teste

| Camada | O que pega | Ferramentas abertas (exemplos) | Framework |
|--------|-----------|--------------------------------|-----------|
| **Teste de unidade/integração de segurança** | A falha específica, no comportamento | `pytest` + cliente de teste do framework (sem subir servidor) | SSDF PW.8, CIS 16 |
| **SAST** (análise estática) | Padrões perigosos no código | Bandit, Semgrep | SSDF PW.7, CIS 16 |
| **Dependências (SCA)** | Bibliotecas com vulnerabilidade conhecida | `pip-audit`, OSV-Scanner | NIST CSF ID.RA, CIS 7 |
| **Segredos** | Senha, token e chave no repositório | Gitleaks | CIS 3 e 16 |
| **Configuração / IaC** | Container, servidor web, SSH inseguros | Checkov, Trivy (modo config), Hadolint | CIS 4 |
| **DAST** (dinâmico) | Falhas com o app rodando | OWASP ZAP em modo baseline, **só contra `127.0.0.1`** | SSDF PW.8 |

Comece pelo teste de unidade do achado de maior risco: é o mais didático e o que vira evidência mais forte.

### 4. Escreva o teste

Para cada achado:

- **Nome claro:** `test_<rota>_<comportamento_seguro_esperado>`.
- **Afirme o comportamento seguro**, não o ataque. Ex.: "o parâmetro `host` com separador de comando não executa o segundo comando", "`../` no nome do arquivo retorna 4xx".
- **Use entradas inofensivas** que só provam a falha (ex.: `{{7*7}}` para SSTI, `echo MARCADOR` para injeção de comando). Nada de payload destrutivo.
- **Use o cliente de teste** do framework, sem abrir porta de rede.

Explique: o teste **falha hoje** (prova a vulnerabilidade) e **passa depois da correção** (prova o controle). Veja o exemplo em `lab/tests/test_seguranca_app.py`.

### 5. Automatize

Mostre como encaixar no fluxo:

- **Antes do commit:** hook com busca de segredos e SAST (`devsecops/pre-commit-config.exemplo.yaml`).
- **No pipeline:** o script `devsecops/security-gate.sh`, que qualquer ferramenta de CI pode chamar e que bloqueia a entrega se algo falhar.

### 6. Feche com evidência e exercício

- **Evidência:** o teste no repositório + o histórico do pipeline mostrando o teste vermelho antes e verde depois da correção → NIST SSDF PW.7 e PW.8, CIS Controls 16.
- **Exercício:** "Escreva o teste do achado #2 sozinho e me mostre."

## Lembre-se

- Teste de segurança que nunca falhou não prova nada: rode antes da correção.
- Ferramenta de varredura só no laboratório.
- Falso positivo de SAST se trata com justificativa registrada, não desligando a regra inteira.
