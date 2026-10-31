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
    python3 tiktok_publish_video.py <ruta_al_mp4_o_URL_publica_de_Drive> "<titulo/caption>" [--publico]

    La fuente acepta tanto una ruta local como una URL publica de Drive (link de "ver" o
    de descarga directa, cualquiera de los dos) -- en ese caso se transmite en streaming
    directo hacia TikTok, sin escribir el binario completo a disco en ningun punto
    intermedio (mismo patron que ya usa youtube_publish_video.py).

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
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

INIT_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
CREATOR_INFO_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"

MAX_SINGLE_CHUNK_BYTES = 64 * 1024 * 1024  # 64MB -- ver aviso de fragmentacion en el docstring
STREAM_BLOCK_BYTES = 1024 * 1024  # 1MB -- mismo bloque que youtube_publish_video.py

_DRIVE_FILE_PATH_RE = re.compile(r"drive\.google\.com/file/d/([^/?]+)")
_DRIVE_ID_PARAM_RE = re.compile(r"[?&]id=([^&]+)")


def _normalize_drive_url(url):
    """Mismo helper que youtube_publish_video.py -- acepta el link de 'ver' de Drive o
    el de descarga directa, siempre devuelve la forma de descarga directa."""
    m = _DRIVE_FILE_PATH_RE.search(url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    if "drive.google.com" in url and "export=download" not in url:
        m = _DRIVE_ID_PARAM_RE.search(url)
        if m:
            return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    return url


def _is_url(s):
    return s.startswith("http://") or s.startswith("https://")


def _open_source(source):
    """Devuelve (stream_legible, tamano_en_bytes). Si 'source' es una URL, abre un GET
    en streaming contra Drive (sin descargar a disco); si es una ruta local, abre el
    archivo. En ambos casos el llamador es responsable de cerrar el stream devuelto."""
    if _is_url(source):
        url = _normalize_drive_url(source)
        print(f"Abriendo stream desde Drive: {url}")
        resp = urllib.request.urlopen(url, timeout=60)
        size = resp.getheader("Content-Length")
        content_type = resp.getheader("Content-Type", "")
        if content_type.startswith("text/html"):
            resp.close()
            sys.exit(
                "La URL devolvio text/html en vez del binario -- casi siempre significa "
                "que el archivo de Drive NO es publico (regla critica Seccion 0: solo "
                "Content_Pieces/ es publico, Assets/ no)."
            )
        if not size:
            resp.close()
            sys.exit("La respuesta de Drive no trajo Content-Length -- no se puede continuar.")
        return resp, int(size)
    if not os.path.isfile(source):
        sys.exit(f"No existe el archivo: {source}")
    return open(source, "rb"), os.path.getsize(source)


def _put_stream(upload_url, source_stream, video_size):
    """PUT de bajo nivel (http.client) -- transmite el body bloque a bloque (1MB) en vez
    de juntar todo el binario en memoria antes de mandarlo, igual que
    youtube_publish_video.py::_put_stream(). Content-Range identico al que ya usaba la
    version anterior (bytes 0-N-1/N), TikTok lo exige aunque sea un solo chunk."""
    parsed = urllib.parse.urlsplit(upload_url)
    conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    conn = conn_cls(parsed.netloc, timeout=180)
    path = parsed.path + (("?" + parsed.query) if parsed.query else "")
    try:
        conn.putrequest("PUT", path)
        conn.putheader("Content-Type", "video/mp4")
        conn.putheader("Content-Length", str(video_size))
        conn.putheader("Content-Range", f"bytes 0-{video_size - 1}/{video_size}")
        conn.endheaders()
        while True:
            bloque = source_stream.read(STREAM_BLOCK_BYTES)
            if not bloque:
                break
            conn.send(bloque)
        resp = conn.getresponse()
        body = resp.read()
        status = resp.status
    finally:
        conn.close()
    return status, body


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
        sys.exit("Uso: tiktok_publish_video.py <ruta_al_mp4_o_URL_de_Drive> \"<titulo>\" [--publico]")

    source = sys.argv[1]
    title = sys.argv[2]
    publico = "--publico" in sys.argv[3:]

    token = os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        sys.exit("Falta TIKTOK_ACCESS_TOKEN en el entorno.")

    stream, video_size = _open_source(source)
    if video_size > MAX_SINGLE_CHUNK_BYTES:
        stream.close()
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

    print(f"Subiendo el binario en streaming (bloques de 1MB, {video_size} bytes) ...")
    try:
        code, body = _put_stream(upload_url, stream, video_size)
    finally:
        stream.close()
    if code != 201:
        sys.exit(f"Subida devolvio HTTP {code} (se esperaba 201): {body.decode(errors='replace')[:400]}")
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
