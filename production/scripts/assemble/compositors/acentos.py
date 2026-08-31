# Acentos Tipo D -- capa final superpuesta encima de cualquier slide ya
# resuelto (Seccion 2.4 de la arquitectura). Nunca se aplican solos, siempre
# sobre un layout principal ya compuesto (Tipo A, B, C o BASE).

import os
from PIL import Image

from layout_specs import ASSETS


class AccentError(Exception):
    pass


def _load_asset(layout, aspecto, assets_dir):
    if layout not in ASSETS or aspecto not in ASSETS[layout]:
        raise AccentError(f"asset no definido para acento={layout} aspecto={aspecto}")
    filename = ASSETS[layout][aspecto]
    path = os.path.join(assets_dir, filename)
    if not os.path.exists(path):
        raise AccentError(
            f"asset de acento no encontrado localmente: {path} "
            f"(image_fetcher.py deberia haberlo descargado de Drive antes de llegar aqui)"
        )
    return Image.open(path).convert("RGBA")


def apply_accent(canvas, accent_name, aspecto, assets_dir):
    if accent_name not in ("cordel_guia", "migas_progreso"):
        raise AccentError(f"acento invalido: {accent_name} (validos: cordel_guia, migas_progreso)")

    asset = _load_asset(accent_name, aspecto, assets_dir)
    canvas.alpha_composite(asset, (0, 0))
    return {"warnings": []}
