#!/usr/bin/env python3
"""OBSOLETO (16-oct-2026): usar drive_authorize_web.py en su lugar. Se deja este archivo como registro de
por que el flujo de dispositivo no sirve: Google rechaza el scope `drive` completo en este flujo (solo deja
scopes "no sensibles" como drive.file), y drive.file no permite escribir dentro de carpetas que Johnny ya
tenia creadas (solo en objetos creados por la propia app) -- confirmado ademas por un reporte publico
identico de otro usuario con el mismo tipo de conector ("User cannot add children"). drive_authorize_web.py
usa un flujo OAuth distinto (loopback/navegador real) que si acepta el scope completo.

Autorizacion UNICA de Drive por "flujo de dispositivo" (la hace Claude con Johnny, una sola vez).

  python3 drive_authorize.py        # imprime un CODIGO y una direccion; Johnny la abre, escribe el codigo y toca Permitir.
                                    # El script espera (hasta 15 min) y al final imprime GOOGLE_OAUTH_REFRESH_TOKEN.

Alcance: SOLO drive.file (acceso unicamente a los archivos/carpetas que esta app cree). Requiere un cliente
OAuth de tipo "TVs y dispositivos de entrada limitada" y las variables GOOGLE_OAUTH_CLIENT_ID /
GOOGLE_OAUTH_CLIENT_SECRET. El refresh token NUNCA se escribe en el repo.

NOTA DE DISENO (16-oct-2026): se intento ampliar a drive completo porque el conector de Drive (MCP) y esta
app OAuth son identidades de acceso SEPARADAS ante Google (aunque autentiquen la misma cuenta de Gmail): con
drive.file, el conector no podia ni ver los archivos/carpetas creados por esta app, haciendo imposible el
diseno original "API sube a root, conector mueve". Google RECHAZA el scope drive completo en el flujo de
dispositivo (device flow) -- "Invalid device flow scope" -- es una restriccion de Google para este tipo de
cliente OAuth, no configurable. Se revierte a drive.file.

Diseno vigente: la API crea su PROPIA cadena de carpetas (mkdir, root -> ... -> carpeta final) y sube dentro
de ellas -- nunca sube ni mueve a una carpeta que ya existia creada por el conector o a mano, porque esa
carpeta es invisible para esta app. Esto deja una jerarquia de carpetas paralela a la que Johnny arma a mano
en Drive; nomenclatura distintiva para esas carpetas automaticas: PENDIENTE DE DEFINIR CON JOHNNY.
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
