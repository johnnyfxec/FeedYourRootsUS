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
import time
import urllib.request
import uuid

DEST_DIR = "production/scripts/tiktok/tmp-photos"  # SIN "_" -- ver advertencia en el docstring
BASE_URL = "https://feedyourroots.us"
MAX_POLL_ATTEMPTS = 20
POLL_SLEEP_SECONDS = 6


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


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: publish_images_to_pages.py <url_o_ruta_img_1> [... hasta 35]")

    sources = sys.argv[1:]
    root = _repo_root()
    dest_dir_abs = os.path.join(root, DEST_DIR)
    os.makedirs(dest_dir_abs, exist_ok=True)

    batch_id = uuid.uuid4().hex[:8]
    rel_paths = []
    for idx, src in enumerate(sources, start=1):
        ext = ".jpg" if src.lower().split("?")[0].endswith((".jpg", ".jpeg")) else ".png"
        fname = f"{batch_id}_{idx}{ext}"
        dest_path = os.path.join(dest_dir_abs, fname)
        if src.startswith("http://") or src.startswith("https://"):
            _download(src, dest_path)
        else:
            _run(["cp", src, dest_path])
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
