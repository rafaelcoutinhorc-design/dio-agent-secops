# Evidência: análise de configuração e infraestrutura

Transcrição real de uma execução do agente sobre o **cenário novo** de configuração insegura e de infraestrutura. O modelo (Claude, no Claude Code) carregou `AGENTS.md`, `agent/persona.md`, o comando `/analisar-codigo`, a skill `secure-code-review` e a base de conhecimento do projeto, a partir de:

```
/analisar-codigo lab/config/docker-compose.yml lab/config/nginx.conf lab/infra/sshd_config
```

As mensagens do agente estão sem edição. As respostas do estudante foram **simuladas**. Print: `04-config-infra.png`.

O objetivo do teste era ver se a mesma skill e o **mesmo formato de achado** funcionam fora do código. A tabela abaixo usa as mesmas colunas da análise do `app.py`, o que permite comparar os dois casos.

---

## Parte 1: perguntas de contexto

### 🛡️ Agente

Olá! Vou revisar os três arquivos juntos, porque eles descrevem a mesma pilha: o contêiner da `lab/app.py`, o banco PostgreSQL, o proxy reverso nginx e o acesso SSH ao host.

Já confirmei pelo cabeçalho dos arquivos que este é o seu **ambiente de laboratório**, configurado de propósito de forma insegura e com senhas fictícias. Então podemos fazer a análise estática sem problema. Só um lembrete: se em algum momento for colar algo de um ambiente real, mascare senhas, IPs públicos e nomes de host antes.

Antes de dar nota aos achados, preciso de um pouco de contexto. Sem ele, eu não consigo calibrar a **probabilidade**: a mesma porta aberta tem um risco num notebook isolado e outro bem diferente na internet. Vou fazer uma pergunta por vez.

**Pergunta 1 de até 4: exposição**

Os arquivos fazem bind em `0.0.0.0`: o app na porta 5000, o banco na 5432, o proxy na 80/443 e o SSH na 22. Isso quer dizer "escutar em todas as interfaces de rede". Na prática, **onde esse host roda ou rodaria?**

- (a) Só na sua máquina ou numa VM local, sem acesso de fora
- (b) Numa rede interna, como a da empresa, da faculdade ou um lab compartilhado
- (c) Num servidor com IP público na internet, como uma VM em nuvem

Se preferir pular as perguntas, é só dizer "pode seguir". Aí eu declaro as suposições por escrito e continuo.

### 👤 Estudante

(c) Imagina um servidor com IP público na internet.

### 🛡️ Agente

Anotado: **servidor com IP público na internet**. Isso pesa bastante na nota. Com bind em `0.0.0.0` e IP público, cada porta aberta fica alcançável por qualquer pessoa. Também entra na mira dos scanners automáticos que varrem a internet o tempo todo. Por isso, a probabilidade da maioria dos achados vai ficar alta.

**Pergunta 2 de até 4: dados**

Uma parte disso os próprios arquivos já mostram. A pilha guarda **credenciais**: os usuários e os hashes de senha na tabela `users` da app, a senha do banco e a `SECRET_KEY` no compose. Além disso, o nginx publica o diretório `/var/backups/`.

O que falta saber é o seguinte: **além das credenciais, que tipo de dado esse sistema guardaria ou teria nos backups?**

- (a) Dados pessoais de clientes ou usuários, como nome, CPF, e-mail ou telefone (o que coloca a LGPD em jogo)
- (b) Dados financeiros ou de pagamento
- (c) Nada sensível além das credenciais, só dados de teste

Isso define o **impacto**: um vazamento do banco ou do backup pesa bem mais se houver dados pessoais ou financeiros.

### 👤 Estudante

(a) Dados pessoais de clientes. E pode seguir com o resto: só temos o log de acesso do nginx e o log do SSH indo para um SIEM que aceita Sigma, e a meta é o NIST CSF começando pelo CIS IG1.

---

## Parte 2: análise

### 🛡️ Agente

Perfeito, já tenho o que preciso. Como você pediu para seguir, registro as suposições do que ficou sem resposta:

