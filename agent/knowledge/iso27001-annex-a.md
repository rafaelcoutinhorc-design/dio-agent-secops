# ISO/IEC 27001:2022 — referência para o agente

Resumo de estudo, com títulos dos controles parafraseados. O texto oficial da norma é pago e deve ser consultado na ISO/ABNT (ABNT NBR ISO/IEC 27001:2022). A orientação de implementação de cada controle está na ISO/IEC 27002:2022.

## Estrutura da norma

- **Cláusulas 4 a 10 (obrigatórias):** contexto da organização (4), liderança (5), planejamento e tratamento de riscos (6), apoio (7), operação (8), avaliação de desempenho e auditoria interna (9), melhoria e não conformidades (10).
- **Anexo A:** 93 controles em 4 temas. A organização escolhe quais aplicar a partir da análise de riscos e justifica na **Declaração de Aplicabilidade (SoA)**.
  - **5 — Organizacionais** (37 controles)
  - **6 — Pessoas** (8 controles)
  - **7 — Físicos** (14 controles)
  - **8 — Tecnológicos** (34 controles)
- A versão 2022 substituiu a 2013 (114 controles em 14 domínios). Certificados na versão 2013 tiveram transição até 31/10/2025.

## Controles mais usados em achados técnicos

| Controle | Tema (parafraseado) | Quando citar |
|----------|---------------------|--------------|
| 5.7 | Inteligência de ameaças | Hunting guiado por TTPs, IoCs, feeds |
| 5.15 | Controle de acesso | Endpoint sem autorização, regra de acesso ausente |
| 5.17 | Informação de autenticação | Senha fraca, senha em código, hash inseguro |
| 5.23 | Segurança no uso de serviços em nuvem | Configuração de tenant M365/Azure |
| 5.24 | Planejamento e preparação para incidentes | Playbook ausente |
| 5.25 | Avaliação e decisão sobre eventos | Triagem de alertas do Defender |
| 5.26 | Resposta a incidentes | Contenção, isolamento de dispositivo |
| 5.27 | Aprendizado com incidentes | Lições aprendidas, nova regra de detecção |
| 5.28 | Coleta de evidências | Cadeia de custódia, exportação de logs |
| 8.2 | Direitos de acesso privilegiado | Painel admin aberto, conta admin compartilhada |
| 8.3 | Restrição de acesso à informação | IDOR, path traversal |
| 8.4 | Acesso ao código-fonte | Segredos no repositório |
| 8.5 | Autenticação segura | Login sem MFA, sem limite de tentativas |
| 8.7 | Proteção contra malware | Defender Antivirus, ASR |
| 8.8 | Gestão de vulnerabilidades técnicas | Biblioteca desatualizada, CVE, Defender Vulnerability Management |
| 8.9 | Gestão de configuração | `debug=True`, configuração padrão insegura |
| 8.11 | Mascaramento de dados | Dados pessoais exibidos ou logados sem máscara |
| 8.12 | Prevenção de vazamento de dados | Exfiltração, DLP |
| 8.15 | Registro de logs (logging) | Ausência de log ou log com senha |
| 8.16 | Atividades de monitoramento | Regras de detecção, SOC, Advanced Hunting |
| 8.20 | Segurança de redes | Serviço exposto em `0.0.0.0` |
| 8.24 | Uso de criptografia | MD5/SHA1 para senha, chave fixa |
| 8.25 | Ciclo de vida de desenvolvimento seguro | Falta de SDLC seguro |
| 8.26 | Requisitos de segurança de aplicações | Requisitos não definidos |
| 8.28 | Codificação segura | SQLi, XSS, command injection, deserialização |
| 8.29 | Testes de segurança no desenvolvimento e aceite | SAST/DAST ausentes |
| 8.31 | Separação de ambientes de desenvolvimento, teste e produção | Debug ou dados reais em produção |
| 8.32 | Gestão de mudanças | Deploy sem revisão |

## Como o auditor pensa (para orientar evidências)

1. **Existe política/procedimento?** (documentado)
2. **Está implementado?** (configuração, código, ferramenta)
3. **Está operando?** (registros: logs, tickets, relatórios de hunting, atas)
4. **É melhorado?** (indicadores, lições aprendidas, ações corretivas — cláusula 10)

Uma boa evidência é datada, rastreável e mostra o controle funcionando, por exemplo: o resultado de uma consulta KQL agendada como regra de detecção personalizada, com histórico de alertas.
