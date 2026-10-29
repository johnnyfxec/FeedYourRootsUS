#!/usr/bin/env python3
"""Publica un video en TikTok via Content Posting API (Direct Post), flujo FILE_UPLOAD.

Probado y funcionando end-to-end el 29-oct-2026 (Sandbox, app "FYR Content Publisher"):
init -> PUT del binario -> status fetch -> PUBLISH_COMPLETE confirmado.

POR QUE FILE_UPLOAD Y NO PULL_FROM_URL (decision deliberada, no un rodeo temporal):
  pull_by_url exige que el video este servido desde un dominio PROPIO ya verificado en
  developers.tiktok.com (URL properties) -- feedyourroots.us SI esta verificado, pero eso
  implicaria subir cada video a GitHub Pages antes de publicar (un commit/push extra por
  pieza) solo para que TikTok lo descargue desde ahi. FILE_UPLOAD evita ese paso por completo:
  se descarga el MP4 de Drive (ya publico, ver regla critica Seccion 0 del plan de
  publicacion) y se sube el binario directo a TikTok via PUT. Mas simple para este caso de uso
  especifico, aunque signifique mover el archivo dos veces (Drive -> aqui -> TikTok) en vez de
  una. Si en el futuro conviene cambiar a pull_by_url (p.ej. para evitar la descarga local),
  la verificacion de dominio ya esta hecha -- no hay que rehacer ese paso.

Uso:
    python3 tiktok_publish_video.py <ruta_al_mp4> "<titulo/caption>" [--publico]

    Sin --publico: publica como SELF_ONLY (privado) -- requerido mientras la app no este
    auditada (ver "unaudited_client_can_only_post_to_private_accounts" mas abajo) Y mientras
    la cuenta de TikTok este en modo privado (TikTok rechaza publicar en una cuenta publica
    desde un cliente sin auditar, incluso si privacy_level ya es SELF_ONLY -- confirmado con
    error real 29-oct-2026).

    Con --publico: intenta PUBLIC_TO_EVERYONE -- solo funcionara una vez que la app pase la
    auditoria de TikTok. Antes de eso dara privacy_level_option_mismatch.

REQUISITO PREVIO IMPORTANTE (confirmado empiricamente, no solo documentado): antes de poder
publicar CUALQUIER cosa, la cuenta de TikTok debe estar en modo PRIVADO (Configuracion y
privacidad > Privacidad > Cuenta privada) mientras la app siga sin auditar. Con la cuenta en
publico, el init devuelve "unaudited_client_can_only_post_to_private_accounts" sin importar
que privacy_level se pida. El cambio de privacidad tarda en propagar del lado de la API
(~1-2 min en la prueba real) despues de activarlo en la app -- confirmar con creator_info/query
que privacy_level_options ya NO incluya PUBLIC_TO_EVERYONE antes de reintentar.

Variables de entorno requeridas:
  TIKTOK_ACCESS_TOKEN (de tiktok_authorize_web.py -- expira en 24h, usar
  TIKTOK_REFRESH_TOKEN para renovar cuando haga falta -- refresh no implementado aun aqui)

Limites de archivo confirmados (doc oficial, media-transfer-guide):
  Video: maximo 4GB, MP4 (recomendado)/WebM/MOV, H.264 (recomendado)/H.265/VP8/VP9,
  23-60 FPS, 360-4096px alto/ancho, maximo 10 minutos.
  Un archivo <=64MB se sube en un solo chunk (chunk_size = video_size, total_chunk_count = 1).
  Mayor a 64MB debe fragmentarse (5-64MB por fragmento, el ultimo hasta 128MB) -- ESTE SCRIPT
  NO IMPLEMENTA FRAGMENTACION TODAVIA, solo sirve para archivos <=64MB. Las piezas de video de
  FYR (9:16, ~30-40s) rondan 20-30MB, asi que no es un problema actual, pero hay que agregar
  fragmentacion antes de usar esto con piezas mas largas.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

INIT_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
CREATOR_INFO_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"

MAX_SINGLE_CHUNK_BYTES = 64 * 1024 * 1024  # 64MB -- ver aviso de fragmentacion en el docstring


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
    if len(sys.argv) < 3:
        sys.exit("Uso: tiktok_publish_video.py <ruta_al_mp4> \"<titulo>\" [--publico]")

    video_path = sys.argv[1]
    title = sys.argv[2]
    publico = "--publico" in sys.argv[3:]

    token = os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        sys.exit("Falta TIKTOK_ACCESS_TOKEN en el entorno.")

    if not os.path.isfile(video_path):
        sys.exit(f"No existe el archivo: {video_path}")
    video_size = os.path.getsize(video_path)
    if video_size > MAX_SINGLE_CHUNK_BYTES:
        sys.exit(
            f"Archivo de {video_size} bytes supera el limite de chunk unico "
            f"({MAX_SINGLE_CHUNK_BYTES} bytes) -- este script no implementa fragmentacion "
            "todavia, ver docstring."
        )

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
            "private_accounts). Pon la cuenta en privado desde la app y espera 1-2 min a "
            "que propague antes de continuar."
        )

    privacy_level = "PUBLIC_TO_EVERYONE" if publico else "SELF_ONLY"

    print(f"Iniciando publicacion (FILE_UPLOAD, {video_size} bytes, privacy={privacy_level}) ...")
    init = _post_json(INIT_URL, token, {
        "post_info": {
            "title": title,
            "privacy_level": privacy_level,
            "disable_duet": True,
            "disable_stitch": True,
            "disable_comment": False,
            "video_cover_timestamp_ms": 1000,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": video_size,
            "total_chunk_count": 1,
        },
    })
    if init.get("error", {}).get("code") != "ok":
        sys.exit("init fallo: " + json.dumps(init)[:500])

    upload_url = init["data"]["upload_url"]
    publish_id = init["data"]["publish_id"]
    print("publish_id:", publish_id)

    print("Subiendo el binario (PUT) ...")
    with open(video_path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        upload_url,
        data=data,
        headers={
            "Content-Type": "video/mp4",
            "Content-Length": str(video_size),
            "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        sys.exit(f"Subida fallo con HTTP {e.code}: {e.read().decode()[:400]}")
    if code != 201:
        sys.exit(f"Subida devolvio HTTP {code} (se esperaba 201).")
    print("Subida completa (HTTP 201).")

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