> **Suponho:** servidor com IP público na internet; **usuários anônimos** alcançam qualquer porta publicada; dados pessoais de clientes (LGPD) no banco e nos backups; telemetria = **log de acesso do nginx + log do SSH** num SIEM que aceita Sigma (sem log de processos do host e sem log do banco); meta = **NIST CSF 2.0**, começando pelo **CIS Controls v8.1 IG1**.

Dois termos antes da tabela:

- **CWE** é o catálogo público de tipos de fraqueza de software.
- **Sigma** é um formato aberto de regra de detecção que você converte para a linguagem de qualquer SIEM.

## Tabela de achados (ordenada por risco)

| # | Local | Achado | CWE | Impacto | Prob. | Risco (I×P) | Severidade | NIST CSF | CIS |
|---|-------|--------|-----|---------|-------|-------------|------------|----------|-----|
| 1 | `sshd_config:4,6-8,10,12-13` | SSH na internet com login de root, autenticação por senha e **senha vazia** permitidos, 10 tentativas por conexão e 5 min de carência | CWE-250 / CWE-307 / CWE-258 | 5 | 5 | 25 | **Crítica** | PR.AA, PR.IR | 5, 6, 12 |
| 2 | `docker-compose.yml:23-24,26-27` | PostgreSQL publicado em todas as interfaces (`5432:5432`) com `admin`/`admin123` (superusuário) | CWE-668 / CWE-521 | 5 | 5 | 25 | **Crítica** | PR.IR, PR.AA | 12, 5 |
| 3 | `nginx.conf:23,34-36` | `location /backup/` publica `/var/backups/` com `autoindex on`, ou seja, listagem e download anônimos | CWE-548 / CWE-200 | 4 | 5 | 20 | **Crítica** | PR.PS, PR.DS | 3, 4 |
| 4 | `docker-compose.yml:8-9,17-19` | Contêiner da app com `privileged`, `root`, socket do runtime montado, `/` do host montado e `network_mode: host` | CWE-250 | 5 | 4 | 20 | **Crítica** | PR.PS | 4 |
| 5 | `nginx.conf:30-32` | `/admin/` publicado para a internet sem nenhuma restrição no proxy | CWE-862 | 4 | 4 | 16 | Alta | PR.AA | 6 |
| 6 | `docker-compose.yml:13` | `FLASK_DEBUG: "1"` liga o depurador interativo | CWE-489 / CWE-215 | 5 | 3 | 15 | Alta | PR.PS | 4 |
| 7 | `docker-compose.yml:14-15,26-27` | Senha do banco e `SECRET_KEY` em texto claro num arquivo versionado | CWE-798 | 4 | 3 | 12 | Alta | PR.AA | 5, 16 |
| 8 | `nginx.conf:14-15,20-21` + `docker-compose.yml:33-34` | Só a porta 80 é publicada, então o login trafega em texto claro; o TLS configurado ainda aceita 1.0/1.1 e `ssl_ciphers ALL` | CWE-319 / CWE-327 | 4 | 3 | 12 | Alta | PR.DS, PR.IR | 12 |
| 9 | `sshd_config:22` | `LogLevel QUIET`: o sshd praticamente não registra autenticação e o SIEM fica cego | CWE-778 | 3 | 4 | 12 | Alta | DE.CM | 8 |
| 10 | `nginx.conf:24` | `client_max_body_size 0`: corpo de requisição sem limite (esgotamento de disco/memória) | CWE-770 | 3 | 4 | 12 | Alta | PR.IR | 4 |
| 11 | `nginx.conf:11` | `server_tokens on` expõe a versão do nginx | CWE-200 | 2 | 5 | 10 | Alta | PR.PS | 4 |
| 12 | `sshd_config:16-19` | X11, encaminhamento TCP, `GatewayPorts` e `PermitTunnel` liberados (pivô após invasão) | CWE-16 | 3 | 3 | 9 | Média | PR.IR | 4, 12 |
| 13 | `nginx.conf:3` | Processos do nginx rodando como root | CWE-250 | 4 | 2 | 8 | Média | PR.PS | 4 |
| 14 | `sshd_config:24-25` | Cifras CBC/3DES e MACs MD5/SHA-1 | CWE-327 | 4 | 2 | 8 | Média | PR.DS | 12 |
| 15 | `docker-compose.yml:7,22,32` | Imagens `latest` sem versão fixa | CWE-1104 | 3 | 2 | 6 | Média | ID.RA | 2, 7 |

