#!/usr/bin/env python3
"""Orquestador del carrusel (Ruta A de FYR_Rutas_De_Produccion.md). NUNCA corre en Actions.

  python3 run_pieza.py descargar <dir_pieza> <trabajo>            # A8: baja las imagenes por ID desde Drive
  python3 run_pieza.py ensamblar <dir_pieza> <trabajo> [--version N] [--config f.json] [--portada]   # A9
  python3 run_pieza.py subir     <dir_pieza> <trabajo> <carpeta_drive_id>                              # A11

<dir_pieza> = production/pieces/PZA_x  (config.json + imagenes.json {nombre: drive_id})
<trabajo>   = carpeta temporal (assets/, out/, final/). Se puede borrar siempre: todo se regenera desde Drive.
Opcion de prueba: --local-dir <dir> en `descargar` copia las imagenes por nombre en vez de bajarlas de Drive.
"""
import glob
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "drive"))

RATIOS = {"4x5": 0.8, "9x16": 9 / 16, "1x1": 1.0}
CANVAS = {"4:5": (1080, 1350), "9:16": (1080, 1920)}


def _arg(argv, flag, default=None):
    return argv[argv.index(flag) + 1] if flag in argv else default


def descargar(pieza, work, local_dir=None):
    from PIL import Image
    ids = json.load(open(os.path.join(pieza, "imagenes.json"), encoding="utf-8"))
    assets = os.path.join(work, "assets")
    os.makedirs(assets, exist_ok=True)
    sin_id = [n for n, i in ids.items() if not i and not local_dir]
    if sin_id:
        sys.exit(f"Sin ID de Drive (imagen aun no registrada en Assets): {sin_id}. Me detengo.")
    d = None
    if not local_dir:
        from drive_client import Drive
        d = Drive()
    for nombre, fid in ids.items():
        dest = os.path.join(assets, nombre)
        if local_dir:
            shutil.copy(os.path.join(local_dir, nombre), dest)
        else:
            meta = d.download(fid, dest)
            if meta["name"] != nombre:
                sys.exit(f"El ID {fid} es '{meta['name']}', no '{nombre}'. Me detengo.")
        w, h = Image.open(dest).size
        for k, r in RATIOS.items():
            if f"_{k}_" in nombre and abs(w / h - r) / r > 0.02:
                sys.exit(f"{nombre}: {w}x{h} no es {k} (proporcion {w/h:.3f}, esperada {r:.3f}). Me detengo.")
        print(f"✓ {nombre} {w}x{h}")
    for f in glob.glob(os.path.join(REPO, "production", "assets_local", "FYR_*")):
        shutil.copy(f, assets)
    print(f"✓ marcos y layouts copiados a {assets}")


def ensamblar(pieza, work, version=1, config=None, portada=False):
    from PIL import Image
    from main import assemble_pieza
    cfg_path = os.path.join(pieza, config or "config.json")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    out, final = os.path.join(work, "out"), os.path.join(work, "final")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(final, exist_ok=True)
    res = assemble_pieza(cfg_path, os.path.join(work, "assets"), out, version=version)
    if res["errors"]:
        sys.exit("El ensamblado tuvo errores; no se renombra nada.")
    asp = cfg["aspecto"].replace(":", "x")
    esperado = CANVAS[cfg["aspecto"]]
    nombres = []
    for f in res["exported"]:
        n = os.path.basename(f).split("_S")[-1].split("_v")[0]
        nombre = (f"FYR_{cfg['pieza_id']}_PORTADA_{asp}_v{version}.png" if portada
                  else f"FYR_{cfg['pieza_id']}_S{n}_{asp}_v{version}.png")
        im = Image.open(f)
        if im.size != esperado:
            sys.exit(f"{nombre}: {im.size}, esperado {esperado}.")
        shutil.copy(f, os.path.join(final, nombre))
        nombres.append(nombre)
    print("✓ listos para revisar en", final, ":", ", ".join(nombres))


def subir(pieza, work, carpeta):
    from drive_client import Drive, link
    d = Drive()
    archivos = sorted(glob.glob(os.path.join(work, "final", "*.png")))
    if not archivos:
        sys.exit("No hay PNG en final/.")
    for f in archivos:
        info = d.upload(f, carpeta)
        print(f"✓ {info['name']} {link(info['id'])} (md5 verificado)")
    en_drive = [x for x in d.ls(carpeta) if x["name"].lower().endswith(".png")]
    print(f"Carpeta con {len(en_drive)} PNG; subidos ahora: {len(archivos)}")


if __name__ == "__main__":
    a = sys.argv
    if len(a) < 4 or a[1] not in ("descargar", "ensamblar", "subir"):
        sys.exit(__doc__)
    if a[1] == "descargar":
        descargar(a[2], a[3], _arg(a, "--local-dir"))
    elif a[1] == "ensamblar":
        ensamblar(a[2], a[3], int(_arg(a, "--version", 1)), _arg(a, "--config"), "--portada" in a)
    else:
        subir(a[2], a[3], a[4])
