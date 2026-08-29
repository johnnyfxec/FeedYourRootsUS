# Compositor Tipo B -- Contenedor Fijo (Seccion 2.2 de la arquitectura).
# El asset se usa a escala nativa (100%), colocado en su posicion medida en
# BBOX/WINDOWS -- no se re-centra ni se escala dinamicamente como Tipo A.
# Aplica a: etiqueta_colgante, nota_esquina, ventana_polaroid.

import os
from PIL import Image

from layout_specs import (
    CANVAS, ASSETS, ROTATED_WINDOWS, WINDOWS, TEXT_ZONES_TYPE_B,
)
from text_renderer import crop_to_fill, render_text_block, render_text_block_rotated


class CompositorError(Exception):
    pass


def _load_asset(layout, aspecto, assets_dir):
    if layout not in ASSETS or aspecto not in ASSETS[layout]:
        raise CompositorError(f"asset no definido para layout={layout} aspecto={aspecto}")
    filename = ASSETS[layout][aspecto]
    path = os.path.join(assets_dir, filename)
    if not os.path.exists(path):
        raise CompositorError(
            f"asset de layout no encontrado localmente: {path} "
            f"(image_fetcher.py deberia haberlo descargado de Drive antes de llegar aqui)"
        )
    return Image.open(path).convert("RGBA")


def _load_scene(imagen_escena, assets_dir):
    path = os.path.join(assets_dir, imagen_escena)
    if not os.path.exists(path):
        raise CompositorError(f"imagen de escena no encontrada: {path}")
    return Image.open(path).convert("RGB")


def _compose_texto_fijo(canvas, slide, aspecto, assets_dir, layout):
    """etiqueta_colgante y nota_esquina estan rotadas en el asset real
    (medido con medidor_esquinas.html, ~11-12 grados) -- el texto se
    renderiza en un lienzo aparte y se rota junto con el material, no se
    escribe derecho sobre una superficie inclinada."""
    texto = slide.get("texto_cuerpo")
    if not texto:
        raise CompositorError(f"{layout} requiere 'texto_cuerpo' en el slide")

    if layout not in ROTATED_WINDOWS or aspecto not in ROTATED_WINDOWS[layout]:
        raise CompositorError(f"geometria rotada no medida para {layout} en aspecto {aspecto}")
    if layout not in TEXT_ZONES_TYPE_B:
        raise CompositorError(f"zona de texto no definida para {layout}")

    geo = ROTATED_WINDOWS[layout][aspecto]
    zone = TEXT_ZONES_TYPE_B[layout]

    asset = _load_asset(layout, aspecto, assets_dir)
    canvas.alpha_composite(asset, (0, 0))

    text_w = geo["w"] * zone["w_frac"]
    text_h = geo["h"] * zone["h_frac"]

    r = render_text_block_rotated(
        canvas, texto, "cuerpo", text_w, text_h, geo["angle"], geo["cx"], geo["cy"]
    )

    warnings = []
    if r["truncated"]:
        warnings.append(f"texto_cuerpo truncado (Tipo B, {layout})")

    return {"warnings": warnings}


def _compose_ventana_polaroid(canvas, slide, aspecto, assets_dir):
    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("ventana_polaroid requiere 'imagen_escena' en el slide")

    if "ventana_polaroid" not in WINDOWS or aspecto not in WINDOWS["ventana_polaroid"]:
        raise CompositorError(f"ventana no medida para ventana_polaroid en aspecto {aspecto}")

    win = WINDOWS["ventana_polaroid"][aspecto]
    ancla = slide.get("ancla_recorte", "center")

    scene = _load_scene(imagen_escena, assets_dir)
    scene_cropped = crop_to_fill(scene, win["w"], win["h"], anchor=ancla)

    canvas.paste(scene_cropped, (win["x"], win["y"]))
    asset = _load_asset("ventana_polaroid", aspecto, assets_dir)
    canvas.alpha_composite(asset, (0, 0))

    warnings = []
    caption = slide.get("texto_cuerpo")
    if caption:
        canvas_w = CANVAS[aspecto]["w"]
        canvas_h = CANVAS[aspecto]["h"]
        caption_h = canvas_h * 0.10
        caption_y = canvas_h - caption_h
        box = (round(canvas_w * 0.10), round(caption_y), round(canvas_w * 0.80), round(caption_h))
        r = render_text_block(canvas, caption, "cuerpo", box)
        if r["truncated"]:
            warnings.append("texto_cuerpo (caption) truncado (Tipo B, ventana_polaroid)")

    return {"warnings": warnings}


def compose(canvas, slide, aspecto, assets_dir):
    layout = slide.get("layout")
    if layout in ("etiqueta_colgante", "nota_esquina"):
        return _compose_texto_fijo(canvas, slide, aspecto, assets_dir, layout)
    if layout == "ventana_polaroid":
        return _compose_ventana_polaroid(canvas, slide, aspecto, assets_dir)
    raise CompositorError(f"tipo_b.compose no maneja el layout: {layout}")
