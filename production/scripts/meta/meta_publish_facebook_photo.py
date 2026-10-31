#!/usr/bin/env python3
"""Publica una foto en la Pagina de Facebook via Graph API (POST /{page_id}/photos).

Formaliza una sesion previa de troubleshooting manual (nunca llego a git -- vivia como
curls sueltos en otra conversacion) que resolvio el problema real: el endpoint /photos de
una Pagina exige un PAGE ACCESS TOKEN clasico (permisos pages_manage_posts), no el
META_SYSTEM_USER_TOKEN directo que SI sirve para Instagram -- usarlo tal cual contra
/photos falla con error de permiso (publish_actions). La solucion no es generar un token
nuevo a mano cada vez: el propio System User token puede DERIVAR un Page token permanente
(GET /{page_id}?fields=access_token, autenticado con el System User), que hereda la
no-expiracion del System User -- nunca hay que renovarlo via login ni OAuth. Mismo patron
de fallback que _resolve_ig_business_id() en meta_publish_carousel.py.

Confirmado funcionando end-to-end en la sesion original: imagen tomada directo de una URL
publica de Drive (sin descarga local), post real en la Pagina "Feed Your Roots US".

Alcance de esta version (deliberado, no un descuido): publica UNA foto por corrida. El
carrusel multi-foto de Facebook (/feed + attached_media, varios /photos con
published=false encadenados a un /feed) todavia no esta probado end-to-end -- queda
pendiente igual que el modo Reel de Instagram, el Pin de video de Pinterest y el modo
foto/carrusel de TikTok (ver Frente 1 de la reverificacion).

Uso:
    python3 meta_publish_facebook_photo.py "<caption>" <url_imagen>

Variables de entorno requeridas (ya en el .env real):
  META_SYSTEM_USER_TOKEN -- mismo token maestro que ya usa meta_publish_carousel.py.
  META_PAGE_ID           -- ID numerico de la Pagina de Facebook (ya en el .env).
  META_PAGE_ACCESS_TOKEN -- opcional. Si esta en el entorno se usa directo (mas rapido);
                            si no esta, este script lo deriva el mismo via
                            META_SYSTEM_USER_TOKEN + META_PAGE_ID.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH_BASE = "https://graph.facebook.com/v21.0"  # misma version que meta_publish_carousel.py


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
    """Deriva un Page Access Token permanente a partir del System User token -- hereda
    la no-expiracion, nunca hay que volver a autorizar nada a mano."""
    if not page_id:
        sys.exit("Falta META_PAGE_ID en el entorno -- no se puede derivar el Page token.")
    detail = _get(f"{GRAPH_BASE}/{page_id}", system_user_token, {"fields": "access_token"})
    _fail_if_error(detail, f"derivar Page Access Token de la Pagina {page_id}")
    token = detail.get("access_token")
    if not token:
        sys.exit(f"La Pagina {page_id} no devolvio access_token -- revisar permisos del System User.")
    return token


def main():
    if len(sys.argv) != 3:
        sys.exit('Uso: meta_publish_facebook_photo.py "<caption>" <url_imagen>')

    caption, image_url = sys.argv[1], sys.argv[2]

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

    print("Publicando foto en la Pagina ...")
    resp = _post_form(f"{GRAPH_BASE}/{page_id}/photos", page_token, {
        "url": image_url,
        "caption": caption,
    })
    _fail_if_error(resp, "POST /photos")
    photo_id = resp.get("id")
    post_id = resp.get("post_id")
    if not post_id:
        sys.exit(f"La respuesta no trajo post_id: {json.dumps(resp)[:500]}")

    print(f"\nPUBLICADO con exito. photo_id: {photo_id}  post_id: {post_id}")

    permalink_resp = _get(f"{GRAPH_BASE}/{post_id}", page_token, {"fields": "permalink_url"})
    permalink = permalink_resp.get("permalink_url")
    if permalink:
        print(f"Ver en: {permalink}")
    else:
        print("No se pudo resolver el permalink automaticamente -- buscar el post mas reciente de la Pagina a mano.")


if __name__ == "__main__":
    main()
