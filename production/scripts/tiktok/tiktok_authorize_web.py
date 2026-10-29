#!/usr/bin/env python3
"""Autorizacion OAuth de TikTok (Login Kit for Web) -- la hace Johnny, una sola vez, desde un
dispositivo con navegador. Mismo proposito que drive_authorize_web.py (Google) y
pinterest_authorize_web.py, pero con una diferencia estructural importante confirmada contra
developers.tiktok.com (login-kit-web, 28-oct-2026, no asumida de memoria):

  TikTok EXIGE que el redirect_uri sea una URL HTTPS absoluta ya registrada -- NO acepta
  "http://localhost:<puerto>" como si aceptan Google (clients "Desktop app") y Pinterest
  (URI fijo registrado, pero localhost es valido para ellos). Por eso este script NO levanta
  un servidor HTTP local para recibir el code automaticamente -- en vez de eso, el redirect_uri
  real es una pagina estatica publicada en el propio sitio de FYR (GitHub Pages):

      https://feedyourroots.us/tiktok-callback.html

  Esa pagina (repo: /tiktok-callback.html) muestra el "code" en pantalla tras la autorizacion
  para que Johnny lo copie y lo pegue aqui cuando el script se lo pida.

  Uso:
      python3 tiktok_authorize_web.py
      Imprime una URL. Johnny la abre en SU navegador, inicia sesion con la cuenta de TikTok
      de Feed Your Roots (en Sandbox: debe ser una "Target user" agregada de antemano en la
      consola de developers.tiktok.com > Sandbox > Target users) y autoriza. TikTok lo redirige
      a la pagina de callback publica, que muestra el "code". Johnny lo pega en la terminal;
      el script lo intercambia por access/refresh token.

NOTAS CONFIRMADAS CONTRA LA DOC OFICIAL (developers.tiktok.com), no asumidas de memoria:
  1. Endpoint de autorizacion: https://www.tiktok.com/v2/auth/authorize/
     (el antiguo /auth/authorize/ sin v2 esta deprecado).
  2. Endpoint de intercambio de token: POST https://open.tiktokapis.com/v2/oauth/token/
     con Content-Type: application/x-www-form-urlencoded.
  3. client_key y client_secret van en el BODY del POST (no en header Authorization Basic,
     a diferencia de Pinterest) -- confirmado en la doc de "Manage User Access Tokens".
  4. PKCE (code_challenge/code_verifier) esta documentado como obligatorio SOLO para Login Kit
     Desktop/Mobile -- la doc de Login Kit for Web no lo menciona, y el endpoint de token no
     pide code_verifier en sus parametros documentados. Este script NO implementa PKCE.
     OJO (si en el futuro TikTok lo exige tambien para Web): el code_challenge de TikTok se
     calcula como SHA256(code_verifier) codificado en HEX -- NO base64url como manda el
     estandar RFC 7636 -- confirmado contra developers.tiktok.com/doc/login-kit-desktop.
     Esto es una rareza real de TikTok, no un error de implementacion si se necesita despues.
  5. redirect_uri debe ser HTTPS absoluto, sin query params ni fragmento (#), y debe coincidir
     EXACTO con uno de los hasta 10 URIs registrados en la app (Products > Login Kit >
     Redirect URI).

Variables de entorno requeridas (de la app ya creada en developers.tiktok.com, pestaña
SANDBOX mientras no este auditada -- Client Key/Secret de Sandbox son DISTINTOS a los de
Production):
  TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET

El refresh token NUNCA se escribe en el repo -- solo se imprime en terminal, para que Johnny
decida donde guardarlo (su .env de Termux).
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

REDIRECT_URI = "https://feedyourroots.us/tiktok-callback.html"

# Scopes para fyr-publisher: user.info.basic (incluido en Login Kit, minimo exigido como
# dependencia) + video.publish (Direct Post -- publicacion directa sin pasar por borrador,
# scope de Content Posting API) + video.upload (fallback: sube como borrador si Direct Post
# no esta disponible para la cuenta/app todavia, p.ej. antes de pasar la auditoria).
SCOPES = ["user.info.basic", "video.publish", "video.upload"]
SCOPE = ",".join(SCOPES)

AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"


def _post_token(key, sec, code):
    data = urllib.parse.urlencode({
        "client_key": key,
        "client_secret": sec,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode() or "{}")


def main():
    key = os.environ.get("TIKTOK_CLIENT_KEY")
    sec = os.environ.get("TIKTOK_CLIENT_SECRET")
    if not key or not sec:
        sys.exit("Faltan TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET en el entorno.")

    params = {
        "client_key": key,
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "state": "fyr_publisher_setup",
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    print(f"ABRE ESTA URL EN TU NAVEGADOR:\n\n{url}\n")
    print("Inicia sesion con la cuenta de TikTok de Feed Your Roots (en Sandbox: debe estar")
    print("agregada como 'Target user' en developers.tiktok.com > Sandbox > Target users).")
    print(f"Tras autorizar, TikTok te redirige a {REDIRECT_URI}")
    print("Esa pagina te muestra el codigo -- cópialo y pégalo aquí.\n")

    code = input("Pega aqui el 'code' que te mostró la pagina: ").strip()
    if not code:
        sys.exit("No se ingreso ningun codigo.")

    tok = _post_token(key, sec, code)
    if "access_token" not in tok:
        sys.exit("TikTok no devolvio access_token: " + json.dumps(tok)[:500])

    print("\nTIKTOK_ACCESS_TOKEN=" + tok["access_token"])
    if "refresh_token" in tok:
        print("TIKTOK_REFRESH_TOKEN=" + tok["refresh_token"])
    print("scope concedido:", tok.get("scope"))
    print("expira en (segundos):", tok.get("expires_in"))
    print("open_id:", tok.get("open_id"))


if __name__ == "__main__":
    main()
