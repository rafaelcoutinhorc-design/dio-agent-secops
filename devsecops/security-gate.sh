#!/usr/bin/env sh
# Portão de segurança genérico para pipeline de CI (qualquer ferramenta de CI que rode shell).
# Bloqueia a entrega (exit 1) se qualquer verificação falhar.
#
# Ferramentas (todas de código aberto, instale antes no runner):
#   gitleaks   - segredos no repositório
#   bandit     - análise estática (SAST) de Python
#   semgrep    - análise estática (SAST) por regras
#   pip-audit  - dependências com vulnerabilidade conhecida
#   checkov    - configuração insegura (container, IaC)
#   pytest     - testes de segurança de lab/tests
#
# Uso, na raiz do repositório:  sh devsecops/security-gate.sh
# Neste projeto o laboratório é vulnerável de propósito: o portão deve FALHAR
# até as correções serem aplicadas. Isso demonstra o bloqueio antes da produção.
#
# NIST SSDF PW.7 e PW.8 | NIST CSF 2.0 PR.PS e ID.RA | CIS Controls v8.1: 7 e 16

FALHAS=0

etapa() {
  nome="$1"; shift
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[ERRO] $nome: ferramenta '$1' não encontrada"
    FALHAS=$((FALHAS + 1))
    return
  fi
  echo "==> $nome"
  if "$@"; then
    echo "[OK] $nome"
  else
    echo "[FALHOU] $nome"
    FALHAS=$((FALHAS + 1))
  fi
}

etapa "Segredos"             gitleaks detect --source . --no-banner
etapa "SAST (bandit)"        bandit -r lab -ll -x lab/tests
etapa "SAST (semgrep)"       semgrep scan --config p/python --error lab
etapa "Dependências"         pip-audit -r lab/requirements.txt
etapa "Configuração"         checkov -d lab/config --quiet --compact
etapa "Testes de segurança"  pytest lab/tests -q

echo
if [ "$FALHAS" -gt 0 ]; then
  echo "Portão de segurança: BLOQUEADO ($FALHAS verificação(ões) com falha)"
  exit 1
fi
echo "Portão de segurança: LIBERADO"
