#!/usr/bin/env bash
# TRAVA DE TRABALHO PESADO: um comando pesado por vez no computador inteiro, entre todas as sessões de IA abertas.
#
# POR QUÊ
#   Cinco sessões rodando a bateria de testes ao mesmo tempo num PC de 16 GB derrubam umas às outras o dia inteiro.
#   Com a trava, build, testes completos, npm ci e deploy entram numa fila; o resto do trabalho (ler, escrever,
#   planejar) segue em paralelo, sem esperar.
#
# USO
#   bash ferramentas/trava.sh <nome> <comando...>
#   ex.: bash ferramentas/trava.sh pesada npm run build
#        bash ferramentas/trava.sh pesada npm test
#        bash ferramentas/trava.sh deploy-app bash scripts/deploy.sh
#
# NOMES SUGERIDOS
#   pesada        build, suíte inteira de testes, npm ci (um por vez no PC)
#   deploy-<app>  publicação de um sistema (uma por vez por sistema)
#
# REGRAS
#   - A trava é uma pasta criada de uma vez (mkdir é atômico): $TRAVA_PASTA/<nome>.lock (padrão: ~/.travas).
#   - Espera até TRAVA_ESPERA_MIN minutos (padrão 8, para caber no limite de 10 min da ferramenta de terminal do
#     Claude Code). Não conseguiu: sai com o código 75 e a sessão tenta de novo depois.
#   - Teto de 45 min por chamada (TRAVA_ESPERA_TETO_MIN). O cache do Claude dura 1 h: sessão que espera mais que isso
#     acorda com o cache vencido e reescreve o contexto inteiro na cota. Melhor sair e chamar de novo.
#   - Trava de processo morto, ou mais velha que TRAVA_VELHA_MIN minutos (padrão 120), é desfeita.
#   - Ao sair, só apaga a trava se ela ainda for deste processo.
#   - O código de saída é o do comando.
#
# Versão simplificada (sem fila por ordem de chegada nem prioridade). Quando muitas sessões disputam a mesma trava e
# uma espera demais, o próximo passo é registrar a hora de chegada de cada uma e servir pela ordem.
set -u
nome="${1:?uso: trava.sh <nome> <comando...>}"; shift
[ "$#" -gt 0 ] || { echo "trava.sh: falta o comando" >&2; exit 2; }
case "$nome" in *[!a-z0-9-]*) echo "trava.sh: nome só com a-z, 0-9 e -" >&2; exit 2;; esac

PASTA="${TRAVA_PASTA:-$HOME/.travas}"
mkdir -p "$PASTA"
TRAVA="$PASTA/$nome.lock"
ESPERA_S="${TRAVA_ESPERA_S:-$(( ${TRAVA_ESPERA_MIN:-8} * 60 ))}"
TETO_S=$(( ${TRAVA_ESPERA_TETO_MIN:-45} * 60 ))
[ "$ESPERA_S" -gt "$TETO_S" ] && ESPERA_S="$TETO_S"
VELHA_S=$(( ${TRAVA_VELHA_MIN:-120} * 60 ))
INTERVALO_S="${TRAVA_INTERVALO_S:-5}"

desfazer_se_velha() {
  [ -d "$TRAVA" ] || return 0
  local pid desde agora
  pid="$(sed -n 's/^pid=//p' "$TRAVA/dono" 2>/dev/null)"
  desde="$(sed -n 's/^desde=//p' "$TRAVA/dono" 2>/dev/null)"
  agora="$(date +%s)"
  # No Git Bash, kill -0 às vezes falha uma vez com o processo vivo: só desfaz se falhar de novo 1 s depois.
  if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null && sleep 1 && ! kill -0 "$pid" 2>/dev/null; then
    echo "trava.sh: '$nome' era de um processo que já morreu ($pid); desfeita" >&2
    rm -rf "$TRAVA"
  elif [ -n "$desde" ] && [ $(( agora - desde )) -gt "$VELHA_S" ]; then
    echo "trava.sh: '$nome' passou de $(( VELHA_S / 60 )) min; desfeita" >&2
    rm -rf "$TRAVA"
  fi
}

inicio="$(date +%s)"
avisou=0
while ! mkdir "$TRAVA" 2>/dev/null; do
  desfazer_se_velha
  if [ $(( $(date +%s) - inicio )) -ge "$ESPERA_S" ]; then
    echo "trava.sh: '$nome' ocupada há mais de $(( ESPERA_S / 60 )) min; tente de novo depois" >&2
    exit 75
  fi
  [ "$avisou" = 0 ] && { echo "trava.sh: '$nome' ocupada; esperando a vez..." >&2; avisou=1; }
  sleep "$INTERVALO_S"
done
printf 'pid=%s\ndesde=%s\ncomando=%s\n' "$$" "$(date +%s)" "$*" > "$TRAVA/dono"

soltar() {
  [ "$(sed -n 's/^pid=//p' "$TRAVA/dono" 2>/dev/null)" = "$$" ] && rm -rf "$TRAVA"
}
trap soltar EXIT
trap 'exit 130' INT TERM

"$@"
