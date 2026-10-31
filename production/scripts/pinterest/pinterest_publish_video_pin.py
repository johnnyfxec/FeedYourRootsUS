#!/usr/bin/env python3
"""Publica un Pin de VIDEO en Pinterest via API v5 -- flujo distinto y mas largo que
pinterest_publish_pin.py (Pin de imagen): Pinterest NO acepta una URL de video directa
en /v5/pins como si acepta image_url para imagenes. Hay que registrar la subida, subir
el binario a un bucket S3 de Pinterest, esperar a que procese, y recien ahi crear el Pin.

Verificado contra la documentacion oficial de Pinterest antes de escribir esto (API
Reference + guia "Create boards and Pins"), con un detalle real NO documentado como
obligatorio pero confirmado por reportes de la comunidad de desarrolladores de Pinterest:
omitir `cover_image_url` en el Pin de video da un 401 Unauthorized enganoso (en vez de un
400 descriptivo) -- este script lo exige siempre, nunca lo deja opcional.

Flujo real (4 pasos):
  1. POST /v5/media {"media_type": "video"} -> {media_id, upload_url, upload_parameters}
  2. POST multipart/form-data a upload_url (bucket S3 de Pinterest) -- TODOS los campos de
     upload_parameters tal cual vienen, en orden, + el binario del video como campo "file"
     al final (requisito de S3 presigned POST, no es orden arbitrario). Este script
     transmite el video en streaming (misma tecnica que youtube_publish_video.py y
     tiktok_publish_video.py) directo desde una URL publica de Drive -- nunca lo escribe
     a disco local.
  3. GET /v5/media/{media_id} en loop hasta status="succeeded" (registered -> processing
     -> succeeded/failed).
  4. POST /v5/pins con media_source={source_type: video_id, media_id, cover_image_url}.

Uso:
    python3 pinterest_publish_video_pin.py --board-id <ID> --title "<titulo>" \\
        --description "<descripcion>" --video-url <url_o_drive_link> \\
        --cover-image-url <url_imagen_portada> [--link <url_destino>]

Variables de entorno: identicas a pinterest_publish_pin.py (PINTEREST_ACCESS_TOKEN).
"""
import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

API_BASE = "https://api.pinterest.com/v5"
STREAM_BLOCK_BYTES = 1024 * 1024  # 1MB
MAX_POLL_ATTEMPTS = 15
POLL_SLEEP_SECONDS = 4

_DRIVE_UC_RE = re.compile(r"^https://drive\.google\.com/uc\?export=download&id=([^&]+)$")
_DRIVE_FILE_PATH_RE = re.compile(r"drive\.google\.com/file/d/([^/?]+)")


def _normalize_drive_url(url):
    """Mismo principio que _normalize_image_url() en pinterest_publish_pin.py -- acepta
    el link de 'ver' de Drive o el de descarga directa, siempre en la forma que de verdad
    sirve para leer el binario en streaming."""
    m = _DRIVE_FILE_PATH_RE.search(url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    if _DRIVE_UC_RE.match(url):
        return url
    return url


def _request(method, path, token, body=None):
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode())
        except Exception:
            sys.exit(f"HTTP {e.code} sin cuerpo JSON legible en {url}")
        sys.exit(f"HTTP {e.code} en {method} {path}: {json.dumps(err_body)[:600]}")


def _open_video_stream(url):
    url = _normalize_drive_url(url)
    print(f"Abriendo stream del video: {url}")
    resp = urllib.request.urlopen(url, timeout=60)
    size = resp.getheader("Content-Length")
    content_type = resp.getheader("Content-Type", "")
    if content_type.startswith("text/html"):
        resp.close()
        sys.exit(
            "La URL devolvio text/html en vez del binario -- el archivo de Drive "
            "probablemente no es publico (regla critica: solo Content_Pieces/ lo es)."
        )
    if not size:
        resp.close()
        sys.exit("La respuesta no trajo Content-Length -- no se puede armar la subida multipart.")
    return resp, int(size)


def _register_video_upload(token):
    print("Paso 1/4: registrando intento de subida (POST /v5/media) ...")
    resp = _request("POST", "/media", token, {"media_type": "video"})
    media_id = resp.get("media_id")
    upload_url = resp.get("upload_url")
    upload_parameters = resp.get("upload_parameters")
    if not media_id or not upload_url or not upload_parameters:
        sys.exit(f"POST /v5/media no devolvio los campos esperados: {json.dumps(resp)[:500]}")
    print(f"  -> media_id: {media_id}")
    return media_id, upload_url, upload_parameters


