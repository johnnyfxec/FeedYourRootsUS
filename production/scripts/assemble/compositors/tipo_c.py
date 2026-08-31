# Compositor Tipo C -- Generado Completo (Seccion 2.3 de la arquitectura).
# Sin composicion real: el PNG ya viene completo desde Gemini (imagen_final
# en el JSON), el script solo valida tamano exacto y lo coloca tal cual.
# Aplica a: palabra_acuarela, tachado.

import os
from PIL import Image

from layout_specs import CANVAS


class CompositorError(Exception):
    pass


def compose(canvas, slide, aspecto, assets_dir):
    layout = slide.get("layout")
    imagen_final = slide.get("imagen_final")
    if not imagen_final:
        raise CompositorError(f"{layout} requiere 'imagen_final' en el slide")

    path = os.path.join(assets_dir, imagen_final)
    if not os.path.exists(path):
        raise CompositorError(f"imagen_final no encontrada: {path}")

    img = Image.open(path).convert("RGBA")
    expected_w = CANVAS[aspecto]["w"]
    expected_h = CANVAS[aspecto]["h"]

    if img.size != (expected_w, expected_h):
        raise CompositorError(
            f"{layout}: imagen_final mide {img.size}, se esperaba "
            f"({expected_w}, {expected_h}) -- error de generacion en Gemini, "
            f"no se corrige con estiramiento (Seccion 2.3, paso 1)"
        )

    canvas.paste(img, (0, 0))
    return {"warnings": [], "canvas": canvas}
