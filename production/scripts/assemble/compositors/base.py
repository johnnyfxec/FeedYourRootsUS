# Compositor BASE -- layouts sin asset fijo (Seccion 2.5 de la arquitectura).
# full_bleed, solo_texto, texto_lateral. No usan ASSETS/WINDOWS/BBOX -- se
# componen directo con imagen de escena (crop-to-fill) y/o texto sobre
# fondo parchment solido.

import os
from PIL import Image, ImageDraw

from layout_specs import CANVAS, PARCHMENT, OVERLAY_ALPHA, usable_zone
from text_renderer import crop_to_fill, render_text_block


class CompositorError(Exception):
    pass


def _load_scene(imagen_escena, assets_dir):
    path = os.path.join(assets_dir, imagen_escena)
    if not os.path.exists(path):
        raise CompositorError(f"imagen de escena no encontrada: {path}")
    return Image.open(path).convert("RGB")


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _contain_fit(scene, box_w, box_h):
    """Escala `scene` completa (sin recortar) para que quepa DENTRO de
    box_w x box_h, preservando su proporcion real. Retorna (imagen_escalada,
    offset_x, offset_y) para pegarla centrada -- el espacio sobrante queda
    sin cubrir (el llamador lo rellena con el color de fondo)."""
    scale = min(box_w / scene.width, box_h / scene.height)
    new_w = round(scene.width * scale)
    new_h = round(scene.height * scale)
    resized = scene.resize((new_w, new_h), Image.LANCZOS)
    offset_x = (box_w - new_w) // 2
    offset_y = (box_h - new_h) // 2
    return resized, offset_x, offset_y


def _compose_full_bleed(canvas, slide, aspecto, assets_dir):
    """Full-bleed real: SOLO imagen, sin texto, nunca (decision de Johnny,
    13-sep-2026 -- ver FYR_Motor_Ensamblado_Arquitectura_v1.md Seccion 2.5).
    La imagen se contiene completa (modo contain, nunca crop) sobre el
    canvas entero, centrada, con el padding sobrante en PARCHMENT solido --
    nunca recorta contenido ni superpone overlay semi-transparente."""
    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("full_bleed requiere 'imagen_escena' en el slide")
    if slide.get("texto_overlay"):
        raise CompositorError("full_bleed no acepta texto_overlay -- es SOLO imagen (usar 'ventana_texto' si el slide necesita texto)")

    canvas_w = CANVAS[aspecto]["w"]
    canvas_h = CANVAS[aspecto]["h"]

    bg = Image.new("RGB", (canvas_w, canvas_h), _hex_to_rgb(PARCHMENT))
    canvas.paste(bg, (0, 0))

    scene = _load_scene(imagen_escena, assets_dir)
    scene_fit, off_x, off_y = _contain_fit(scene, canvas_w, canvas_h)
    canvas.paste(scene_fit, (off_x, off_y))

    return {"warnings": []}


def _compose_ventana_texto(canvas, slide, aspecto, assets_dir):
    """Imagen contenida (modo contain, nunca crop) en los dos tercios
    superiores del canvas + franja de texto SOLIDA (sin transparencia, sin
    imagen detras) en el tercio inferior. Decision de Johnny, 13-sep-2026:
    reemplaza el full_bleed-con-overlay original, que superponia texto
    semi-transparente sobre imagen recortada al canvas completo -- eso
    dejaba imagen visible detras del texto siempre, sin importar el
    contenido de la imagen (ver Arquitectura Seccion 2.5)."""
    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("ventana_texto requiere 'imagen_escena' en el slide")

    texto = slide.get("texto_overlay")
    if not texto:
        raise CompositorError("ventana_texto requiere 'texto_overlay' en el slide")

    canvas_w = CANVAS[aspecto]["w"]
    canvas_h = CANVAS[aspecto]["h"]

    bg = Image.new("RGB", (canvas_w, canvas_h), _hex_to_rgb(PARCHMENT))
    canvas.paste(bg, (0, 0))

    imagen_h = round(canvas_h * 2 / 3)
    scene = _load_scene(imagen_escena, assets_dir)
    scene_fit, off_x, off_y = _contain_fit(scene, canvas_w, imagen_h)
    canvas.paste(scene_fit, (off_x, off_y))

    franja_y = imagen_h
    franja_h = canvas_h - franja_y
    box = (round(canvas_w * 0.10), franja_y + 20, round(canvas_w * 0.80), franja_h - 40)
    r = render_text_block(canvas, texto, "cuerpo", box)

    warnings = []
    if r["truncated"]:
        warnings.append("texto_overlay truncado (BASE, ventana_texto)")
    return {"warnings": warnings}


