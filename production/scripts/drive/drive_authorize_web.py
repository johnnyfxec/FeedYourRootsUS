#!/usr/bin/env python3
"""Autorizacion UNICA de Drive por flujo OAuth "loopback" (navegador real) -- la hace Johnny, una sola vez,
desde un dispositivo con navegador (su tablet, via Termux u otro). Reemplaza el flujo de dispositivo
(drive_authorize.py), que Google restringe a scopes "no sensibles" (no deja pedir `drive` completo).

  python3 drive_authorize_web.py
      Imprime una URL. Johnny la abre en SU PROPIO navegador (no en este sandbox), inicia sesion con la
      cuenta de Google correcta y toca "Permitir". El navegador lo redirige a http://localhost:<puerto>/...
      -- este script levanta un servidor HTTP local en un puerto libre elegido al azar para recibir esa
      redireccion, intercambia el codigo por un refresh token, lo imprime y termina. Timeout: 5 minutos.

Requiere un client ID OAuth de tipo "Aplicacion de escritorio" ("Desktop app"), NO "TV y dispositivos de
entrada limitada" -- ese tipo es el que rechaza el scope completo. Variables de entorno:
  GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET  (del client "Desktop app")

NOTA (16-oct-2026): para clientes tipo "Desktop app", Google NO exige registrar un Redirect URI en la
consola -- acepta automaticamente cualquier `http://localhost:<puerto>/` sin configuracion previa (es la
unica razon por la que este flujo es practico: cada corrida puede usar un puerto distinto). Por eso este
script NO usa un puerto fijo, sino uno libre que el sistema operativo asigna solo.

Alcance: `drive` completo (lectura/escritura de TODO el Drive accesible para la cuenta que autoriza, no solo
archivos creados por esta app). Es necesario para poder subir directo dentro de carpetas que Johnny ya creo
a mano (ej. Content_Pieces/PZA_x/<fecha>/) -- con `drive.file` la API solo puede escribir en objetos que ella
misma creo (restriccion de Google, confirmada 16-oct-2026, no un bug nuestro: ver nota en drive_client.py).

NOTA DE ARQUITECTURA (16-oct-2026): el flujo de dispositivo (TV) y el flujo loopback (Desktop app) son el
MISMO backend de Google Drive y el MISMO tipo de token (OAuth de usuario) -- lo unico que cambia es COMO se
obtiene el consentimiento. El loopback corre un navegador real, por eso Google si permite scopes sensibles
ahi. Una vez obtenido el refresh token, el cliente (drive_client.py) funciona identico sin importar en que
maquina corra despues (este sandbox, la tablet via Termux, un servidor) -- el problema de hoy nunca fue
"donde corre el script", fue el tipo de client OAuth y su scope.

El refresh token NUNCA se escribe en el repo -- solo al scratchpad de la sesion o a donde Johnny decida
guardarlo el (ej. una variable de entorno en su .bashrc de Termux).
"""
import http.server
import json
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/youtube.upload",
]
SCOPE = " ".join(SCOPES)
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


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


def _post(url, data):
    try:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode())
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode() or "{}")


def main():
    cid = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    sec = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("Faltan GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET en el entorno "
                  "(client OAuth tipo 'Aplicacion de escritorio').")

    server = http.server.HTTPServer(("127.0.0.1", 0), _Handler)  # puerto 0 = el SO asigna uno libre
    puerto = server.server_address[1]
    redirect_uri = f"http://localhost:{puerto}/"
    params = {
        "client_id": cid,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",  # fuerza que Google SIEMPRE devuelva refresh_token, incluso en re-autorizaciones
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    server.timeout = 300
    print(f"ABRE ESTA URL EN TU NAVEGADOR (en tu tablet, no en esta terminal):\n\n{url}\n")
    print(f"Esperando la autorizacion en http://localhost:{puerto}/ (5 min) ...", flush=True)

    t = threading.Thread(target=server.handle_request, daemon=True)
    t.start()
    t.join(timeout=300)

    if _Handler.error:
        sys.exit("Google devolvio un error: " + _Handler.error)
    if not _Handler.code:
        sys.exit("No llego el codigo de autorizacion en 5 minutos. Repite el proceso.")

    tok = _post(TOKEN_URL, {
        "client_id": cid,
        "client_secret": sec,
        "code": _Handler.code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    })
    if "refresh_token" not in tok:
        sys.exit("Google no devolvio refresh_token: " + json.dumps(tok)[:400] +
                  "\n(Si ya habias autorizado antes sin 'prompt=consent' puede que no lo reemita; "
                  "revoca el acceso en https://myaccount.google.com/permissions y reintenta.)")
    print("\nGOOGLE_OAUTH_REFRESH_TOKEN=" + tok["refresh_token"])
    print("alcance concedido:", tok.get("scope"))


if __name__ == "__main__":
    main()
