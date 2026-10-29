#!/usr/bin/env python3
"""Publica un carrusel (2-10 imagenes) en Instagram via Graph API.

Flujo real de Meta para carruseles (documentado, probado aqui por primera vez con
PZA_10.4 -- 29-oct-2026):
  1. Por cada imagen: POST /<IG_USER_ID>/media con is_carousel_item=true -> devuelve
     un child container id (NO se publica nada todavia).
  2. POST /<IG_USER_ID>/media con media_type=CAROUSEL + children=[...] (los ids del
     paso 1) + caption -> devuelve el id del container padre.
  3. POST /<IG_USER_ID>/<parent_id>/media_publish -> publica el carrusel completo.

Cada imagen debe ser una URL publica alcanzable por los servidores de Meta (no un
archivo local) -- en FYR, las imagenes ya ensambladas viven en Google Drive con
permiso publico (ver regla critica Seccion 0 del plan de publicacion): usar la URL
de descarga directa, no el link de "ver" de Drive:
    https://drive.google.com/uc?export=download&id=<FILE_ID>

Uso:
    python3 meta_publish_carousel.py "<caption>" <url_img_1> <url_img_2> ... [url_img_N]

    Minimo 2 imagenes, maximo 10 (limite de Instagram para carruseles).

Variables de entorno requeridas:
  META_IG_ACCESS_TOKEN  -- token de acceso (page access token o user token con los
                           scopes instagram_basic + instagram_content_publish +
                           pages_show_list, segun como se haya generado)
  META_IG_USER_ID       -- ID numerico de la cuenta de Instagram Business/Creator
                           (no el @username) -- obtenerlo una vez via
                           GET /me/accounts y luego GET /<page_id>?fields=instagram_business_account
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GRAPH_BASE = "https://graph.facebook.com/v21.0"
MAX_POLL_ATTEMPTS = 10
POLL_SLEEP_SECONDS = 5


def _post_form(url, token, payload):
    body = dict(payload)
    body["access_token"] = token
    data = urllib.parse.urlencode(body).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except Exception:
            sys.exit(f"HTTP {e.code} sin cuerpo JSON legible en {url}")


def _get(url, token, params=None):
    q = dict(params or {})
    q["access_token"] = token
    full = f"{url}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(full, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except Exception:
            sys.exit(f"HTTP {e.code} sin cuerpo JSON legible en {url}")


def _fail_if_error(resp, contexto):
    if "error" in resp:
        sys.exit(f"{contexto} fallo: {json.dumps(resp)[:600]}")


def main():
    if len(sys.argv) < 4:
        sys.exit(
            'Uso: meta_publish_carousel.py "<caption>" <url_img_1> <url_img_2> '
            "[... hasta 10 urls]"
        )

    caption = sys.argv[1]
    image_urls = sys.argv[2:]

    if not (2 <= len(image_urls) <= 10):
        sys.exit(
            f"Instagram requiere entre 2 y 10 imagenes por carrusel -- se dieron "
            f"{len(image_urls)}."
        )

    token = os.environ.get("META_IG_ACCESS_TOKEN")
    ig_user_id = os.environ.get("META_IG_USER_ID")
    if not token:
        sys.exit("Falta META_IG_ACCESS_TOKEN en el entorno.")
    if not ig_user_id:
        sys.exit("Falta META_IG_USER_ID en el entorno.")

    media_url = f"{GRAPH_BASE}/{ig_user_id}/media"

    # ---------- Paso 1: un child container por imagen ----------
    child_ids = []
    for idx, url in enumerate(image_urls, start=1):
        print(f"Creando child container {idx}/{len(image_urls)} ...")
        resp = _post_form(media_url, token, {
            "image_url": url,
            "is_carousel_item": "true",
        })
        _fail_if_error(resp, f"child container {idx} ({url})")
        child_id = resp.get("id")
        if not child_id:
            sys.exit(f"child container {idx} no devolvio id: {json.dumps(resp)[:400]}")
        print(f"  -> {child_id}")
        child_ids.append(child_id)

    # ---------- Paso 2: container padre (CAROUSEL) ----------
    print(f"\nCreando container padre (CAROUSEL, {len(child_ids)} hijos) ...")
    parent_resp = _post_form(media_url, token, {
        "media_type": "CAROUSEL",
        "caption": caption,
        "children": ",".join(child_ids),
    })
    _fail_if_error(parent_resp, "container padre")
    parent_id = parent_resp.get("id")
    if not parent_id:
        sys.exit(f"container padre no devolvio id: {json.dumps(parent_resp)[:400]}")
    print(f"  -> parent_id: {parent_id}")

    # ---------- Paso 2.5: esperar a que el padre quede FINISHED ----------
    # Meta procesa el container de forma asincrona -- publicar antes de que su
    # status_code sea FINISHED devuelve "Media ID is not available" aunque el id
    # ya exista.
    status_url = f"{GRAPH_BASE}/{parent_id}"
    print("\nEsperando a que el container quede listo (status_code=FINISHED) ...")
    for intento in range(MAX_POLL_ATTEMPTS):
        status = _get(status_url, token, {"fields": "status_code"})
        _fail_if_error(status, "status check del container padre")
        code = status.get("status_code")
        print(f"  intento {intento + 1}: {code}")
        if code == "FINISHED":
            break
        if code == "ERROR":
            sys.exit("El container padre quedo en status_code=ERROR -- revisar manualmente.")
        time.sleep(POLL_SLEEP_SECONDS)
    else:
        sys.exit(
            "El container no quedo FINISHED tras varios intentos -- no se publica para "
            f"evitar un error de API. Revisar manualmente con parent_id={parent_id}"
        )

    # ---------- Paso 3: publicar ----------
    print("\nPublicando ...")
    publish_url = f"{GRAPH_BASE}/{ig_user_id}/media_publish"
    publish_resp = _post_form(publish_url, token, {"creation_id": parent_id})
    _fail_if_error(publish_resp, "media_publish")
    media_id = publish_resp.get("id")
    if not media_id:
        sys.exit(f"media_publish no devolvio id: {json.dumps(publish_resp)[:400]}")

    print(f"\nPUBLICADO con exito. media_id: {media_id}")
    print(f"Ver en: https://www.instagram.com/p/ (busca el post mas reciente de la cuenta)")


if __name__ == "__main__":
    main()
