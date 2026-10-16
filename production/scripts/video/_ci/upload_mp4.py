#!/usr/bin/env python3
"""Sube el MP4 renderizado DIRECTO a su carpeta en Drive (OAuth de usuario, scope `drive` completo,
verificacion de md5) -- ver nota de diseno en drive_client.py. Ya no sube a la raiz ni deja paso manual
de moverlo: con el scope completo `parent_id` puede ser cualquier carpeta de Johnny.

Uso (desde la carpeta de la pieza): upload_mp4.py pieza_X.json <variante> [parent_id]
Lee del JSON:  pieza_id (PZA_1.1).
Sin parent_id: sube a la raiz de Mi unidad y lo dice explicitamente (hay que moverlo a mano).
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
    parent_id = sys.argv[3] if len(sys.argv) > 3 else None
    pieza = json.load(open(pj, encoding="utf-8"))
    mp4s = sorted(glob.glob(f"salida/*{variante}*.mp4")) or sorted(glob.glob("salida/*.mp4"))
    if not mp4s:
        sys.exit("No hay MP4 en salida/.")
    d = Drive()
    prefijo = f"FYR_{pieza['pieza_id']}_VIDEO_{variante}_9x16_v"
    usados = [int(m.group(1)) for f in d.find_prefix(prefijo, parent_id or "root") for m in [re.match(re.escape(prefijo) + r"(\d+)\.mp4$", f["name"])] if m]
    nombre = f"{prefijo}{max(usados, default=0) + 1}.mp4"
    info = d.upload(mp4s[0], parent_id, nombre)
    url = link(info["id"])
    destino = f"carpeta {parent_id}" if parent_id else "la raiz de Mi unidad (sin parent_id; hay que moverlo a mano)"

    # Verificacion real de llegada (16-oct-2026): d.upload() ya compara md5 contra lo que Drive guardo,
    # pero esto confirma ademas que el archivo quedo DONDE se esperaba -- no basta con que el script no
    # haya lanzado excepcion (lo que fallo en el piloto del 16-oct fue el `continue-on-error` del workflow
    # enmascarando un paso que nunca corria por falta de secretos, no este script; esta verificacion es
    # una segunda defensa para el caso en que la subida "funcione" pero el parent_id resulte equivocado).
    encontrados = d.find(nombre, parent_id or "root")
    coincide = [f for f in encontrados if f["id"] == info["id"]]
    if not coincide:
        sys.exit(f"✗ VERIFICACION FALLIDA: {nombre} se subio (id {info['id']}) pero no aparece al buscarlo "
                  f"en {destino}. No continuar como si hubiera terminado bien.")

    print(f"✓ subido {nombre} -> {url} (md5 verificado, presencia confirmada en {destino}).")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"drive_link={url}\ndrive_name={nombre}\ndrive_id={info['id']}\n")


if __name__ == "__main__":
    main()