def _build_multipart_frame(upload_parameters, filename):
    """Arma el preambulo y epilogo del multipart/form-data -- el binario del video se
    transmite aparte, en streaming, entre ambos (ver _upload_to_s3). Los campos de
    upload_parameters van en el orden en que Pinterest los devolvio (dict de Python 3.7+
    preserva orden de insercion) -- S3 presigned POST es sensible a que 'file' sea el
    ULTIMO campo, no al orden de los demas."""
    boundary = uuid.uuid4().hex
    preamble = bytearray()
    for key, value in upload_parameters.items():
        preamble += f"--{boundary}\r\n".encode()
        preamble += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        preamble += f"{value}\r\n".encode()
    preamble += f"--{boundary}\r\n".encode()
    preamble += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
    preamble += b"Content-Type: video/mp4\r\n\r\n"
    epilogue = f"\r\n--{boundary}--\r\n".encode()
    return boundary, bytes(preamble), epilogue


def _upload_to_s3(upload_url, upload_parameters, video_stream, video_size):
    print(f"Paso 2/4: subiendo {video_size} bytes en streaming al bucket de Pinterest ...")
    boundary, preamble, epilogue = _build_multipart_frame(upload_parameters, "video.mp4")
    total_size = len(preamble) + video_size + len(epilogue)
    parsed = urllib.parse.urlsplit(upload_url)
    conn = http.client.HTTPSConnection(parsed.netloc, timeout=300)
    path = parsed.path + (("?" + parsed.query) if parsed.query else "")
    try:
        conn.putrequest("POST", path)
        conn.putheader("Content-Type", f"multipart/form-data; boundary={boundary}")
        conn.putheader("Content-Length", str(total_size))
        conn.endheaders()
        conn.send(preamble)
        while True:
            bloque = video_stream.read(STREAM_BLOCK_BYTES)
            if not bloque:
                break
            conn.send(bloque)
        conn.send(epilogue)
        resp = conn.getresponse()
        status = resp.status
        body = resp.read()
    finally:
        conn.close()
    if status not in (200, 201, 204):
        sys.exit(f"Subida a S3 fallo con HTTP {status}: {body.decode(errors='replace')[:500]}")
    print(f"  -> subida aceptada (HTTP {status}).")


def _poll_until_succeeded(token, media_id):
    print("Paso 3/4: esperando a que Pinterest procese el video (GET /v5/media/{id}) ...")
    for intento in range(MAX_POLL_ATTEMPTS):
        resp = _request("GET", f"/media/{media_id}", token)
        st = resp.get("status")
        print(f"  intento {intento + 1}: status={st}")
        if st == "succeeded":
            return
        if st == "failed":
            sys.exit(f"Pinterest marco el procesamiento como failed: {json.dumps(resp)[:500]}")
        time.sleep(POLL_SLEEP_SECONDS)
    sys.exit(f"El video no quedo 'succeeded' tras varios intentos -- media_id={media_id}")


def _create_video_pin(token, board_id, title, description, media_id, cover_image_url, link):
    print("Paso 4/4: creando el Pin de video ...")
    body = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "media_source": {
            "source_type": "video_id",
            "media_id": media_id,
            "cover_image_url": cover_image_url,
        },
    }
    if link:
        body["link"] = link
    resp = _request("POST", "/pins", token, body)
    pin_id = resp.get("id")
    if not pin_id:
        sys.exit(f"La respuesta no trajo id de Pin: {json.dumps(resp)[:600]}")
    print(f"\nPUBLICADO con exito. pin_id: {pin_id}")
    print(f"Ver en: https://www.pinterest.com/pin/{pin_id}/")
    return pin_id


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--board-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--video-url", required=True, help="URL publica del video (link de Drive, cualquiera de los 2 formatos).")
    parser.add_argument("--cover-image-url", required=True, help="URL publica de la imagen de portada (obligatoria para Pinterest, aunque su doc no lo marque claro).")
    parser.add_argument("--link", default=None)
    args = parser.parse_args()

    token = os.environ.get("PINTEREST_ACCESS_TOKEN")
    if not token:
        sys.exit("Falta PINTEREST_ACCESS_TOKEN en el entorno (ver .env).")

    media_id, upload_url, upload_parameters = _register_video_upload(token)

    video_stream, video_size = _open_video_stream(args.video_url)
    try:
        _upload_to_s3(upload_url, upload_parameters, video_stream, video_size)
    finally:
        video_stream.close()

    _poll_until_succeeded(token, media_id)

    _create_video_pin(token, args.board_id, args.title, args.description, media_id, args.cover_image_url, args.link)


if __name__ == "__main__":
    main()
