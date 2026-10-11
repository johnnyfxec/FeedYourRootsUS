#!/usr/bin/env python3
"""Baja de Drive las imagenes de escena que pide un config de carrusel.

Uso: fetch_drive_images.py <config.json> <FOLDER_ID> <assets_dir>

Busca cada archivo por nombre dentro de la carpeta de fecha de la pieza
(FOLDER_ID) y lo guarda en assets_dir. Usa la cuenta de servicio de
GOOGLE_APPLICATION_CREDENTIALS (rol Lector). Falla si falta alguna imagen.
"""
import json
import os
import sys

import google.auth.transport.requests
from google.oauth2 import service_account

SCENE_FIELDS = ("imagen_escena", "imagen_escena_1", "imagen_escena_2")
API = "https://www.googleapis.com/drive/v3/files"


def main():
    cfg_path, folder_id, assets_dir = sys.argv[1:4]
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    names = sorted({s[f] for s in cfg["slides"] for f in SCENE_FIELDS if s.get(f)})
    creds = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    session = google.auth.transport.requests.AuthorizedSession(creds)
    os.makedirs(assets_dir, exist_ok=True)
    missing = []
    for name in names:
        q = f"name = '{name}' and '{folder_id}' in parents and trashed = false"
        r = session.get(API, params={
            "q": q, "fields": "files(id,name,size)", "orderBy": "modifiedTime desc",
            "supportsAllDrives": "true", "includeItemsFromAllDrives": "true", "pageSize": 5,
        })
        r.raise_for_status()
        files = r.json().get("files", [])
        if not files:
            print(f"✗ no encuentro {name} en la carpeta {folder_id}")
            missing.append(name)
            continue
        d = session.get(f"{API}/{files[0]['id']}", params={"alt": "media", "supportsAllDrives": "true"})
        d.raise_for_status()
        with open(os.path.join(assets_dir, name), "wb") as fh:
            fh.write(d.content)
        print(f"✓ {name} ({len(d.content) // 1024} KB)")
    if missing:
        print(f"Faltan {len(missing)} imagen(es). Me detengo.")
        sys.exit(1)


if __name__ == "__main__":
    main()
