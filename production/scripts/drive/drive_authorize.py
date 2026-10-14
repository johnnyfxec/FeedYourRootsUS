#!/usr/bin/env python3
"""Autorizacion UNICA de Drive (se corre una sola vez, la hace Claude con Johnny).

Paso 1:  python3 drive_authorize.py url
         -> imprime la direccion que Johnny abre en su navegador y donde da "Permitir".
         Al terminar, el navegador muestra una pagina que "no se puede abrir" (localhost). ES NORMAL:
         Johnny copia la direccion COMPLETA de esa pagina y se la pega a Claude.
Paso 2:  python3 drive_authorize.py canjear "<direccion pegada>"
         -> imprime el refresh token. Se guarda como variable GOOGLE_OAUTH_REFRESH_TOKEN
            (entorno de claude.ai/code y secreto de GitHub). NUNCA se escribe en el repo.

Requiere GOOGLE_OAUTH_CLIENT_ID y GOOGLE_OAUTH_CLIENT_SECRET en el entorno.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

REDIRECT = "http://localhost:8765/"
SCOPE = "https://www.googleapis.com/auth/drive"


def _creds():
    cid, sec = os.environ.get("GOOGLE_OAUTH_CLIENT_ID"), os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("Faltan GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET en el entorno.")
    return cid, sec


def main(argv):
    if len(argv) < 2 or argv[1] not in ("url", "canjear"):
        sys.exit(__doc__)
    cid, sec = _creds()
    if argv[1] == "url":
        q = urllib.parse.urlencode({
            "client_id": cid, "redirect_uri": REDIRECT, "response_type": "code", "scope": SCOPE,
            "access_type": "offline", "prompt": "consent"})
        print("https://accounts.google.com/o/oauth2/v2/auth?" + q)
        return
    pegado = argv[2]
    code = urllib.parse.parse_qs(urllib.parse.urlparse(pegado).query).get("code", [None])[0]
    if not code:
        sys.exit("La direccion pegada no trae 'code='. Pidele a Johnny que copie la direccion completa.")
    data = urllib.parse.urlencode({
        "code": code, "client_id": cid, "client_secret": sec,
        "redirect_uri": REDIRECT, "grant_type": "authorization_code"}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data), timeout=60) as r:
        j = json.loads(r.read())
    if "refresh_token" not in j:
        sys.exit("Google no devolvio refresh_token (repetir el paso 1 con prompt=consent): " + json.dumps(j)[:300])
    print("REFRESH_TOKEN=" + j["refresh_token"])
    print("alcance:", j.get("scope"))


if __name__ == "__main__":
    main(sys.argv)
