#!/usr/bin/env python3
"""Publica un Reel en la Pagina de Facebook via la Reels Publishing API
(POST /{page_id}/video_reels, flujo de 3 fases: start -> upload -> finish).

Verificado contra la documentacion oficial de Meta (developers.facebook.com/docs/
video-api/guides/reels-publishing) antes de escribir este script -- no se adivino de
memoria. Dato no obvio que confirma esa doc: en la Fase 2, el flujo "hosted file" NO
manda la URL en el body ni en query string -- va como HEADER HTTP ("file_url: <url>"),
con "Authorization: OAuth <page_token>" (literal "OAuth ", no "Bearer"). Meta descarga el
video el mismo (misma logica que /photos?url=... y el carrusel de Instagram) -- este
script nunca descarga el binario, solo pasa la URL publica de Drive.

Fase 1 (start): POST /{page_id}/video_reels {"upload_phase":"start"} -> {video_id, upload_url}
Fase 2 (upload): POST <upload_url> con headers Authorization + file_url, sin body -> {"success": true}
Fase 3 (finish): POST /{page_id}/video_reels ?video_id=...&upload_phase=finish&video_state=
                 PUBLISHED&description=... -> {"success": true}

Entre Fase 2 y Fase 3 se consulta el estado (GET /{video_id}?fields=status) hasta que
uploading_phase.status == "complete", igual que meta_publish_carousel.py espera
status_code=FINISHED antes de publicar un carrusel -- publicar antes de tiempo puede
fallar aunque el video_id ya exista.

Mismo Page Access Token derivado del System User que ya usan meta_publish_facebook_photo.py
y meta_publish_facebook_carousel.py.

Uso:
    python3 meta_publish_facebook_reel.py "<descripcion/caption>" <url_video>

Variables de entorno: identicas al resto de la familia Facebook --
  META_SYSTEM_USER_TOKEN / META_PAGE_ID (ya en el .env real).
  META_PAGE_ACCESS_TOKEN -- opcional, se deriva solo si no esta.

Limites reales (doc oficial): max 30 publicaciones de Reels por pagina en una ventana
movil de 24h (aplica al propio POST .../video_reels de la Fase 3, no a esta cuenta en
general). URLs de fbcdn.net son rechazadas por Meta en el file_url de la Fase 2 -- debe
ser un host que Meta pueda alcanzar normalmente (Drive publico, como el resto del
pipeline, funciona).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GRAPH_BASE = "https://graph.facebook.com/v21.0"  # misma version que el resto de scripts de Meta
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


def _resolve_page_token(system_user_token, page_id):
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
        sys.exit('Uso: meta_publish_facebook_reel.py "<descripcion>" <url_video>')

    description, video_url = sys.argv[1], sys.argv[2]

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

    # ---------- Fase 1: iniciar la sesion ----------
    print("Fase 1/3: iniciando sesion (upload_phase=start) ...")
    start_resp = _post_form(f"{GRAPH_BASE}/{page_id}/video_reels", page_token, {
        "upload_phase": "start",
    })
    _fail_if_error(start_resp, "upload_phase=start")
    video_id = start_resp.get("video_id")
    upload_url = start_resp.get("upload_url")
    if not video_id or not upload_url:
        sys.exit(f"La respuesta no trajo video_id/upload_url: {json.dumps(start_resp)[:500]}")
    print(f"  -> video_id: {video_id}")

    # ---------- Fase 2: pasar la URL publica de Drive -- Meta la descarga el mismo.
    # OJO: va en HEADERS, no en el body ni en query string (confirmado contra la doc
    # oficial, no es intuitivo). Authorization literal "OAuth <token>", no "Bearer". ----------
    print("Fase 2/3: pasando file_url a Meta (headers, Meta descarga el video el mismo) ...")
    upload_req = urllib.request.Request(
        upload_url,
        data=None,
        headers={
            "Authorization": f"OAuth {page_token}",
            "file_url": video_url,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(upload_req, timeout=120) as r:
            upload_resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Fase 2 fallo con HTTP {e.code}: {e.read().decode()[:500]}")
    if not upload_resp.get("success"):
        sys.exit(f"Fase 2 no devolvio success=true: {json.dumps(upload_resp)[:500]}")
    print("  -> Meta acepto la URL, descargando/procesando ...")

    # ---------- Esperar a que termine la fase de subida antes de publicar ----------
    print("Esperando a que uploading_phase quede 'complete' ...")
    for intento in range(MAX_POLL_ATTEMPTS):
        status_resp = _get(f"{GRAPH_BASE}/{video_id}", page_token, {"fields": "status"})
        _fail_if_error(status_resp, "status check")
        uploading = status_resp.get("status", {}).get("uploading_phase", {})
        st = uploading.get("status")
        print(f"  intento {intento + 1}: uploading_phase.status={st}")
        if st == "complete":
            break
        time.sleep(POLL_SLEEP_SECONDS)
    else:
        sys.exit(
            "uploading_phase no quedo 'complete' tras varios intentos -- no se publica para "
            f"evitar un error de API. Revisar manualmente con video_id={video_id}"
        )

    # ---------- Fase 3: publicar ----------
    print("Fase 3/3: publicando (upload_phase=finish, video_state=PUBLISHED) ...")
    finish_resp = _post_form(f"{GRAPH_BASE}/{page_id}/video_reels", page_token, {
        "video_id": video_id,
        "upload_phase": "finish",
        "video_state": "PUBLISHED",
        "description": description,
    })
    _fail_if_error(finish_resp, "upload_phase=finish")
    if not finish_resp.get("success"):
        sys.exit(f"Fase 3 no devolvio success=true: {json.dumps(finish_resp)[:500]}")

    print(f"\nPUBLICADO con exito. video_id: {video_id}")

    permalink_resp = _get(f"{GRAPH_BASE}/{video_id}", page_token, {"fields": "permalink_url"})
    permalink = permalink_resp.get("permalink_url")
    if permalink:
        print(f"Ver en: {permalink}")
    else:
        print(f"No se pudo resolver permalink_url -- probar https://www.facebook.com/reel/{video_id}")


if __name__ == "__main__":
    main()
