# Compositor BASE -- layouts sin asset fijo (Seccion 2.5 de la arquitectura).
# full_bleed, solo_texto, texto_lateral. No usan ASSETS/WINDOWS/BBOX -- se
# componen directo con imagen de escena (crop-to-fill) y/o texto sobre
# fondo parchment solido.

import os
from PIL import Image, ImageDraw

from layout_specs import CANVAS, PARCHMENT, OVERLAY_ALPHA, usable_zone
from text_renderer import crop_to_fill, render_text_block, render_text_block_top


class CompositorError(Exception):
    pass


# Simbolo de marca C14 (FYR_Brand_Mark_Spec_v1.md). Es identidad de marca
# versionada en el repo (assets/brand/icons/), NO un asset local de Drive:
# se resuelve desde la raiz del repo y no depende de assets_dir (que apunta a
# production/assets_local/, carpeta ignorada por git con escenas y marcos).
# Fuente: el PNG de 1024px, en Root Black -- el mark solo se reduce, nunca se
# amplia. La proporcion se toma del contenido real (bbox del alpha), nunca se
# fuerza: la spec prohibe estirar el simbolo (Seccion 06).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
BRAND_MARK_PATH = os.path.join(REPO_ROOT, "assets", "brand", "icons", "FYR_C14_logo-frasco-1024px_1x1_v1.png")

MARK_CIERRE_H = 169  # px -- firma del slide de cierre (marca_cierre: true)
MARK_CHICO_H = 91    # px -- marca de esquina en el resto de slides
MARK_MARGEN = 24     # px de aire entre el mark y el borde del canvas / zona de texto

_BRAND_MARK_SRC = None


def _load_brand_mark_src():
    """Carga el PNG fuente una sola vez y lo recorta al bbox real del alpha
    (el lienzo es 1:1 con padding transparente). Cacheado en resolucion
    original: el escalado se hace por llamada, nunca encadenado."""
    global _BRAND_MARK_SRC
    if _BRAND_MARK_SRC is None:
        if not os.path.exists(BRAND_MARK_PATH):
            raise CompositorError(f"simbolo de marca no encontrado: {BRAND_MARK_PATH}")
        img = Image.open(BRAND_MARK_PATH).convert("RGBA")
        bbox = img.getchannel("A").getbbox()
        if bbox is None:
            raise CompositorError(f"simbolo de marca sin contenido (alpha vacio): {BRAND_MARK_PATH}")
        _BRAND_MARK_SRC = img.crop(bbox)
    return _BRAND_MARK_SRC


def _brand_mark(height):
    """Devuelve el simbolo escalado a `height` px de alto; el ancho sale de
    la proporcion real del contenido (nunca estirado). Usar .width/.height
    de la imagen devuelta para posicionarlo."""
    src = _load_brand_mark_src()
    width = round(src.width * height / src.height)
    return src.resize((width, height), Image.LANCZOS)


def _paste_brand_mark(canvas, mark, x, y):
    """Pega el mark usando su propio alpha como mascara."""
    canvas.paste(mark, (round(x), round(y)), mark)


def _zona_mark(mark_h):
    """Franja vertical que el texto debe ceder al pie del canvas usable para
    un mark de `mark_h` px: el margen inferior, el mark y el espacio de
    proteccion X (15.6% de la altura del simbolo, Spec Seccion 02)."""
    return MARK_MARGEN + mark_h + round(mark_h * 0.156)


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

    # Proporcion derivada (decision de Johnny, 13-sep-2026): la zona de
    # imagen se calcula a partir del ratio real de la imagen, no un
    # porcentaje fijo -- altura ideal = ancho del canvas / ratio de la
    # imagen. Topes: maximo 80% de imagen (deja piso de 20% para texto,
    # validado contra un caso real de imagen casi-4:5 -- ver Arquitectura
    # Seccion 2.5). Sin piso minimo de imagen: ninguna imagen del catalogo
    # actual es panoramica: si eso cambia, revisar este criterio.
    scene = _load_scene(imagen_escena, assets_dir)
    img_ratio = scene.width / scene.height
    altura_ideal = canvas_w / img_ratio
    imagen_h = round(min(altura_ideal, canvas_h * 0.80))

    scene_fit, off_x, off_y = _contain_fit(scene, canvas_w, imagen_h)
    canvas.paste(scene_fit, (off_x, off_y))

    franja_y = imagen_h
    franja_h = canvas_h - franja_y
    texto_y = franja_y + 20
    texto_max_h = franja_h - 40
    r = render_text_block_top(canvas, texto, "cuerpo", round(canvas_w * 0.10), texto_y, round(canvas_w * 0.80), texto_max_h)

    # Marca de esquina (inferior derecha) sobre el parchment liso de la franja,
    # anclada al borde inferior USABLE (en 9:16 el borde del canvas queda bajo
    # la interfaz de los reels). Queda fuera de la columna de texto (10%-90%).
    mark = _brand_mark(MARK_CHICO_H)
    _, margen_bottom, _ = usable_zone(aspecto)
    mark_x = canvas_w - MARK_MARGEN - mark.width
    mark_y = margen_bottom - MARK_MARGEN - mark.height
    _paste_brand_mark(canvas, mark, mark_x, mark_y)

    warnings = []
    if r["truncated"]:
        warnings.append("texto_overlay truncado (BASE, ventana_texto)")
    if mark_y - round(mark.height * 0.156) < off_y + scene_fit.height:
        warnings.append("marca de esquina demasiado cerca de la imagen (BASE, ventana_texto)")
    return {"warnings": warnings}


