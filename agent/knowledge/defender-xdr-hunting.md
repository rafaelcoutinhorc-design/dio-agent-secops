# Microsoft Defender XDR — Advanced Hunting

Referência para escrever KQL (Kusto Query Language) no portal **security.microsoft.com → Hunting → Advanced hunting**. Documentação oficial: https://learn.microsoft.com/defender-xdr/advanced-hunting-overview

## Conceitos

- **Advanced Hunting:** consulta até **30 dias** de dados brutos de endpoints, e-mail, identidade e apps de nuvem.
- **Custom detection rule:** uma consulta salva e agendada que gera alertas e pode executar ações (isolar dispositivo, coletar pacote de investigação). A consulta precisa retornar `Timestamp`, `ReportId` e uma coluna de entidade (ex.: `DeviceId`, `AccountObjectId`).
- **Licenças:** tabelas `Device*` exigem Defender for Endpoint P2 (ou Defender for Business); `Email*` exigem Defender for Office 365 P2; `Identity*` exigem Defender for Identity. Sempre pergunte o que o estudante tem.
- **Microsoft Sentinel:** usa o mesmo KQL; no Sentinel a coluna de tempo é `TimeGenerated` em vez de `Timestamp`.

## Tabelas mais usadas

| Tabela | O que tem | Colunas-chave |
|--------|-----------|---------------|
| `DeviceProcessEvents` | Criação de processos | `Timestamp`, `DeviceName`, `FileName`, `ProcessCommandLine`, `InitiatingProcessFileName`, `InitiatingProcessCommandLine`, `AccountName`, `SHA256` |
| `DeviceNetworkEvents` | Conexões de rede | `RemoteIP`, `RemotePort`, `RemoteUrl`, `LocalPort`, `ActionType`, `InitiatingProcessFileName` |
| `DeviceFileEvents` | Criação/alteração de arquivos | `FileName`, `FolderPath`, `ActionType`, `SHA256` |
| `DeviceLogonEvents` | Logons no dispositivo | `LogonType`, `AccountName`, `RemoteIP`, `ActionType` |
| `DeviceRegistryEvents` | Alterações no registro | `RegistryKey`, `RegistryValueName`, `RegistryValueData` |
| `DeviceEvents` | Eventos diversos (ASR, exploit guard, etc.) | `ActionType`, `AdditionalFields` |
| `DeviceTvmSoftwareVulnerabilities` | Vulnerabilidades por dispositivo | `SoftwareName`, `CveId`, `VulnerabilitySeverityLevel` |
| `AlertInfo` / `AlertEvidence` | Alertas e entidades | `AlertId`, `Title`, `Severity`, `EntityType` |
| `EmailEvents`, `EmailUrlInfo`, `UrlClickEvents` | E-mail e cliques | `SenderFromAddress`, `Url`, `ActionType` |
| `IdentityLogonEvents` | Logons no AD/Entra ID | `ActionType`, `LogonType`, `Application` |
| `CloudAppEvents` | Atividades em apps de nuvem | `ActionType`, `Application`, `AccountObjectId` |

Os nomes de tabela evoluem (ex.: tabelas de sign-in do Entra em migração). Se a consulta falhar com "tabela não encontrada", consulte o painel de schema no próprio portal.

## Boas práticas de KQL

1. **Filtre o tempo primeiro:** `| where Timestamp > ago(7d)`.
2. **Filtre cedo, projete tarde:** `where` antes de `extend`/`summarize`; `project` só no final.
3. Use `has`/`in~` em vez de `contains` quando possível (mais rápido).
4. **Agregue para reduzir ruído:** `summarize count(), make_set(...) by DeviceName, bin(Timestamp, 1h)`.
5. Comente a hipótese no topo da consulta (`// Hipótese: ...`).
6. Documente **falsos positivos esperados** e como excluí-los.

## Padrão de consulta de hunting

```kql
// Hipótese: <o que o atacante faria e que rastro deixaria>
// MITRE ATT&CK: <técnica>   |   ISO 27001: 8.16   |   NIST CSF: DE.CM
DeviceProcessEvents
| where Timestamp > ago(7d)
| where <filtro do comportamento>
| summarize Execucoes = count(), Comandos = make_set(ProcessCommandLine, 10)
    by DeviceName, AccountName, InitiatingProcessFileName
| order by Execucoes desc
```

## Técnicas MITRE ATT&CK frequentes em apps web

| Técnica | Nome | Rastro no Defender |
|---------|------|--------------------|
| T1190 | Exploit Public-Facing Application | Processo do servidor web gerando processos incomuns |
| T1059.003 / .004 / .001 | Windows Command Shell / Unix Shell / PowerShell | `DeviceProcessEvents` com pai `python`, `java`, `w3wp`, `node` |
| T1505.003 | Web Shell | `DeviceFileEvents` criando `.py/.php/.aspx` em pasta do app |
| T1552.001 | Credentials In Files | Leitura de `.env`, `config.py` por processo inesperado |
| T1110 | Brute Force | `DeviceLogonEvents`/`IdentityLogonEvents` com muitas falhas |
| T1105 | Ingress Tool Transfer | `curl`/`wget`/`certutil` iniciados pelo app |
