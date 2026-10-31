#!/usr/bin/env python3
"""Publica un carrusel de fotos en TikTok via Content Posting API
(POST /v2/post/publish/content/init/, source=PULL_FROM_URL).

POR QUE PULL_FROM_URL Y NO FILE_UPLOAD (no hay eleccion aqui, a diferencia de video): el
endpoint de fotos SOLO acepta PULL_FROM_URL -- no existe modo FILE_UPLOAD para fotos en la
Content Posting API (confirmado contra la doc oficial, 31-oct-2026). Eso significa que las
URLs en --photo-images deben estar en un dominio YA VERIFICADO en developers.tiktok.com --
las URLs de Drive NO sirven para esto (no es el dominio verificado del proyecto). Correr
publish_images_to_pages.py primero para conseguir URLs validas en feedyourroots.us (el
unico dominio verificado) antes de usar este script.

Uso:
    python3 tiktok_publish_photo.py "<titulo>" "<descripcion>" [--publico] \\
        <url_img_1> <url_img_2> [... hasta 35]

    Sin --publico: privacy_level=SELF_ONLY, mismo criterio que tiktok_publish_video.py
    mientras la app no este auditada (unaudited_client_can_only_post_to_private_accounts).

Variables de entorno: identicas a tiktok_publish_video.py --
  TIKTOK_ACCESS_TOKEN (expira en 24h, sin refresh automatico implementado aqui todavia).

Limite real (doc oficial): hasta 35 imagenes por carrusel.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

INIT_URL = "https://open.tiktokapis.com/v2/post/publish/content/init/"
STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
CREATOR_INFO_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"

MAX_PHOTOS = 35  # limite real documentado del endpoint de fotos


def _post_json(url, token, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode() or "{}")


def main():
    if len(sys.argv) < 4:
        sys.exit(
            'Uso: tiktok_publish_photo.py "<titulo>" "<descripcion>" [--publico] '
            "<url_img_1> [... hasta 35]"
        )

    title = sys.argv[1]
    description = sys.argv[2]
    rest = sys.argv[3:]
    publico = "--publico" in rest
    photo_images = [a for a in rest if a != "--publico"]

    if not (1 <= len(photo_images) <= MAX_PHOTOS):
        sys.exit(f"TikTok permite hasta {MAX_PHOTOS} fotos -- se dieron {len(photo_images)}.")

    token = os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        sys.exit("Falta TIKTOK_ACCESS_TOKEN en el entorno.")

    print("Verificando estado de la cuenta (creator_info/query) ...")
    info = _post_json(CREATOR_INFO_URL, token, {})
    if info.get("error", {}).get("code") != "ok":
        sys.exit("creator_info/query fallo: " + json.dumps(info)[:400])
    opts = info["data"]["privacy_level_options"]
    print("privacy_level_options actuales:", opts)
    if "PUBLIC_TO_EVERYONE" in opts:
        print(
            "AVISO: la cuenta parece estar en modo PUBLICO. Mientras la app no este "
            "auditada, TikTok rechazara la publicacion (unaudited_client_can_only_post_to_"
            "private_accounts). Pon la cuenta en privado y espera 1-2 min a que propague."
        )

    privacy_level = "PUBLIC_TO_EVERYONE" if publico else "SELF_ONLY"

    print(f"\nIniciando publicacion ({len(photo_images)} fotos, privacy={privacy_level}) ...")
    init = _post_json(INIT_URL, token, {
        "post_info": {
            "title": title,
            "description": description,
            "privacy_level": privacy_level,
            "disable_comment": False,
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "photo_cover_index": 0,
            "photo_images": photo_images,
        },
        "post_mode": "DIRECT_POST",
        "media_type": "PHOTO",
    })
    if init.get("error", {}).get("code") != "ok":
        sys.exit("init fallo: " + json.dumps(init)[:500])

    publish_id = init["data"]["publish_id"]
    print("publish_id:", publish_id)

    print("Consultando estado de publicacion ...")
    for intento in range(10):
        status = _post_json(STATUS_URL, token, {"publish_id": publish_id})
        st = status.get("data", {}).get("status")
        print(f"  intento {intento + 1}: {st}")
        if st == "PUBLISH_COMPLETE":
            print("\nPUBLICADO con exito. publish_id:", publish_id)
            return
        if st == "FAILED":
            sys.exit("Publicacion fallida: " + json.dumps(status)[:500])
        time.sleep(5)

    print("\nNo se confirmo PUBLISH_COMPLETE tras varios intentos -- revisar manualmente con "
          f"publish_id={publish_id}")


if __name__ == "__main__":
    main()
