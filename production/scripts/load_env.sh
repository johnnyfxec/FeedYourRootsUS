#!/usr/bin/env bash
# load_env.sh (20-oct-2026) -- carga el .env local (fuera de git) al entorno de la shell,
# para que drive_client.py y demas scripts encuentren sus credenciales SIN que tengas que
# pegarlas a mano en cada sesion de Claude Code.
#
# Uso en Termux (una sola vez, configuralo y olvidate):
#   1. Agrega esta linea a tu ~/.bashrc (o ~/.zshrc si usas zsh):
#        source /ruta/a/feedyourrootsus/production/scripts/load_env.sh
#   2. Abre una terminal nueva (o corre: source ~/.bashrc) -- listo, cada sesion nueva
#      arranca con las variables ya puestas, sin ningun paso manual.
#
# Si el .env no existe todavia (primera vez), este script NO falla ni interrumpe tu shell
# -- solo avisa una vez, para que sepas que falta copiar .env.example como .env y rellenarlo.
#
# Este script se puede "source"-ar (carga en la shell actual) o ejecutar directo -- en ese
# caso solo imprime que variables quedarian puestas, sin contaminar el proceso que lo llamo.

_fyr_env_file() {
  # Busca el .env en la raiz del repo, sin importar desde que carpeta se llame este script.
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
  echo "$script_dir/../../.env"
}

_FYR_ENV_FILE="$(_fyr_env_file)"

if [ -f "$_FYR_ENV_FILE" ]; then
  set -a  # exporta automaticamente cada variable que se defina a continuacion
  # shellcheck disable=SC1090
  source "$_FYR_ENV_FILE"
  set +a
  if [ "${FYR_ENV_QUIET:-0}" != "1" ]; then
    echo "[FYR] Credenciales cargadas desde $_FYR_ENV_FILE"
  fi
else
  echo "[FYR] Aviso: no encontre $_FYR_ENV_FILE -- copia .env.example como .env en la raiz del repo y rellenalo (una sola vez)." >&2
fi

unset -f _fyr_env_file
unset _FYR_ENV_FILE
