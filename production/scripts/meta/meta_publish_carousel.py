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

Variables de entorno requeridas (ya en el .env real de Johnny, ninguna nueva que generar):
  META_SYSTEM_USER_TOKEN -- token MAESTRO generado en Business Manager > Configuracion del
                            negocio > Usuarios del sistema (NO el Explorador de la API Graph
                            -- ese da un token de usuario normal, de corta duracion). Este
                            NUNCA expira (expires_at=0, data_access_expires_at=0). Publica
                            directo en Instagram via graph.facebook.com.
  META_IG_BUSINESS_ID    -- ID de la cuenta de Instagram Business, ya resuelto de antemano
                            (GET /<META_PAGE_ID>?fields=instagram_business_account). NO es
                            el mismo ID que se ve en graph.instagram.com.

Si por algun motivo META_IG_BUSINESS_ID no estuviera en el entorno, este script lo resuelve
el mismo via META_PAGE_ID (tambien ya en .env) -> instagram_business_account, pero el camino
normal es que ya este puesto y no haga falta resolver nada en cada corrida.
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


def _resolve_ig_business_id(token, page_id):
    """Fallback solamente -- el camino normal es que META_IG_BUSINESS_ID ya este en .env."""
    if not page_id:
        sys.exit(
            "Faltan META_IG_BUSINESS_ID Y META_PAGE_ID en el entorno -- no hay forma de "
            "resolver la cuenta de Instagram. Revisa el .env."
        )
    detail = _get(f"{GRAPH_BASE}/{page_id}", token, {"fields": "instagram_business_account"})
    _fail_if_error(detail, f"resolver instagram_business_account de la Pagina {page_id}")
    ig = detail.get("instagram_business_account")
    if not ig or not ig.get("id"):
        sys.exit(f"La Pagina {page_id} no tiene una cuenta de Instagram Business vinculada.")
    return ig["id"]


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

    token = os.environ.get("META_SYSTEM_USER_TOKEN")
    if not token:
        sys.exit("Falta META_SYSTEM_USER_TOKEN en el entorno (ver .env).")

    ig_user_id = os.environ.get("META_IG_BUSINESS_ID")
    if not ig_user_id:
        print("META_IG_BUSINESS_ID no esta en el entorno -- resolviendolo via META_PAGE_ID ...")
        ig_user_id = _resolve_ig_business_id(token, os.environ.get("META_PAGE_ID"))
        print(f"  -> IG Business ID: {ig_user_id}")

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

    # ---------- Paso 4: resolver el permalink real ----------
    # El shortcode real de un post de Instagram (ej. DfFafzPjm2-) NO se puede derivar del
    # media_id numerico -- confirmado el 29-oct-2026 tras publicar PZA_10.4 (media_id
    # 17996701389021317, permalink real /p/DfFafzPjm2-/, sin relacion visible entre ambos).
    # Pedirselo a la API en vez de dejar que alguien lo busque a mano o lo adivine.
    permalink_resp = _get(f"{GRAPH_BASE}/{media_id}", token, {"fields": "permalink"})
    permalink = permalink_resp.get("permalink")
    if permalink:
        print(f"Ver en: {permalink}")
    else:
        print(
            "No se pudo resolver el permalink automaticamente -- buscar el post mas "
            "reciente de la cuenta a mano."
        )


if __name__ == "__main__":
    main()
