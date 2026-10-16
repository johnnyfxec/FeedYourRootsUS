#!/usr/bin/env python3
"""Sube el MP4 renderizado a la RAIZ del Drive de Johnny con verificacion de md5 (alcance drive.file).
Despues Claude lo mueve a Content_Pieces/PZA_x/fecha/ con el conector de Drive (update_file con parentId).

Uso (desde la carpeta de la pieza): upload_mp4.py pieza_X.json <variante>
Lee del JSON:  pieza_id (PZA_1.1).
Credenciales por entorno: GOOGLE_OAUTH_CLIENT_ID / _CLIENT_SECRET / _REFRESH_TOKEN (secretos de GitHub).
Escribe el resultado en $GITHUB_OUTPUT (drive_link) si existe.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "drive"))
from drive_client import Drive, link  # noqa: E402


def main():
    pj, variante = sys.argv[1], sys.argv[2]
    pieza = json.load(open(pj, encoding="utf-8"))
    mp4s = sorted(glob.glob(f"salida/*{variante}*.mp4")) or sorted(glob.glob("salida/*.mp4"))
    if not mp4s:
        sys.exit("No hay MP4 en salida/.")
    d = Drive()
    prefijo = f"FYR_{pieza['pieza_id']}_VIDEO_{variante}_9x16_v"
    usados = [int(m.group(1)) for f in d.find_prefix(prefijo) for m in [re.match(re.escape(prefijo) + r"(\d+)\.mp4$", f["name"])] if m]
    nombre = f"{prefijo}{max(usados, default=0) + 1}.mp4"
    info = d.upload(mp4s[0], None, nombre)
    url = link(info["id"])
    print(f"✓ subido {nombre} -> {url} (md5 verificado). Pendiente: moverlo a su carpeta (id {info['id']})")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"drive_link={url}\ndrive_name={nombre}\ndrive_id={info['id']}\n")


if __name__ == "__main__":
    main()
