# Frameworks públicos — referência para o agente

O agente usa **frameworks públicos e gratuitos** como base: NIST CSF 2.0, NIST SSDF, CIS Controls v8.1, OWASP e MITRE ATT&CK. A ISO/IEC 27001 aparece só como **referência de equivalência** no fim deste arquivo, para quem trabalha numa empresa que já a adota.

Detalhes do NIST estão em `nist-csf-ssdf.md`. Este arquivo cobre o CIS Controls, o OWASP e a tabela de equivalência.

## CIS Controls v8.1

Publicado pelo Center for Internet Security (https://www.cisecurity.org/controls), gratuito para uso. São **18 controles**, cada um com salvaguardas (safeguards) divididas em 3 Grupos de Implementação: **IG1** (higiene básica, toda organização), **IG2** e **IG3** (organizações maiores ou mais expostas).

| # | Controle | Quando citar |
|---|----------|--------------|
| 1 | Inventário de ativos da organização | Servidor ou container desconhecido |
| 2 | Inventário de software | Dependência sem controle de versão, imagem `latest` |
| 3 | Proteção de dados | Dado sensível sem criptografia, senha em log |
| 4 | Configuração segura de ativos e software | `debug=True`, `privileged`, serviço com configuração padrão |
| 5 | Gestão de contas | Conta admin compartilhada, login root |
| 6 | Gestão de controle de acesso | Rota sem autorização, falta de MFA |
| 7 | Gestão contínua de vulnerabilidades | Biblioteca desatualizada, CVE sem correção |
| 8 | Gestão de logs de auditoria | Ausência de log, log com segredo |
| 9 | Proteção de e-mail e navegador | Phishing, extensões |
| 10 | Defesas contra malware | Execução de binário suspeito |
| 11 | Recuperação de dados | Backup ausente ou não testado |
| 12 | Gestão da infraestrutura de rede | Porta exposta em `0.0.0.0`, TLS antigo |
| 13 | Monitoramento e defesa de rede | Regras de detecção, SIEM, IDS |
| 14 | Conscientização e treinamento | Erro humano recorrente |
| 15 | Gestão de provedores de serviço | Terceiro com acesso sem controle |
| 16 | Segurança de software de aplicação | SQLi, XSS, command injection, falta de SAST |
| 17 | Gestão de resposta a incidentes | Playbook ausente |
| 18 | Testes de intrusão | Pentest e validação de controles |

Cite o **número do controle** com segurança. Só cite o número de uma salvaguarda (ex.: 16.x) se conferir na publicação oficial.

## OWASP

- **OWASP Top 10:2021** (https://owasp.org/Top10): as 10 categorias de risco mais comuns em aplicações web. A tabela por CWE está em `cwe-owasp-quickref.md`.
- **OWASP ASVS** (Application Security Verification Standard): lista de requisitos verificáveis para aplicações, em 3 níveis. Bom para transformar um achado em requisito de aceite. Confira a versão vigente antes de citar o número de um requisito.
- **OWASP Cheat Sheet Series** (https://cheatsheetseries.owasp.org): a correção recomendada para cada tipo de falha.

## MITRE ATT&CK

Base pública de táticas e técnicas de atacantes (https://attack.mitre.org). Usada para escrever a hipótese de detecção. Técnicas frequentes estão em `threat-hunting-sigma.md`.

## Como escolher o framework

| Pergunta do estudante | Use |
|-----------------------|-----|
| "Qual o risco disso para o negócio?" | NIST CSF 2.0 (função e categoria) |
| "O que eu implemento primeiro?" | CIS Controls (comece pelo IG1) |
| "Como desenvolvo de forma segura?" | NIST SSDF + OWASP ASVS |
| "Como o atacante faria e como eu vejo?" | MITRE ATT&CK + regra Sigma |
| "A empresa usa ISO 27001, qual controle é?" | Tabela de equivalência abaixo |

## Equivalência com a ISO/IEC 27001:2022 (apenas referência)

A ISO 27001 é uma norma paga e certificável. O agente **não** a usa como base, mas indica o tema equivalente do Anexo A para quem precisa conversar com uma área que já a adota. Os títulos são parafraseados; o texto oficial deve ser consultado na ISO/ABNT.

| NIST CSF 2.0 | CIS Controls v8.1 | Tema equivalente na ISO 27001:2022 (Anexo A) |
|--------------|-------------------|----------------------------------------------|
| PR.AA | 5, 6 | 5.15 a 5.18 (acesso e autenticação), 8.2, 8.5 |
| PR.DS | 3 | 8.11, 8.12, 8.24 (dados e criptografia) |
| PR.PS | 2, 4, 16 | 8.9 (configuração), 8.25 a 8.29 (desenvolvimento seguro) |
| PR.IR | 12 | 8.20 a 8.22 (redes) |
| ID.AM | 1, 2 | 5.9 (inventário) |
| ID.RA | 7 | 8.8 (vulnerabilidades técnicas) |
| DE.CM, DE.AE | 8, 13 | 8.15, 8.16 (logs e monitoramento) |
| RS.MA, RS.AN, RS.MI | 17 | 5.24 a 5.28 (incidentes) |

Esta tabela é um atalho didático, não um mapeamento oficial. O NIST e o CIS publicam mapeamentos oficiais em seus sites.

## Como um auditor ou avaliador pensa

Vale para qualquer framework. Para cada controle, pergunte:

1. **Está documentado?** (política, procedimento, padrão)
2. **Está implementado?** (configuração, código, ferramenta)
3. **Está operando?** (registros: logs, tickets, relatórios, histórico de alertas)
4. **É melhorado?** (indicadores, lições aprendidas, ações corretivas)

Uma boa evidência é datada, rastreável e mostra o controle funcionando. Exemplo: uma regra Sigma versionada no repositório, convertida e ativa no SIEM, com histórico de alertas triados.
