# NIST — CSF 2.0, SSDF e Resposta a Incidentes

Documentos públicos e gratuitos do NIST (https://www.nist.gov/cyberframework e https://csrc.nist.gov).

## NIST Cybersecurity Framework (CSF) 2.0 — fev/2024

Seis **funções**, cada uma com **categorias** (código de 2 letras + ponto + 2 letras):

| Função | Pergunta que responde | Categorias |
|--------|----------------------|------------|
| **GV — Govern** | Como a estratégia e os riscos de cyber são decididos? | GV.OC contexto organizacional · GV.RM estratégia de gestão de riscos · GV.RR papéis e responsabilidades · GV.PO política · GV.OV supervisão · GV.SC riscos da cadeia de suprimentos |
| **ID — Identify** | O que temos e quais riscos corremos? | ID.AM gestão de ativos · ID.RA avaliação de riscos · ID.IM melhoria |
| **PR — Protect** | Como evitamos o incidente? | PR.AA identidade, autenticação e controle de acesso · PR.AT conscientização e treinamento · PR.DS segurança de dados · PR.PS segurança de plataforma · PR.IR resiliência da infraestrutura |
| **DE — Detect** | Como percebemos o ataque? | DE.CM monitoramento contínuo · DE.AE análise de eventos adversos |
| **RS — Respond** | O que fazemos durante o incidente? | RS.MA gestão de incidentes · RS.AN análise · RS.CO comunicação · RS.MI mitigação |
| **RC — Recover** | Como voltamos ao normal? | RC.RP execução do plano de recuperação · RC.CO comunicação na recuperação |

Novidade da 2.0: a função **Govern** e a gestão de riscos da cadeia de suprimentos. Os **Tiers** (1 a 4) medem maturidade; os **Profiles** (atual × alvo) servem para gap analysis.

### Atalhos de mapeamento

- Vulnerabilidade de código → **PR.PS** (plataforma/software seguro) e **ID.RA** (vulnerabilidades identificadas)
- Senha/autenticação → **PR.AA**
- Criptografia, vazamento → **PR.DS**
- Regra de detecção / hunting → **DE.CM** e **DE.AE**
- Triagem e contenção → **RS.MA**, **RS.AN**, **RS.MI**
- Lições aprendidas → **ID.IM**

## NIST SP 800-218 — Secure Software Development Framework (SSDF) v1.1

Quatro grupos de práticas para desenvolvimento seguro:

- **PO — Prepare the Organization:** requisitos, papéis, ferramentas, critérios.
- **PS — Protect the Software:** proteger código-fonte e integridade dos releases.
- **PW — Produce Well-Secured Software:** destaque para **PW.5** (codificar seguindo práticas seguras), **PW.7** (revisar/analisar código), **PW.8** (testar o executável), **PW.9** (configuração segura por padrão).
- **RV — Respond to Vulnerabilities:** identificar, tratar e analisar causa raiz.

Use o SSDF quando o achado for de desenvolvimento: ele complementa o controle 8.28 da ISO 27001.

## NIST SP 800-61 Rev. 3 — abr/2025

Recomendações de resposta a incidentes, agora organizadas pelas funções do CSF 2.0 (em vez do antigo ciclo de 4 fases da Rev. 2: preparação; detecção e análise; contenção, erradicação e recuperação; pós-incidente). Útil para montar playbooks do SOC que usam o Defender XDR.

## Equivalência rápida ISO 27001 ↔ NIST CSF 2.0

| ISO 27001:2022 | NIST CSF 2.0 |
|----------------|--------------|
| 5.15, 5.17, 8.2, 8.5 | PR.AA |
| 8.24, 8.11, 8.12 | PR.DS |
| 8.9, 8.25, 8.28, 8.29 | PR.PS |
| 8.8 | ID.RA |
| 8.15, 8.16 | DE.CM, DE.AE |
| 5.24 a 5.28 | RS.MA, RS.AN, RS.MI, ID.IM |

O NIST mantém mapeamentos oficiais (Informative References) no site do CSF. A tabela acima é um atalho didático, não um mapeamento oficial.
