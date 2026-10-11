#!/usr/bin/env python3
"""Compone la portada 9:16 de un video con el motor de ensamblado.

Uso (desde la carpeta de la pieza): make_cover.py pieza_X.json

Para cada slide con la clave "portada" ({layout, texto_titulo, texto_subtitulo}):
  1. toma la imagen ya descargada en slide["imagen"] (la ilustracion 1:1 de la ventana),
  2. la compone con assemble (marco_grande_cuadrado + titulo + subtitulo),
  3. guarda el PNG 1080x1920 en el mismo slide["imagen"].
"""
import json
import os
import shutil
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
ASSEMBLE = os.path.join(REPO, "production", "scripts", "assemble")
ASSETS = os.path.join(REPO, "production", "assets_local")
sys.path.insert(0, ASSEMBLE)

from main import assemble_slide  # noqa: E402


def main():
    pieza = json.load(open(sys.argv[1], encoding="utf-8"))
    hechas = 0
    for s in pieza["slides"]:
        portada = s.get("portada")
        if not portada:
            continue
        src = s["imagen"]
        escena = "_portada_src_" + os.path.basename(src)
        shutil.copy(src, os.path.join(ASSETS, escena))
        slide = dict(portada)
        slide["imagen_escena"] = escena
        canvas, warnings = assemble_slide(slide, "9:16", ASSETS)
        canvas.convert("RGB").save(src)
        os.remove(os.path.join(ASSETS, escena))
        for w in warnings:
            print(f"  advertencia: {w}")
        print(f"✓ portada del slide {s['n']} compuesta -> {src}")
        hechas += 1
    if not hechas:
        print("(sin slides con 'portada')")


if __name__ == "__main__":
    main()