def _compose_solo_texto(canvas, slide, aspecto, assets_dir):
    texto = slide.get("texto_cuerpo")
    if not texto:
        raise CompositorError("solo_texto requiere 'texto_cuerpo' en el slide")

    canvas_w = CANVAS[aspecto]["w"]
    margen_top, margen_bottom, usable_h = usable_zone(aspecto)

    # Dos niveles de marca. Cierre (marca_cierre: true): firma grande centrada
    # al pie; el texto cede esa franja. Resto: mark chico en la esquina
    # inferior derecha, fuera de la columna de texto (12%-88%), sin restarle
    # espacio.
    es_cierre = bool(slide.get("marca_cierre"))
    mark = _brand_mark(MARK_CIERRE_H if es_cierre else MARK_CHICO_H)
    texto_h = usable_h - _zona_mark(MARK_CIERRE_H) if es_cierre else usable_h

    r = render_text_block_top(canvas, texto, "cuerpo", round(canvas_w * 0.12), round(margen_top), round(canvas_w * 0.76), round(texto_h))

    mark_x = (canvas_w - mark.width) / 2 if es_cierre else canvas_w - MARK_MARGEN - mark.width
    mark_y = margen_bottom - MARK_MARGEN - mark.height
    _paste_brand_mark(canvas, mark, mark_x, mark_y)

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

    # Marca de esquina del lado del TEXTO (nunca sobre la imagen): inferior
    # derecha si la imagen va a la izquierda, inferior izquierda si va a la
    # derecha. Aqui el mark comparte columna con el texto, asi que la columna
    # cede la franja inferior (el texto va anclado arriba, no se desplaza).
    mark = _brand_mark(MARK_CHICO_H)
    mark_x = canvas_w - MARK_MARGEN - mark.width if lado == "izquierda" else MARK_MARGEN
    mark_y = margen_bottom - MARK_MARGEN - mark.height

    r = render_text_block_top(canvas, texto, "cuerpo", text_x0, round(margen_top), text_x1 - text_x0, round(usable_h - _zona_mark(MARK_CHICO_H)), align=align)
    _paste_brand_mark(canvas, mark, mark_x, mark_y)

    warnings = []
    if r["truncated"]:
        warnings.append("texto_cuerpo truncado (BASE, texto_lateral)")
    return {"warnings": warnings}


def compose(canvas, slide, aspecto, assets_dir):
    layout = slide.get("layout")
    if slide.get("marca_cierre") and layout != "solo_texto":
        raise CompositorError(f"marca_cierre solo esta soportado en solo_texto (recibido: {layout}) -- el slide de cierre con firma de marca usa solo_texto")
    if layout == "full_bleed":
        return _compose_full_bleed(canvas, slide, aspecto, assets_dir)
    if layout == "ventana_texto":
        return _compose_ventana_texto(canvas, slide, aspecto, assets_dir)
    if layout == "solo_texto":
        return _compose_solo_texto(canvas, slide, aspecto, assets_dir)
    if layout == "texto_lateral":
        return _compose_texto_lateral(canvas, slide, aspecto, assets_dir)
    raise CompositorError(f"base.compose no maneja el layout: {layout}")
