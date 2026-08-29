# Compositor Tipo A -- Contenedor Escalable (Seccion 2.1 de la arquitectura).
# El marco se redimensiona segun % imagen/texto del slide; la ventana interior
# escala con el mismo factor. Aplica a: marco_grande, doble_marco.

import os
from PIL import Image

from layout_specs import (
    CANVAS, SAFE_PRACTICAL, ASSETS, WINDOWS, ROTATED_WINDOWS,
)
from text_renderer import crop_to_fill, render_text_block


class CompositorError(Exception):
    pass


def _usable_zone(aspecto):
    h = CANVAS[aspecto]["h"]
    top = h * SAFE_PRACTICAL["top"]
    bottom = h * SAFE_PRACTICAL["bottom"]
    return top, bottom, bottom - top


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


def _compose_marco_grande(canvas, slide, aspecto, assets_dir):
    porcentaje_imagen = slide.get("porcentaje_imagen")
    if porcentaje_imagen is None:
        raise CompositorError("marco_grande requiere 'porcentaje_imagen' en el slide")

    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("marco_grande requiere 'imagen_escena' en el slide")

    if "marco_grande" not in WINDOWS or aspecto not in WINDOWS["marco_grande"]:
        raise CompositorError(f"ventana no medida para marco_grande en aspecto {aspecto}")

    win = WINDOWS["marco_grande"][aspecto]
    asset_w, asset_h = win["asset_w"], win["asset_h"]

    margen_top, margen_bottom, usable_h = _usable_zone(aspecto)
    canvas_w = CANVAS[aspecto]["w"]

    porcentaje_texto = 100 - porcentaje_imagen
    image_zone_height = usable_h * (porcentaje_imagen / 100)
    text_zone_height = usable_h * (porcentaje_texto / 100)

    frame_scale = image_zone_height / asset_h
    frame_w_final = asset_w * frame_scale
    frame_h_final = asset_h * frame_scale

    frame_x = (canvas_w - frame_w_final) / 2
    frame_y = margen_top

    frame_asset = _load_asset("marco_grande", aspecto, assets_dir)
    frame_resized = frame_asset.resize(
        (round(frame_w_final), round(frame_h_final)), Image.LANCZOS
    )

    ventana_x = frame_x + (win["x"] * frame_scale)
    ventana_y = frame_y + (win["y"] * frame_scale)
    ventana_w = win["w"] * frame_scale
    ventana_h = win["h"] * frame_scale

    scene = _load_scene(imagen_escena, assets_dir)
    ancla = slide.get("ancla_recorte", "center")
    scene_cropped = crop_to_fill(scene, round(ventana_w), round(ventana_h), anchor=ancla)

    canvas.paste(scene_cropped, (round(ventana_x), round(ventana_y)))
    canvas.alpha_composite(frame_resized, (round(frame_x), round(frame_y)))

    texto_y_inicio = frame_y + frame_h_final + 20
    texto_box = (
        round(canvas_w * 0.08), round(texto_y_inicio),
        round(canvas_w * 0.84), round(text_zone_height - 20),
    )

    warnings = []
    titulo = slide.get("texto_titulo")
    subtitulo = slide.get("texto_subtitulo")
    if not titulo and not subtitulo:
        raise CompositorError("marco_grande requiere texto_titulo o texto_subtitulo")

    cursor_y = texto_box[1]
    box_w = texto_box[2] - texto_box[0]
    if titulo:
        remaining_h = texto_box[1] + (texto_box[3] - texto_box[1]) - cursor_y
        titulo_h = remaining_h if not subtitulo else remaining_h * 0.6
        r = render_text_block(canvas, titulo, "titulo", (texto_box[0], round(cursor_y), box_w, round(titulo_h)))
        if r["truncated"]:
            warnings.append("texto_titulo truncado (Tipo A, marco_grande)")
        cursor_y += titulo_h
    if subtitulo:
        remaining_h = texto_box[1] + (texto_box[3] - texto_box[1]) - cursor_y
        r = render_text_block(canvas, subtitulo, "subtitulo", (texto_box[0], round(cursor_y), box_w, round(remaining_h)))
        if r["truncated"]:
            warnings.append("texto_subtitulo truncado (Tipo A, marco_grande)")

    return {"warnings": warnings}


def _paste_rotated_scene(canvas, scene_img, window_spec, ancla="center"):
    w, h, angle, cx, cy = (
        window_spec["w"], window_spec["h"], window_spec["angle"],
        window_spec["cx"], window_spec["cy"],
    )
    # Margen extra 3% para que la imagen rotada cubra todo el hueco del marco
    # sin dejar bordes vacios en las esquinas (el recorte exacto medido deja
    # un remanente de un par de px al rotar).
    margin = 1.03
    cropped = crop_to_fill(scene_img, round(w * margin), round(h * margin), anchor=ancla).convert("RGBA")
    rotated = cropped.rotate(-angle, expand=True, resample=Image.BICUBIC)
    paste_x = round(cx - rotated.width / 2)
    paste_y = round(cy - rotated.height / 2)
    canvas.alpha_composite(rotated, (paste_x, paste_y))


def _compose_doble_marco(canvas, slide, aspecto, assets_dir):
    img1 = slide.get("imagen_escena_1")
    img2 = slide.get("imagen_escena_2")
    if not img1 or not img2:
        raise CompositorError("doble_marco requiere 'imagen_escena_1' e 'imagen_escena_2'")

    if "doble_marco" not in ROTATED_WINDOWS or aspecto not in ROTATED_WINDOWS["doble_marco"]:
        raise CompositorError(f"ventanas rotadas no medidas para doble_marco en aspecto {aspecto}")

    windows = ROTATED_WINDOWS["doble_marco"][aspecto]
    ancla = slide.get("ancla_recorte", "center")

    scene1 = _load_scene(img1, assets_dir)
    scene2 = _load_scene(img2, assets_dir)

    _paste_rotated_scene(canvas, scene1, windows["trasero"], ancla)
    _paste_rotated_scene(canvas, scene2, windows["frontal"], ancla)

    frame_asset = _load_asset("doble_marco", aspecto, assets_dir)
    canvas.alpha_composite(frame_asset, (0, 0))

    warnings = []
    titulo = slide.get("texto_titulo")
    if titulo:
        canvas_w = CANVAS[aspecto]["w"]
        margen_top, _, _ = _usable_zone(aspecto)
        box = (round(canvas_w * 0.08), 20, round(canvas_w * 0.84), round(margen_top - 30))
        r = render_text_block(canvas, titulo, "titulo", box)
        if r["truncated"]:
            warnings.append("texto_titulo truncado (Tipo A, doble_marco)")

    return {"warnings": warnings}


def compose(canvas, slide, aspecto, assets_dir):
    layout = slide.get("layout")
    if layout == "marco_grande":
        return _compose_marco_grande(canvas, slide, aspecto, assets_dir)
    if layout == "doble_marco":
        return _compose_doble_marco(canvas, slide, aspecto, assets_dir)
    raise CompositorError(f"tipo_a.compose no maneja el layout: {layout}")
