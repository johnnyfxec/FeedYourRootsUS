#!/usr/bin/env python3
"""Publica un post multi-foto en la Pagina de Facebook via Graph API -- el equivalente
real de Facebook al carrusel de Instagram. NO es el mismo endpoint que una foto sola
(meta_publish_facebook_photo.py): ese es un flujo de 1 paso para 1 imagen; este es el
flujo real de 2 pasos para publicar varias imagenes como UN solo post agrupado.

Flujo real (mismo principio que el carrusel de Instagram: subir cada pieza sin publicarla
todavia, luego publicar UN solo post padre que las agrupa a todas):
  1. Por cada imagen: POST /{page_id}/photos con url=<url> + published=false -> devuelve
     un photo id (queda subida pero invisible, no es un post en si mismo).
  2. POST /{page_id}/feed con message=<caption> + attached_media=[{"media_fbid": id}, ...]
     (los ids del paso 1, uno por imagen) -> publica UN post que agrupa todas las fotos.

Mismo Page Access Token derivado del System User que ya usa meta_publish_facebook_photo.py
-- ver ese script para la explicacion completa de por que /photos y /feed exigen un Page
token clasico y no el META_SYSTEM_USER_TOKEN directo (que SI sirve para Instagram).

Uso:
    python3 meta_publish_facebook_carousel.py "<caption>" <url_img_1> <url_img_2> ... [url_img_N]

    Minimo 2 imagenes -- con 1 sola, usar meta_publish_facebook_photo.py (flujo distinto,
    un solo paso, no vale la pena pasar por /feed+attached_media para una sola foto).

Variables de entorno: identicas a meta_publish_facebook_photo.py --
  META_SYSTEM_USER_TOKEN / META_PAGE_ID (ya en el .env real).
  META_PAGE_ACCESS_TOKEN -- opcional, se deriva solo si no esta.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH_BASE = "https://graph.facebook.com/v21.0"  # misma version que el resto de scripts de Meta


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


def _resolve_page_token(system_user_token, page_id):
    """Deriva un Page Access Token permanente a partir del System User token -- mismo
    helper que meta_publish_facebook_photo.py."""
    if not page_id:
        sys.exit("Falta META_PAGE_ID en el entorno -- no se puede derivar el Page token.")
    detail = _get(f"{GRAPH_BASE}/{page_id}", system_user_token, {"fields": "access_token"})
    _fail_if_error(detail, f"derivar Page Access Token de la Pagina {page_id}")
    token = detail.get("access_token")
    if not token:
        sys.exit(f"La Pagina {page_id} no devolvio access_token -- revisar permisos del System User.")
    return token


def main():
    if len(sys.argv) < 4:
        sys.exit(
            'Uso: meta_publish_facebook_carousel.py "<caption>" <url_img_1> <url_img_2> '
            "[... mas urls]"
        )

    caption = sys.argv[1]
    image_urls = sys.argv[2:]
    if len(image_urls) < 2:
        sys.exit(
            f"Se dio {len(image_urls)} imagen -- con 1 sola usa "
            "meta_publish_facebook_photo.py (flujo distinto, mas simple)."
        )

    system_token = os.environ.get("META_SYSTEM_USER_TOKEN")
    if not system_token:
        sys.exit("Falta META_SYSTEM_USER_TOKEN en el entorno (ver .env).")
    page_id = os.environ.get("META_PAGE_ID")
    if not page_id:
        sys.exit("Falta META_PAGE_ID en el entorno (ver .env).")

    page_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
    if not page_token:
        print("META_PAGE_ACCESS_TOKEN no esta en el entorno -- derivandolo via META_SYSTEM_USER_TOKEN ...")
        page_token = _resolve_page_token(system_token, page_id)
        print("  -> Page Access Token derivado correctamente.")

    # ---------- Paso 1: subir cada foto sin publicarla (published=false) ----------
    media_fbids = []
    for idx, url in enumerate(image_urls, start=1):
        print(f"Subiendo foto {idx}/{len(image_urls)} (published=false) ...")
        resp = _post_form(f"{GRAPH_BASE}/{page_id}/photos", page_token, {
            "url": url,
            "published": "false",
        })
        _fail_if_error(resp, f"subir foto {idx} ({url})")
        photo_id = resp.get("id")
        if not photo_id:
            sys.exit(f"Foto {idx} no devolvio id: {json.dumps(resp)[:400]}")
        print(f"  -> {photo_id}")
        media_fbids.append(photo_id)

    # ---------- Paso 2: publicar UN post padre que agrupa todas las fotos ----------
    print(f"\nPublicando post con {len(media_fbids)} fotos adjuntas ...")
    attached_media = [{"media_fbid": pid} for pid in media_fbids]
    resp = _post_form(f"{GRAPH_BASE}/{page_id}/feed", page_token, {
        "message": caption,
        "attached_media": json.dumps(attached_media),
    })
    _fail_if_error(resp, "POST /feed")
    post_id = resp.get("id")
    if not post_id:
        sys.exit(f"La respuesta no trajo id de post: {json.dumps(resp)[:500]}")

    print(f"\nPUBLICADO con exito. post_id: {post_id}")

    permalink_resp = _get(f"{GRAPH_BASE}/{post_id}", page_token, {"fields": "permalink_url"})
    permalink = permalink_resp.get("permalink_url")
    if permalink:
        print(f"Ver en: {permalink}")
    else:
        print("No se pudo resolver el permalink automaticamente -- buscar el post mas reciente de la Pagina a mano.")


if __name__ == "__main__":
    main()
