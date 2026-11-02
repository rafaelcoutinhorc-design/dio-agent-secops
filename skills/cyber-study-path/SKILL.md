---
name: cyber-study-path
description: Use quando o estudante quiser uma trilha de estudos em cibersegurança (por onde começar, qual área seguir, o que estudar para AppSec, monitoramento/detecção, GRC ou infraestrutura segura), com fases, práticas em laboratório e marcos de portfólio.
---

# Skill: Trilha de estudos em cibersegurança

Monta uma trilha em fases, ligada a papéis reais do mercado (NICE Framework) e às funções do NIST CSF 2.0, com prática em laboratório próprio e entregas de portfólio.

## Quando usar

"Quero entrar em segurança, por onde começo?", "O que estudar para ser analista de detecção?", "Sou dev, como migro para AppSec?". Para encaixar cursos e Formações específicos da DIO, combine com `study-plan`.

## Processo

### 1. Perguntas de contexto (uma por vez)

1. **Ponto de partida:** nunca trabalhou com TI, vem de desenvolvimento, de infraestrutura/suporte ou já atua em segurança?
2. **Área de interesse:** desenvolvimento seguro (AppSec), monitoramento e detecção, governança e riscos (GRC), infraestrutura e cloud seguras, ou ainda não sabe?
3. **Tempo:** quantas horas por semana e em quanto tempo quer chegar à primeira vaga ou promoção?

Se não souber a área, proponha as 4 fases comuns e decida a especialização na fase 3.

### 2. Monte a trilha em fases

| Fase | Objetivo | Conteúdo | Prática no laboratório | Entrega de portfólio |
|------|----------|----------|------------------------|----------------------|
| **1. Fundamentos** | Entender o que se protege | Redes (TCP/IP, DNS, HTTP), Linux, linha de comando, Git, uma linguagem (Python) | Subir um servidor web local e ler os logs | Repositório com anotações e scripts |
| **2. Base de segurança** | Falar a língua da área | Tríade CID, autenticação, criptografia básica, OWASP Top 10, MITRE ATT&CK, NIST CSF 2.0 (6 funções) | Explorar e corrigir o `lab/app.py` com o agente | Relatório de análise no formato padrão |
| **3. Especialização** | Escolher um papel | Ver tabela abaixo | Projeto da especialização | Projeto publicado com README |
| **4. Prática contínua** | Ganhar experiência | Desafios em ambientes de treino legais (CTFs), leitura de relatórios públicos de incidentes | Um laboratório novo por mês | Artigos curtos explicando o que aprendeu |

Especializações da fase 3:

| Área | Funções do NIST CSF | Estude | Projeto sugerido |
|------|---------------------|--------|------------------|
| **AppSec / DevSecOps** | PR.PS, ID.RA | NIST SSDF, OWASP ASVS, SAST, testes de segurança, pipeline | Pipeline com `devsecops/security-gate.sh` e testes de `lab/tests/` |
| **Monitoramento e detecção** | DE.CM, DE.AE, RS.AN | Logs, Sigma, MITRE ATT&CK, triagem de alertas, SIEM de código aberto | Conjunto de regras Sigma testadas contra o `lab/app.py` |
| **GRC** | GV, ID.RA | NIST CSF Profiles, CIS Controls (IG1), NIST SP 800-30, LGPD | Gap analysis do laboratório com perfil atual × alvo |
| **Infraestrutura segura** | PR.IR, PR.PS | Hardening de Linux e SSH, containers, TLS, CIS Controls 4 e 12 | Corrigir `lab/config/` e `lab/infra/` com antes e depois |

### 3. Distribua no tempo

Divida as horas por semana entre **teoria (40%)**, **prática no laboratório (40%)** e **portfólio (20%)**. Dê marcos mensais verificáveis ("ao fim do mês 2, você entrega o relatório do `app.py`").

### 4. Conecte com a DIO

Indique o **tipo** de experiência da DIO que cobre cada fase (Curso, Formação, Bootcamp de segurança ou cloud). Cite pelo nome só o que confirmou, usando `study-plan` e `agent/knowledge/learning-experiences.md`.

### 5. Feche

Pergunte qual fase parece mais difícil e proponha a primeira tarefa da semana.

## Lembre-se

- Não recomende certificação, curso pago ou ferramenta comercial como obrigatório; mostre alternativas gratuitas.
- Prática ofensiva só em laboratório próprio ou em ambientes de treino feitos para isso.
- Confira os nomes atuais dos papéis do NICE Framework antes de citar.
