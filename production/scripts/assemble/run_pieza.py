#!/usr/bin/env python3
"""Orquestador del carrusel (Ruta A de FYR_Rutas_De_Produccion.md). NUNCA corre en Actions.

  python3 run_pieza.py importar  <dir_pieza> <trabajo> <resultado1.json> ...   # A8: valida y decodifica lo descargado con el conector de Drive
  python3 run_pieza.py ensamblar <dir_pieza> <trabajo> [--version N] [--config f.json] [--portada]   # A9
  python3 run_pieza.py subir     <dir_pieza> <trabajo> [parent_id]                                     # A11 (directo a parent_id vía OAuth de usuario; sin parent_id va a la raíz)

<dir_pieza> = production/pieces/PZA_x  (config.json + imagenes.json {nombre: drive_id})
<trabajo>   = carpeta temporal (assets/, out/, final/). Se puede borrar siempre: todo se regenera desde Drive.
Descarga: Claude llama `download_file_content` (conector de Drive) por cada ID de imagenes.json; el resultado queda
guardado en un archivo JSON {content(base64), id, title, mimeType} cuya ruta se pasa a `importar`.
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


def importar(pieza, work, archivos):
    """A8: toma los resultados guardados por `download_file_content` del conector de Drive
    ({content: base64, id, title, mimeType}), los decodifica a <trabajo>/assets/<nombre> y valida."""
    import base64
    from PIL import Image
    ids = json.load(open(os.path.join(pieza, "imagenes.json"), encoding="utf-8"))
    assets = os.path.join(work, "assets")
    os.makedirs(assets, exist_ok=True)
    sin_id = [n for n, i in ids.items() if not i]
    if sin_id:
        sys.exit(f"Sin ID de Drive (imagen aun no registrada en Assets): {sin_id}. Me detengo.")
    recibidos = set()
    for f in archivos:
        j = json.load(open(f, encoding="utf-8"))
        nombre = j["title"]
        if nombre not in ids:
            sys.exit(f"'{nombre}' no esta en imagenes.json. Me detengo.")
        if ids[nombre] != j["id"]:
            sys.exit(f"{nombre}: el ID descargado ({j['id']}) no es el de imagenes.json ({ids[nombre]}). Me detengo.")
        dest = os.path.join(assets, nombre)
        with open(dest, "wb") as out:
            out.write(base64.b64decode(j["content"]))
        w, h = Image.open(dest).size
        for k, r in RATIOS.items():
            if f"_{k}_" in nombre and abs(w / h - r) / r > 0.02:
                sys.exit(f"{nombre}: {w}x{h} no es {k} (proporcion {w/h:.3f}, esperada {r:.3f}). Me detengo.")
        recibidos.add(nombre)
        print(f"✓ {nombre} {w}x{h}")
    faltan = sorted(set(ids) - recibidos)
    if faltan:
        sys.exit(f"Faltan por descargar: {faltan}. Me detengo.")
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


def subir(pieza, work, parent_id=None):
    """A11: sube los PNG finales directo a `parent_id` (carpeta de la pieza en Drive, dada por Claude segun
    el brief), usando OAuth de usuario con scope `drive` completo (drive_client.py). Sin parent_id va a la
    raiz de Mi unidad y hay que moverlo despues a mano / con otro paso -- siempre que se conozca el ID de la
    carpeta de destino, pasarlo aqui evita ese paso extra."""
    from drive_client import Drive, link
    d = Drive()
    archivos = sorted(glob.glob(os.path.join(work, "final", "*.png")))
    if not archivos:
        sys.exit("No hay PNG en final/.")
    for f in archivos:
        info = d.upload(f, parent_id=parent_id)
        print(f"✓ {info['name']} id={info['id']} {link(info['id'])} (md5 verificado)")
    destino = f"carpeta {parent_id}" if parent_id else "la raiz de Mi unidad"
    print(f"{len(archivos)} PNG subidos directo a {destino}.")


if __name__ == "__main__":
    a = sys.argv
    if len(a) < 4 or a[1] not in ("importar", "ensamblar", "subir"):
        sys.exit(__doc__)
    if a[1] == "importar":
        importar(a[2], a[3], [x for x in a[4:] if not x.startswith("--")])
    elif a[1] == "ensamblar":
        ensamblar(a[2], a[3], int(_arg(a, "--version", 1)), _arg(a, "--config"), "--portada" in a)
    else:
        subir(a[2], a[3], a[4] if len(a) > 4 else None)
