#!/usr/bin/env python3
"""Autorizacion OAuth de Pinterest por flujo "loopback" (navegador real) -- la hace Johnny, una
sola vez, desde un dispositivo con navegador (su tablet, via Termux u otro). Mismo patron que
drive_authorize_web.py (Google), adaptado a las particularidades de la API v5 de Pinterest:

  python3 pinterest_authorize_web.py
      Imprime una URL. Johnny la abre en SU PROPIO navegador, inicia sesion con la cuenta de
      Pinterest Business de Feed Your Roots y toca "Permitir". El navegador lo redirige a
      http://localhost:8787/ -- este script levanta un servidor HTTP local en ESE puerto fijo
      para recibir la redireccion, intercambia el codigo por un access/refresh token, los
      imprime y termina. Timeout: 5 minutos.

DIFERENCIAS CLAVE VS. GOOGLE (drive_authorize_web.py) -- confirmadas contra
developers.pinterest.com, 28-oct-2026, no asumidas de memoria:
  1. Puerto FIJO, no aleatorio. Pinterest exige que el redirect_uri este registrado EXACTO
     de antemano en developers.pinterest.com (My apps > Configure > Redirect URIs) -- no
     acepta "cualquier localhost:<puerto>" como si acepta Google para clients "Desktop app".
     Por eso aqui el puerto es fijo (8787) y DEBE coincidir con lo registrado en la consola.
  2. El intercambio de code por token usa HTTP Basic Auth (client_id:client_secret en base64
     dentro del header Authorization), NO client_secret en el body del POST como Google.
  3. El endpoint de autorizacion es https://www.pinterest.com/oauth/ (no accounts.google.com).
     El de intercambio de token es https://api.pinterest.com/v5/oauth/token.
  4. Scopes probados para fyr-publisher: boards:read (leer boards, necesario para resolver
     board_id al crear un pin) + pins:write (crear pines de imagen Y video pins -- no existe
     un scope separado para video, confirmado contra developers.pinterest.com/docs/content/update/)
     + user_accounts:read (unico scope que habilita los endpoints de analiticas -- GET
     /user_account/analytics/top_pins y similares -- sin el, dan "code":3, missing scope,
     aunque la cuenta sea Business y el resto de las llamadas funcionen bien).

Variables de entorno requeridas (de la app ya creada en developers.pinterest.com):
  PINTEREST_CLIENT_ID / PINTEREST_CLIENT_SECRET

El refresh token NUNCA se escribe en el repo -- solo se imprime en terminal, para que Johnny
decida donde guardarlo (su .env de Termux).
"""
import base64
import http.server
import json
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request

PUERTO_FIJO = 8787  # DEBE coincidir exacto con el Redirect URI registrado en developers.pinterest.com
REDIRECT_URI = f"http://localhost:{PUERTO_FIJO}/"

SCOPES = ["boards:read", "boards:write", "pins:read", "pins:write", "user_accounts:read"]
# boards:write y pins:read se agregaron el 28-oct-2026 -- confirmado por error real de la API
# ("code":3, Missing: ['boards:write','pins:read']) al intentar crear un pin con solo
# boards:read+pins:write. La doc de Pinterest no deja claro de antemano que crear un pin
# requiera tambien leer pines y escribir en el board -- quedo confirmado empiricamente.
# user_accounts:read se agrego el 31-oct-2026 -- confirmado por error real al llamar
# GET /user_account/analytics/top_pins con el token viejo ("code":3, Missing:
# ['user_accounts:read']). Necesario para cualquier endpoint de analiticas (metricas de
# Pines/cuenta), no solo para leer datos basicos de la cuenta como sugiere el nombre.

AUTH_URL = "https://www.pinterest.com/oauth/"
# NOTA (29-oct-2026): Standard access aprobado para "fyr publisher" -- revertido de vuelta a
# produccion (quitado el "-sandbox"). Mientras la app estuvo en Trial access, Pinterest exigia
# que el intercambio de token se hiciera contra api-sandbox.pinterest.com (error real confirmado
# el 28-oct: {"code":29,"message":"Apps with Trial access may not create Pins in production ...
# use API Sandbox instead."}) para que el token resultante funcionara contra los endpoints de
# datos de sandbox. Con Standard access ya no aplica esa restriccion.
TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"


class _Handler(http.server.BaseHTTPRequestHandler):
    code = None
    error = None

    def do_GET(self):
        qs = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(qs)
        if "code" in params:
            _Handler.code = params["code"][0]
            msg = "Autorizado. Ya puedes cerrar esta pestana y volver a la terminal."
        else:
            _Handler.error = params.get("error", ["desconocido"])[0]
            msg = f"Error de autorizacion: {_Handler.error}. Vuelve a la terminal."
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"<html><body><h2>{msg}</h2></body></html>".encode())

    def log_message(self, *a):
        pass  # silencioso, no ensuciar la terminal de Johnny


def _post_token(cid, sec, code):
    basic = base64.b64encode(f"{cid}:{sec}".encode()).decode()
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "continuous_refresh": "true",
    }).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode() or "{}")


def main():
    cid = os.environ.get("PINTEREST_CLIENT_ID")
    sec = os.environ.get("PINTEREST_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("Faltan PINTEREST_CLIENT_ID / PINTEREST_CLIENT_SECRET en el entorno.")

    server = http.server.HTTPServer(("127.0.0.1", PUERTO_FIJO), _Handler)
    params = {
        "client_id": cid,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": "fyr_publisher_setup",
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    server.timeout = 300
    print(f"ABRE ESTA URL EN TU NAVEGADOR (en tu tablet, no en esta terminal):\n\n{url}\n")
    print(f"Esperando la autorizacion en {REDIRECT_URI} (5 min) ...", flush=True)

    t = threading.Thread(target=server.handle_request, daemon=True)
    t.start()
    t.join(timeout=300)

    if _Handler.error:
        sys.exit("Pinterest devolvio un error: " + _Handler.error)
    if not _Handler.code:
        sys.exit("No llego el codigo de autorizacion en 5 minutos. Repite el proceso.")

    tok = _post_token(cid, sec, _Handler.code)
    if "access_token" not in tok:
        sys.exit("Pinterest no devolvio access_token: " + json.dumps(tok)[:400])

    print("\nPINTEREST_ACCESS_TOKEN=" + tok["access_token"])
    if "refresh_token" in tok:
        print("PINTEREST_REFRESH_TOKEN=" + tok["refresh_token"])
    print("scope concedido:", tok.get("scope"))
    print("expira en (segundos):", tok.get("expires_in"))


if __name__ == "__main__":
    main()
