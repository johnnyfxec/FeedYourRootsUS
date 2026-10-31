#!/usr/bin/env python3
"""Copia imagenes a una carpeta publica de feedyourroots.us (GitHub Pages) y espera a que
el sitio las sirva -- paso previo obligatorio antes de publicar fotos en TikTok.

POR QUE EXISTE ESTE PASO (no es arbitrario, ver tiktok_publish_photo.py): el endpoint de
fotos de la Content Posting API de TikTok (POST /v2/post/publish/content/init/) SOLO
acepta source=PULL_FROM_URL -- a diferencia de video, no tiene modo FILE_UPLOAD.
PULL_FROM_URL exige que la URL este en un dominio ya verificado en
developers.tiktok.com -- las URLs de Drive NO sirven para esto. El unico dominio
verificado del proyecto es feedyourroots.us (el mismo que ya usa el callback OAuth de
TikTok). Este script copia las imagenes ahi (comitea + empuja al repo, que ES el sitio),
y espera a que GitHub Pages las sirva antes de devolver las URLs finales.

ADVERTENCIA REAL CONFIRMADA (31-oct-2026): este repo corre Jekyll por defecto (no hay
`.nojekyll`), y Jekyll ignora SIN AVISAR cualquier carpeta que empiece con "_" (reservado
para _layouts, _includes, etc. de Jekyll) -- un archivo ahi queda en git pero JAMAS se
publica. Por eso DEST_DIR abajo no empieza con guion bajo -- no cambiarlo a una carpeta
con "_" sin agregar tambien un archivo .nojekyll en la raiz del repo.

SEGUNDA ADVERTENCIA REAL CONFIRMADA (31-oct-2026, PZA_3.1): TikTok Photo Mode RECHAZA PNG
-- solo acepta JPG/JPEG/WebP (confirmado contra documentacion oficial + fallo real,
fail_reason=file_format_check_failed). Las imagenes de FYR siempre son PNG
(`FYR_PZA_X_SY_4x5_v1.png`). Este script convierte TODO a JPEG antes de comitear, sin
importar el formato de origen -- nunca copiar/descargar el PNG tal cual para este uso
especifico (los demas scripts de publicacion SI pueden usar el PNG original, esto es
exclusivo del endpoint de fotos de TikTok).

Uso:
    python3 publish_images_to_pages.py <url_o_ruta_img_1> [url_o_ruta_img_2 ... hasta 35]

    Imprime, al final, una URL publica por imagen en el mismo orden dado -- usarlas como
    --photo-images en tiktok_publish_photo.py.

No borra nada al terminar -- la limpieza (revertir el commit, sacar las imagenes del
repo) queda como paso aparte y deliberado, no automatico.
"""
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid

try:
    from PIL import Image
except ImportError:
    sys.exit(
        "Falta Pillow (PIL) -- necesario para convertir a JPEG (TikTok Photo Mode "
        "rechaza PNG). Instalar con: pip install Pillow --break-system-packages"
    )

DEST_DIR = "production/scripts/tiktok/tmp-photos"  # SIN "_" -- ver advertencia en el docstring
BASE_URL = "https://feedyourroots.us"
MAX_POLL_ATTEMPTS = 20
POLL_SLEEP_SECONDS = 6
JPEG_QUALITY = 92


def _run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"Comando fallo ({' '.join(cmd)}):\n{result.stdout}\n{result.stderr}")
    return result.stdout


def _repo_root():
    return _run(["git", "rev-parse", "--show-toplevel"]).strip()


def _download(url, dest_path):
    print(f"Descargando {url} -> {dest_path}")
    urllib.request.urlretrieve(url, dest_path)


def _to_jpeg(src_path, dest_path):
    """Convierte cualquier imagen (PNG incluido) a JPEG real -- TikTok Photo Mode
    rechaza PNG. Descarta canal alpha si existe (JPEG no soporta transparencia, mismo
    criterio que ya usa el compositor del pipeline en otro punto)."""
    img = Image.open(src_path)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    img.save(dest_path, "JPEG", quality=JPEG_QUALITY)


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: publish_images_to_pages.py <url_o_ruta_img_1> [... hasta 35]")

    sources = sys.argv[1:]
    root = _repo_root()
    dest_dir_abs = os.path.join(root, DEST_DIR)
    os.makedirs(dest_dir_abs, exist_ok=True)

    batch_id = uuid.uuid4().hex[:8]
    rel_paths = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, src in enumerate(sources, start=1):
            raw_ext = ".jpg" if src.lower().split("?")[0].endswith((".jpg", ".jpeg")) else ".png"
            raw_path = os.path.join(tmpdir, f"raw_{idx}{raw_ext}")
            if src.startswith("http://") or src.startswith("https://"):
                _download(src, raw_path)
            else:
                _run(["cp", src, raw_path])

            fname = f"{batch_id}_{idx}.jpg"  # siempre .jpg -- ver _to_jpeg()
            dest_path = os.path.join(dest_dir_abs, fname)
            print(f"Convirtiendo a JPEG: {raw_path} -> {dest_path}")
            _to_jpeg(raw_path, dest_path)
            rel_paths.append(f"{DEST_DIR}/{fname}")

    print("\nComiteando y pusheando ...")
    _run(["git", "-C", root, "add"] + rel_paths)
    _run(["git", "-C", root, "commit", "-m", f"Imagenes temporales para prueba de TikTok Photo (lote {batch_id})"])
    _run(["git", "-C", root, "push", "origin", "HEAD"])

    urls = [f"{BASE_URL}/{p}" for p in rel_paths]
    print("\nEsperando a que GitHub Pages publique (puede tardar) ...")
    for intento in range(MAX_POLL_ATTEMPTS):
        all_ok = True
        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=15) as r:
                    if r.status != 200:
                        all_ok = False
            except Exception:
                all_ok = False
        print(f"  intento {intento + 1}: {'listas' if all_ok else 'esperando'}")
        if all_ok:
            break
        time.sleep(POLL_SLEEP_SECONDS)
    else:
        sys.exit("Las imagenes no quedaron publicadas en Pages tras varios intentos -- revisar manualmente.")

    print("\nURLs publicas finales (usar en tiktok_publish_photo.py):")
    for url in urls:
        print(url)


if __name__ == "__main__":
    main()
