#!/usr/bin/env python3
"""Publica un Reel en Instagram via Graph API (media_type=REELS).

Mismo flujo de 3 pasos que ya usa meta_publish_carousel.py (container -> poll FINISHED ->
publish), pero con UN solo container (no child+parent como el carrusel, un Reel no se
arma de piezas). Verificado contra la documentacion oficial de Meta antes de escribir
esto -- un detalle real que no es obvio y que SI importa: sin `share_to_feed=true`, el
Reel publica solo en la pestaña Reels, no aparece en el feed normal de la cuenta (mismo
comportamiento que ya tienen los carruseles, que siempre caen en feed) -- este script lo
pone en true por defecto, con --solo-reels para desactivarlo si alguna vez hace falta.

Mismo META_SYSTEM_USER_TOKEN directo que ya usa meta_publish_carousel.py (Instagram NO
necesita el Page token derivado que si exige Facebook).

Uso:
    python3 meta_publish_instagram_reel.py "<caption>" <url_video> [--solo-reels]

    Sin --solo-reels: share_to_feed=true (aparece en feed Y en Reels, default).
    Con --solo-reels: share_to_feed=false (solo en la pestana Reels).

Variables de entorno: identicas a meta_publish_carousel.py --
  META_SYSTEM_USER_TOKEN (obligatoria), META_IG_BUSINESS_ID (se resuelve via META_PAGE_ID
  si no esta, mismo fallback que el script de carrusel).

Especificaciones reales del video (doc oficial, Reel Specifications): aspect ratio
0.01:1-10:1 (recomendado 9:16), bitrate video max 25Mbps VBR, audio 128kbps, duracion
3s-15min. Las piezas de FYR (9:16, ~30-40s) caen comodas dentro de todos estos limites.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GRAPH_BASE = "https://graph.facebook.com/v21.0"  # misma version que meta_publish_carousel.py
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
    """Mismo fallback que meta_publish_carousel.py -- el camino normal es que
    META_IG_BUSINESS_ID ya este en .env."""
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
    if len(sys.argv) < 3:
        sys.exit('Uso: meta_publish_instagram_reel.py "<caption>" <url_video> [--solo-reels]')

    caption = sys.argv[1]
    video_url = sys.argv[2]
    share_to_feed = "--solo-reels" not in sys.argv[3:]

    token = os.environ.get("META_SYSTEM_USER_TOKEN")
    if not token:
        sys.exit("Falta META_SYSTEM_USER_TOKEN en el entorno (ver .env).")

    ig_user_id = os.environ.get("META_IG_BUSINESS_ID")
    if not ig_user_id:
        print("META_IG_BUSINESS_ID no esta en el entorno -- resolviendolo via META_PAGE_ID ...")
        ig_user_id = _resolve_ig_business_id(token, os.environ.get("META_PAGE_ID"))
        print(f"  -> IG Business ID: {ig_user_id}")

    media_url = f"{GRAPH_BASE}/{ig_user_id}/media"

    # ---------- Paso 1: crear el container del Reel (uno solo, no hay children) ----------
    print(f"Creando container REELS (share_to_feed={share_to_feed}) ...")
    resp = _post_form(media_url, token, {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true" if share_to_feed else "false",
    })
    _fail_if_error(resp, "container REELS")
    container_id = resp.get("id")
    if not container_id:
        sys.exit(f"container REELS no devolvio id: {json.dumps(resp)[:400]}")
    print(f"  -> container_id: {container_id}")

    # ---------- Paso 2: esperar a que quede FINISHED (los videos tardan mas que las
    # imagenes del carrusel -- Meta tiene que descargar y procesar el archivo) ----------
    status_url = f"{GRAPH_BASE}/{container_id}"
    print("\nEsperando a que el container quede listo (status_code=FINISHED) ...")
    for intento in range(MAX_POLL_ATTEMPTS):
        status = _get(status_url, token, {"fields": "status_code"})
        _fail_if_error(status, "status check del container")
        code = status.get("status_code")
        print(f"  intento {intento + 1}: {code}")
        if code == "FINISHED":
            break
        if code == "ERROR":
            sys.exit("El container quedo en status_code=ERROR -- revisar manualmente.")
        time.sleep(POLL_SLEEP_SECONDS)
    else:
        sys.exit(
            "El container no quedo FINISHED tras varios intentos -- no se publica para "
            f"evitar un error de API. Revisar manualmente con container_id={container_id}"
        )

    # ---------- Paso 3: publicar ----------
    print("\nPublicando ...")
    publish_url = f"{GRAPH_BASE}/{ig_user_id}/media_publish"
    publish_resp = _post_form(publish_url, token, {"creation_id": container_id})
    _fail_if_error(publish_resp, "media_publish")
    media_id = publish_resp.get("id")
    if not media_id:
        sys.exit(f"media_publish no devolvio id: {json.dumps(publish_resp)[:400]}")

    print(f"\nPUBLICADO con exito. media_id: {media_id}")

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