def _compose_solo_texto(canvas, slide, aspecto, assets_dir):
    texto = slide.get("texto_cuerpo")
    if not texto:
        raise CompositorError("solo_texto requiere 'texto_cuerpo' en el slide")

    canvas_w = CANVAS[aspecto]["w"]
    margen_top, margen_bottom, usable_h = usable_zone(aspecto)

    box = (round(canvas_w * 0.12), round(margen_top), round(canvas_w * 0.76), round(usable_h))
    r = render_text_block(canvas, texto, "cuerpo", box)

    warnings = []
    if r["truncated"]:
        warnings.append("texto_cuerpo truncado (BASE, solo_texto)")
    return {"warnings": warnings}


def _compose_texto_lateral(canvas, slide, aspecto, assets_dir):
    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("texto_lateral requiere 'imagen_escena' en el slide")

    texto = slide.get("texto_cuerpo")
    if not texto:
        raise CompositorError("texto_lateral requiere 'texto_cuerpo' en el slide")

    lado = slide.get("lado_imagen", "izquierda")
    if lado not in ("izquierda", "derecha"):
        raise CompositorError(f"lado_imagen invalido: {lado} (validos: izquierda, derecha)")

    porcentaje_imagen = slide.get("porcentaje_imagen", 50)

    canvas_w = CANVAS[aspecto]["w"]
    margen_top, margen_bottom, usable_h = usable_zone(aspecto)
    img_w = round(canvas_w * (porcentaje_imagen / 100))
    ancla = slide.get("ancla_recorte", "center")

    scene = _load_scene(imagen_escena, assets_dir)
    scene_cropped = crop_to_fill(scene, img_w, round(usable_h), anchor=ancla)

    if lado == "izquierda":
        img_x = 0
        text_x0 = img_w + round(canvas_w * 0.06)
        text_x1 = canvas_w - round(canvas_w * 0.06)
        align = "left"
    else:
        img_x = canvas_w - img_w
        text_x0 = round(canvas_w * 0.06)
        text_x1 = img_x - round(canvas_w * 0.06)
        align = "right"

    canvas.paste(scene_cropped, (img_x, round(margen_top)))

    box = (text_x0, round(margen_top), text_x1 - text_x0, round(usable_h))
    r = render_text_block(canvas, texto, "cuerpo", box, align=align)

    warnings = []
    if r["truncated"]:
        warnings.append("texto_cuerpo truncado (BASE, texto_lateral)")
    return {"warnings": warnings}


def compose(canvas, slide, aspecto, assets_dir):
    layout = slide.get("layout")
    if layout == "full_bleed":
        return _compose_full_bleed(canvas, slide, aspecto, assets_dir)
    if layout == "ventana_texto":
        return _compose_ventana_texto(canvas, slide, aspecto, assets_dir)
    if layout == "solo_texto":
        return _compose_solo_texto(canvas, slide, aspecto, assets_dir)
    if layout == "texto_lateral":
        return _compose_texto_lateral(canvas, slide, aspecto, assets_dir)
    raise CompositorError(f"base.compose no maneja el layout: {layout}")
