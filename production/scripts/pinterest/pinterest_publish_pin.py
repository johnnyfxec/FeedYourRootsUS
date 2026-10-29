#!/usr/bin/env python3
"""Publica un Pin de imagen en Pinterest via API v5 (Standard access, produccion).

CONFIRMADO EN PRODUCCION (29-oct-2026): primer Pin real publicado con exito --
pin_id 1151725304742928915, board "Backyard Chickens & Bees Integration", imagen de
PZA_10.4 S5. El cuerpo del POST /v5/pins y GET /v5/boards funcionan tal como estaban
documentados (developers.pinterest.com/docs/content/update/ + referencia del SDK).

UNICA correccion real necesaria: Pinterest NO sigue redirects al leer media_source.url.
Un link de Drive tipo "drive.google.com/uc?export=download&id=X" responde 303 (redirige
a drive.usercontent.google.com/download?id=X&export=download) -- Meta SI sigue ese
redirect, Pinterest no, y falla con {"code":1,"message":"Sorry we could not fetch the
image."}. Este script ahora normaliza esa forma de URL automaticamente a la version
final (usercontent) antes de mandarla a la API, asi que no hace falta pensarlo en cada
corrida -- pero si se usa otra fuente de imagenes que tambien redirija, el mismo error
va a volver a aparecer.

Flujo:
  1. (si no se pasa --board-id) GET /v5/boards -> lista los boards de la cuenta,
     Johnny elige cual usar y lo pasa en la siguiente corrida con --board-id.
  2. POST /v5/pins con board_id + media_source (source_type=image_url) + title +
     description + link opcional -> crea y publica el Pin en un solo paso (Pinterest
     no tiene un flujo de 2 pasos tipo "container" como Instagram -- el pin queda
     visible de inmediato).

Uso:
    # Paso 1 (una sola vez, o si no te acuerdas el board_id):
    python3 pinterest_publish_pin.py --list-boards

    # Paso 2:
    python3 pinterest_publish_pin.py --board-id <ID> --title "<titulo>" \\
        --description "<descripcion>" --image-url <url_imagen> [--link <url_destino>]

Variables de entorno requeridas (ya en el .env real de Johnny, ninguna nueva):
  PINTEREST_ACCESS_TOKEN -- token de produccion (Standard access), Authorization: Bearer.
                            Si el .env todavia tiene el token de Sandbox (Trial access),
                            este script va a fallar -- reautorizar con
                            pinterest_authorize_web.py primero.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.pinterest.com/v5"

_DRIVE_UC_RE = re.compile(r"^https://drive\.google\.com/uc\?export=download&id=([^&]+)$")


def _normalize_image_url(url):
    """Pinterest no sigue el 303 redirect de drive.google.com/uc?export=download --
    reescribe esa forma a la URL final (drive.usercontent.google.com) antes de usarla.
    Cualquier otra URL se deja tal cual."""
    m = _DRIVE_UC_RE.match(url)
    if not m:
        return url
    file_id = m.group(1)
    nueva = f"https://drive.usercontent.google.com/download?id={file_id}&export=download"
    print(f"(normalizando URL de Drive para evitar el redirect que Pinterest no sigue: {nueva})")
    return nueva


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


def list_boards(token):
    print("Consultando GET /v5/boards ...")
    resp = _request("GET", "/boards", token)
    items = resp.get("items", [])
    if not items:
        sys.exit(
            "No se encontraron boards en la cuenta -- crea uno en Pinterest antes de "
            "publicar un pin, o revisa que el token sea el de la cuenta Business "
            "correcta."
        )
    print(f"\n{len(items)} board(s) encontrados:\n")
    for b in items:
        print(f"  id={b.get('id')}  name={b.get('name')!r}")
    print("\nUsa el id que corresponda con --board-id en la siguiente corrida.")


def create_pin(token, board_id, title, description, image_url, link):
    image_url = _normalize_image_url(image_url)
    body = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "media_source": {
            "source_type": "image_url",
            "url": image_url,
        },
    }
    if link:
        body["link"] = link

    print("Creando Pin ...")
    resp = _request("POST", "/pins", token, body)
    pin_id = resp.get("id")
    if not pin_id:
        sys.exit(f"La respuesta no trajo id de Pin: {json.dumps(resp)[:600]}")

    print(f"\nPUBLICADO con exito. pin_id: {pin_id}")
    print(f"Ver en: https://www.pinterest.com/pin/{pin_id}/")
    return pin_id


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list-boards", action="store_true", help="Lista los boards de la cuenta y termina.")
    parser.add_argument("--board-id", help="ID del board donde crear el Pin.")
    parser.add_argument("--title", help="Titulo del Pin.")
    parser.add_argument("--description", help="Descripcion del Pin.")
    parser.add_argument("--image-url", help="URL publica de la imagen (ej. link de descarga directa de Drive).")
    parser.add_argument("--link", default=None, help="URL de destino opcional al hacer clic en el Pin.")
    args = parser.parse_args()

    token = os.environ.get("PINTEREST_ACCESS_TOKEN")
    if not token:
        sys.exit("Falta PINTEREST_ACCESS_TOKEN en el entorno (ver .env).")

    if args.list_boards:
        list_boards(token)
        return

    faltantes = [
        nombre for nombre, val in [
            ("--board-id", args.board_id),
            ("--title", args.title),
            ("--description", args.description),
            ("--image-url", args.image_url),
        ] if not val
    ]
    if faltantes:
        sys.exit(
            "Faltan argumentos obligatorios: " + ", ".join(faltantes) +
            "\nUsa --list-boards primero si no tienes el board_id."
        )

    create_pin(token, args.board_id, args.title, args.description, args.image_url, args.link)


if __name__ == "__main__":
    main()
