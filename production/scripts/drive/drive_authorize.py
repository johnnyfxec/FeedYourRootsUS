#!/usr/bin/env python3
"""Autorizacion UNICA de Drive por "flujo de dispositivo" (la hace Claude con Johnny, una sola vez).

  python3 drive_authorize.py        # imprime un CODIGO y una direccion; Johnny la abre, escribe el codigo y toca Permitir.
                                    # El script espera (hasta 15 min) y al final imprime GOOGLE_OAUTH_REFRESH_TOKEN.

Alcance: SOLO drive.file (acceso unicamente a los archivos que esta app cree). Requiere un cliente OAuth de tipo
"TVs y dispositivos de entrada limitada" y las variables GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET.
El refresh token NUNCA se escribe en el repo.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SCOPE = "https://www.googleapis.com/auth/drive.file"


def _post(url, data):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(data).encode()), timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode() or "{}")


def main():
    cid, sec = os.environ.get("GOOGLE_OAUTH_CLIENT_ID"), os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("Faltan GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET en el entorno.")
    j = _post("https://oauth2.googleapis.com/device/code", {"client_id": cid, "scope": SCOPE})
    if "device_code" not in j:
        sys.exit("Google rechazo la solicitud: " + json.dumps(j)[:400])
    print(f"ABRE: {j['verification_url']}\nESCRIBE EL CODIGO: {j['user_code']}", flush=True)
    fin = time.time() + min(int(j.get("expires_in", 900)), 900)
    espera = int(j.get("interval", 5))
    while time.time() < fin:
        time.sleep(espera)
        t = _post("https://oauth2.googleapis.com/token", {
            "client_id": cid, "client_secret": sec, "device_code": j["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"})
        if "refresh_token" in t:
            print("GOOGLE_OAUTH_REFRESH_TOKEN=" + t["refresh_token"])
            print("alcance:", t.get("scope"))
            return
        err = t.get("error")
        if err == "slow_down":
            espera += 5
        elif err not in ("authorization_pending", None):
            sys.exit("Autorizacion fallida: " + json.dumps(t)[:300])
    sys.exit("El codigo caduco sin que se autorizara. Repetir.")


if __name__ == "__main__":
    main()