**Justificativas e como a nota mudaria:**

- **#1:** P5 porque a porta 22 com IP público recebe tentativas automáticas de força bruta em minutos, e a configuração aceita root, senha e até conta sem senha. Numa VM só local, cairia para P2 (10, Alta).
- **#2:** I5 porque o `POSTGRES_USER` da imagem oficial é **superusuário**: controle total da base com dados pessoais. Sem a linha `ports`, só a rede interna do compose alcançaria o banco (P1-2, Média ou Baixa).
- **#3:** I4 porque são dados pessoais de muitos clientes. Uma ressalva honesta: no compose atual, o contêiner do proxy não monta `/var/backups`, então hoje o diretório pode estar vazio. Basta uma linha de volume para o risco virar real. Dei a nota pela intenção da configuração. Sem dados no diretório, cairia para I1.
- **#3 vs. #4 (empate em 20):** coloquei o #3 na frente porque ele não depende de nenhuma outra falha. O #4 exige que o atacante já execute código na app. Fiquei em P4 e não P1 porque a `lab/app.py` tem falhas conhecidas de execução de comando. Com a app limpa, iria para P2 (10, Alta).
- **#5 e #6:** a app já tem falhas próprias (rota admin sem autorização, debug). O proxy deveria ser a segunda barreira, e não é. No #6, dei P3 porque o depurador tem PIN e a `app.py` faz bind em `127.0.0.1`. Se exposto, vira Crítica.
- **#11:** cai em Alta pela matemática da matriz (2×5), mas é o mais barato de corrigir. Não deixe que ele roube tempo dos quatro primeiros.
- **Coerência:** com `network_mode: host`, a linha `ports` (10-11) é ignorada. Além disso, o proxy roda em outra rede, então o `proxy_pass http://127.0.0.1:5000` aponta para o próprio contêiner do proxy. A configuração é inconsistente. Pontuei pela intenção, e corrigir o #4 resolve isso junto.
- **CWE-319, 770 e 778:** não estão na nossa referência rápida. Confira a descrição em cwe.mitre.org antes de citar num relatório.

---

## Os 3 de maior risco em detalhe

### #1: SSH aberto para root, senha e senha vazia

**Por que é vulnerável:** o SSH é a porta da frente do servidor. Essa configuração aceita o usuário mais poderoso (root), autenticação por senha, contas **sem senha** e 10 chutes por conexão. Robôs varrem a internet o tempo todo testando senhas comuns em root (MITRE ATT&CK T1110, Brute Force; o ATT&CK é a base pública de técnicas de atacantes). Um acerto, ou uma conta sem senha, dá um **shell de root** (T1078, Valid Accounts). Isso é controle total do host, do banco e dos backups. E, com `GatewayPorts` e `PermitTunnel` liberados (#12), o servidor ainda vira trampolim.

**Correção** (`sshd_config`):
```
ListenAddress <IP da rede de administração ou da VPN>
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
PubkeyAuthentication yes
AllowUsers <usuario_admin>
MaxAuthTries 3
LoginGraceTime 30
LogLevel VERBOSE
X11Forwarding no
AllowTcpForwarding no
GatewayPorts no
PermitTunnel no
```
Some a isso uma regra de firewall que libera a 22 só para a origem administrativa. Teste com `sshd -t` antes de reiniciar e **mantenha uma sessão aberta** para não se trancar fora.

**Detecção:** atenção, com `LogLevel QUIET` (#9) **nenhuma regra vai disparar**. Corrija o log primeiro. Depois, esta regra cobre o comportamento mais grave:

```yaml
title: Login SSH aceito como root ou com senha vazia
id: <gere um UUID>
status: experimental
description: |
  Hipótese: num host exposto à internet com PermitRootLogin e PermitEmptyPasswords
  ligados, um acesso indevido aparece no log do sshd como "Accepted" para root
  ou pelo método "none" (conta sem senha).
references:
  - https://attack.mitre.org/techniques/T1078/
  - https://attack.mitre.org/techniques/T1110/
author: <seu nome>
date: 2026-11-02
tags:
  - attack.initial-access
  - attack.t1078
  - attack.credential-access
  - attack.t1110
logsource:
  product: linux
  service: sshd
detection:
  keywords_root:
    - 'Accepted password for root from'
    - 'Accepted keyboard-interactive/pam for root from'
  keywords_sem_senha:
    - 'Accepted none for'
  condition: keywords_root or keywords_sem_senha
falsepositives:
  - Administração legítima como root antes do hardening (depois dele, o esperado é zero)
level: high
```
Para a força bruta em si, crie uma segunda regra: conte `Failed password` por IP de origem numa janela de tempo, usando uma regra de correlação Sigma (`event_count`). Confira a sintaxe atual na especificação do SigmaHQ. Antes de considerar essas regras prontas, valide no laboratório que o texto do log do seu OpenSSH bate com elas. Regra não testada é rascunho.

**Evidência:** commit do `sshd_config` endurecido; saída de `sshd -T` mostrando `permitrootlogin no` e `passwordauthentication no`; regra de firewall da porta 22; as duas regras Sigma versionadas no repositório e ativas no SIEM; um teste de login root no lab gerando alerta.

### #2: Banco de dados publicado na internet com senha fraca

**Por que é vulnerável:** a linha `"5432:5432"` publica o banco em todas as interfaces do host. Na internet, qualquer pessoa conecta direto no PostgreSQL, sem passar pela app. A senha `admin123` é das primeiras que um robô testa, e o usuário é superusuário. O atacante lê, altera ou apaga **todos os dados pessoais dos clientes**. Ele pode até sequestrar a base pedindo resgate. Pela LGPD, é o tipo de evento que vira incidente com dados pessoais.

**Correção** (`docker-compose.yml`):
```yaml
  db:
    image: postgres:<versão fixa>          # confira a versão suportada atual
    # sem "ports": só a rede interna do compose alcança o banco
    environment:
      POSTGRES_USER: app_owner
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt         # gerado aleatoriamente e fora do git (.gitignore)
```
A app deve conectar com um **papel sem superusuário**, com permissão só nas tabelas de que precisa. Se a senha `admin123` já esteve exposta, trate como comprometida e troque.

**Detecção:** hoje você **não tem telemetria do banco** no SIEM, então este ataque é invisível. O log que o banco deveria gerar (`postgresql.conf`):
```
log_connections = on
log_disconnections = on
```
Com isso, toda conexão e toda falha de senha (`password authentication failed for user`) ficam registradas. Envie esse log ao SIEM e escreva uma regra Sigma de palavra-chave para falhas repetidas e para conexões vindas de fora da rede da app. Ajuste o `logsource` ao que o seu SIEM mapeia e confira no SigmaHQ. Até lá, a lacuna de detecção precisa constar como risco conhecido.

**Evidência:** diff do compose sem `ports` no `db`; varredura de portas feita **a partir de fora, no seu próprio lab**, mostrando a 5432 fechada; arquivo de segredo fora do controle de versão; `log_connections` ativo e eventos chegando ao SIEM.

### #3: Backups publicados com listagem de diretório

**Por que é vulnerável:** `autoindex on` monta uma página com a lista de todos os arquivos. O `location /backup/` serve `/var/backups/` para qualquer visitante. Backups costumam conter **cópias inteiras do banco**. O atacante não precisa de técnica nenhuma: basta abrir a URL e baixar. Isso costuma ser achado por ferramentas que enumeram caminhos comuns.

**Correção** (`nginx.conf`):
```nginx
server_tokens off;               # aproveita e resolve o #11

server {
    ...
    autoindex off;
    # location /backup/ REMOVIDO: backup não mora em servidor web
    location ~ /\. { deny all; } # bloqueia arquivos ocultos (.env, .git)
}
```
Leve os backups para um destino fora do servidor web, **criptografados** e com acesso restrito (CIS 11, recuperação de dados, e CIS 3, proteção de dados).

**Detecção:** essa você consegue **hoje**, porque o log de acesso do nginx já vai para o SIEM:

```yaml
title: Acesso ao caminho /backup/ publicado pelo proxy
id: <gere um UUID>
status: experimental
description: |
  Hipótese: quem descobre o diretório de backups exposto acessa /backup/ para listar
  e baixar arquivos; depois da correção, qualquer acesso indica reconhecimento.
references:
  - https://cwe.mitre.org/data/definitions/548.html
author: <seu nome>
date: 2026-11-02
tags:
  - attack.initial-access
  - attack.t1190
logsource:
  category: webserver
detection:
  selection:
    cs-uri-stem|startswith: '/backup'
  condition: selection
falsepositives:
  - Nenhum esperado; a rota não deveria existir
level: high
```
O mapeamento para T1190 é aproximado: é um recurso exposto por má configuração, não um exploit. Diga isso se apresentar a regra. Rode também um **hunting retroativo** no log do nginx: acessos a `/backup` com `sc-status` 200. Se aparecerem downloads de origem desconhecida, é um possível incidente com dados pessoais (NIST CSF RS.MA, CIS 17). A decisão sobre comunicar à ANPD e aos titulares é do encarregado de dados e do jurídico, não sua nem minha.

**Evidência:** diff do `nginx.conf`; `nginx -t` aprovado; requisição de teste no lab a `/backup/` retornando 404; regra versionada e ativa; resultado do hunting retroativo registrado (mesmo que vazio, com data).

---

## Plano de ação

1. **Agora:** endureça o SSH (#1) e troque `LogLevel` para `VERBOSE` (#9) no mesmo commit. Sem isso, você não vê o ataque mais provável.
2. **Agora:** tire o banco da internet e troque a senha (#2). Remova `/backup` e `autoindex` e faça o hunting retroativo (#3).
3. **Esta sprint:** o contêiner da app (#4, #6): remova `privileged`, o socket do runtime, o volume `/:/host`, `user: root` e `network_mode: host`, e use `FLASK_DEBUG: "0"`. Restrinja `/admin/` no proxy (#5).
4. **Esta sprint:** publique a 443 com só `TLSv1.2 TLSv1.3` e cifras modernas, redirecione 80 para 443 (#8) e limite `client_max_body_size` (#10). No SSH, troque cifras e MACs (#14). Fixe as versões das imagens (#15).
5. **Processo:** tire os segredos do compose (#7). Coloque no pipeline uma busca de segredos e uma análise estática de configuração (IaC), com revisão obrigatória de alterações em `lab/config/` e `lab/infra/` (NIST SSDF PW.7 e PW.9, CIS 16). As regras Sigma ficam versionadas no repositório, como em `lab/hunting/`.

**Sobre o IG1:** os achados caem principalmente nos controles CIS 3, 4, 5, 8 e 12. Todos têm salvaguardas no IG1, mas confira na publicação oficial do CIS **quais** salvaguardas de cada controle são IG1 antes de montar o seu perfil-alvo. E lembre: declarar que o ambiente "está adequado" é papel do avaliador. Nosso papel é deixar a evidência pronta.

**Uma lacuna para registrar:** as regras de `lab/hunting/` que olham criação de processos (por exemplo `python-web-spawning-shell.yml`) **não funcionam** com a sua telemetria atual, porque não há log de processos do host. Isso significa que uma fuga do contêiner (#4) hoje não seria vista. Vale incluir na sua lista de melhorias de detecção (DE.CM, CIS 8).

---

## Exercício

Corrija o achado **#1** no `lab/infra/sshd_config` e me mostre o diff. Depois, em **duas frases para um gestor**, explique por que o achado **#3** é um risco de LGPD e não só um problema técnico. Quer começar por qual dos dois?
