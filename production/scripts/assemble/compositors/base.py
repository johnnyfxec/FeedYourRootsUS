# Compositor BASE -- layouts sin asset fijo (Seccion 2.5 de la arquitectura).
# full_bleed, ventana_texto, solo_texto, texto_lateral, lockup_cierre. No usan ASSETS/WINDOWS/BBOX -- se
# componen directo con imagen de escena (crop-to-fill) y/o texto sobre
# fondo parchment solido.

import os
from PIL import Image, ImageDraw

from layout_specs import CANVAS, PARCHMENT, OVERLAY_ALPHA, usable_zone
from text_renderer import render_text_block, crop_to_fill


class CompositorError(Exception):
    pass


# Simbolo de marca C14 (FYR_Brand_Mark_Spec_v1.md). Es identidad de marca
# versionada en el repo (assets/brand/), NO un asset local de Drive: se
# resuelve desde la raiz del repo y no depende de assets_dir (que apunta a
# production/assets_local/, carpeta ignorada por git con escenas y marcos).
# Fuente: PNG de 1024px, Root Black -- el mark solo se reduce, nunca se
# amplia. La proporcion se toma del contenido real (bbox del alpha), nunca se
# fuerza: la spec prohibe estirar el simbolo (Seccion 06).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
BRAND_MARK_PATH = os.path.join(REPO_ROOT, "assets", "brand", "icons", "FYR_C14_logo-frasco-1024px_1x1_v1.png")
LOCKUP_VERTICAL_PATH = os.path.join(REPO_ROOT, "assets", "brand", "lockups-vertical", "FYR_C14_lockup-vertical_1x1_v1.png")

# Decision de Johnny (11-oct-2026): el icono vive SOLO en carruseles 4:5, en
# slides secundarias (nunca portada), abajo al centro. En 9:16 no hay icono
# (la interfaz de las plataformas lo taparia); la marca entra en video solo
# con el layout lockup_cierre cuando el guion necesita nombrarla.
MARK_H = 91          # px -- alto del icono (spec: minimo 32 px)
MARK_GAP = 38        # px de aire entre el contenido y el icono (>= X = 15.6% de MARK_H)
LOCKUP_W = 620       # px -- ancho del lockup vertical en lockup_cierre
VENTANA_IMG_MAX = {"4:5": 2 / 3, "9:16": 3 / 4}   # tope de la zona de imagen de ventana_texto (900 px en 4:5; 1440 en 9:16, deja el 25% inferior al texto)
VENTANA_PAD = 16     # px de aire arriba/abajo de la franja de texto de ventana_texto
POSICIONES_TEXTO = ("centro", "tercio_superior")
# Decision de Johnny (11-oct-2026): los espacios se rellenan siempre. Gemini
# no entrega ratios exactos (4:5 sale 928x1152 = 0.806; 9:16 sale 768x1376 =
# 0.558), asi que una imagen que difiere <= 2% del espacio se rellena
# recortando lo minimo (nunca quedan bandas). Si difiere mas, NO se recorta en
# silencio (cortaria contenido): se contiene entera y se avisa con "RATIO:"
# para regenerar la imagen con la proporcion correcta.
RATIO_TOL = 0.02
VENTANA_RATIO_ESPERADO = {"4:5": 4 / 5, "9:16": 3 / 4}   # proporcion a pedir a Gemini para ventana_texto
LATERAL_IMG_W = 540  # px -- ancho de la imagen de texto_lateral (50% del canvas)
LATERAL_IMG_H = 960  # px -- alto: proporcion 9:16 exacta, que se pide tal cual a Gemini

_BRAND_MARK_SRC = None
_LOCKUP_SRC = None


def _load_trimmed(path, nombre):
    """Carga un PNG de marca y lo recorta al bbox real del alpha (los
    lienzos son 1:1 con padding transparente). Cacheado en resolucion
    original: el escalado se hace por llamada, nunca encadenado."""
    if not os.path.exists(path):
        raise CompositorError(f"{nombre} no encontrado: {path}")
    img = Image.open(path).convert("RGBA")
    bbox = img.getchannel("A").getbbox()
    if bbox is None:
        raise CompositorError(f"{nombre} sin contenido (alpha vacio): {path}")
    return img.crop(bbox)


def _brand_mark(height):
    """Icono escalado a `height` px de alto; el ancho sale de la proporcion
    real del contenido (nunca estirado)."""
    global _BRAND_MARK_SRC
    if _BRAND_MARK_SRC is None:
        _BRAND_MARK_SRC = _load_trimmed(BRAND_MARK_PATH, "simbolo de marca")
    src = _BRAND_MARK_SRC
    return src.resize((round(src.width * height / src.height), height), Image.LANCZOS)


def _lockup_vertical(width):
    """Lockup vertical escalado a `width` px de ancho, proporcion real."""
    global _LOCKUP_SRC
    if _LOCKUP_SRC is None:
        _LOCKUP_SRC = _load_trimmed(LOCKUP_VERTICAL_PATH, "lockup vertical")
    src = _LOCKUP_SRC
    return src.resize((width, round(src.height * width / src.width)), Image.LANCZOS)


def _paste_brand_mark(canvas, mark, x, y):
    """Pega el mark usando su propio alpha como mascara."""
    canvas.paste(mark, (round(x), round(y)), mark)


def _zona_contenido(canvas, aspecto):
    """Zona vertical (top, bottom) disponible para el contenido del slide.
    En 4:5 pega el icono abajo al centro (anclado al margen inferior
    minimo) y el contenido cede la franja que ocupa; en 9:16 no hay icono
    y el contenido llega hasta el borde inferior de la zona usable."""
    margen_top, margen_bottom, _ = usable_zone(aspecto)
    if aspecto != "4:5":
        return margen_top, margen_bottom
    canvas_w = CANVAS[aspecto]["w"]
    mark = _brand_mark(MARK_H)
    mark_y = margen_bottom - mark.height
    _paste_brand_mark(canvas, mark, (canvas_w - mark.width) / 2, mark_y)
    return margen_top, mark_y - MARK_GAP


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


def _colocar_imagen(scene, box_w, box_h, nombre, warnings, esperado=None):
    """Prepara `scene` para el espacio box_w x box_h. Retorna (imagen,
    offset_x, offset_y) para pegarla dentro del espacio.
    - ratio dentro de RATIO_TOL del espacio -> rellena (recorte minimo).
    - si no -> contain completo (sin recortar contenido).
    `esperado` es el ratio que se pidio a Gemini para ese layout (por defecto,
    el del espacio); si la imagen se aparta de el mas de RATIO_TOL se agrega
    un aviso "RATIO:" a `warnings`."""
    ratio = scene.width / scene.height
    ratio_box = box_w / box_h
    ratio_esp = esperado if esperado else ratio_box
    if abs(ratio / ratio_esp - 1) > RATIO_TOL:
        warnings.append(
            f"RATIO: {nombre} llego {scene.width}x{scene.height} ({ratio:.3f}) y el layout espera {ratio_esp:.3f} "
            f"(tolerancia {RATIO_TOL:.0%}) -- regenerar la imagen con la proporcion correcta")
    if abs(ratio / ratio_box - 1) <= RATIO_TOL:
        return crop_to_fill(scene, box_w, box_h), 0, 0
    return _contain_fit(scene, box_w, box_h)


def _compose_full_bleed(canvas, slide, aspecto, assets_dir):
    """Full-bleed real: SOLO imagen, sin texto, nunca (decision de Johnny,
    13-sep-2026 -- ver FYR_Motor_Ensamblado_Arquitectura_v1.md Seccion 2.5).
    La imagen llena el canvas entero (recorte minimo si el ratio difiere
    <= RATIO_TOL; si difiere mas se contiene completa con padding PARCHMENT y
    aviso RATIO:) -- nunca superpone overlay semi-transparente."""
    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("full_bleed requiere 'imagen_escena' en el slide")
    if slide.get("texto_overlay"):
        raise CompositorError("full_bleed no acepta texto_overlay -- es SOLO imagen (usar 'ventana_texto' si el slide necesita texto)")

    canvas_w = CANVAS[aspecto]["w"]
    canvas_h = CANVAS[aspecto]["h"]

    bg = Image.new("RGB", (canvas_w, canvas_h), _hex_to_rgb(PARCHMENT))
    canvas.paste(bg, (0, 0))

    warnings = []
    scene = _load_scene(imagen_escena, assets_dir)
    scene_fit, off_x, off_y = _colocar_imagen(scene, canvas_w, canvas_h, "full_bleed", warnings)
    canvas.paste(scene_fit, (off_x, off_y))

    return {"warnings": warnings}


def _compose_ventana_texto(canvas, slide, aspecto, assets_dir):
    """Imagen arriba (se rellena su espacio; ver RATIO_TOL) + franja de texto
    SOLIDA (sin transparencia, sin imagen detras) debajo. Decision de Johnny,
    13-sep-2026: reemplaza el full_bleed-con-overlay original (ver
    Arquitectura Seccion 2.5). Ajuste del 11-oct-2026: la zona de imagen
    llega hasta 2/3 del alto en 4:5 (900 px) y hasta 3/4 en 9:16 (1440 px,
    el 25% inferior queda para el texto), y el texto va
    centrado verticalmente en la franja entre la imagen y el icono (4:5) o
    el borde inferior del canvas (9:16, sin icono)."""
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

    # Proporcion derivada (decision de Johnny, 13-sep-2026): la altura de la
    # imagen sale del ratio real (ancho del canvas / ratio), con tope de 2/3
    # del alto del canvas (2/3 en 4:5, 3/4 en 9:16). Si la imagen es panoramica queda
    # mas baja y el texto gana espacio.
    scene = _load_scene(imagen_escena, assets_dir)
    img_ratio = scene.width / scene.height
    altura_ideal = canvas_w / img_ratio
    imagen_h = round(min(altura_ideal, canvas_h * VENTANA_IMG_MAX[aspecto]))

    warnings = []
    scene_fit, off_x, off_y = _colocar_imagen(scene, canvas_w, imagen_h, "ventana_texto", warnings, esperado=VENTANA_RATIO_ESPERADO[aspecto])
    canvas.paste(scene_fit, (off_x, off_y))

    _, zona_bottom = _zona_contenido(canvas, aspecto)
    if aspecto == "9:16":
        # Decision de Johnny (11-oct-2026): el texto se centra en TODO el
        # espacio que deja la imagen (hasta el borde del canvas), para que
        # no quede vacio debajo. Ojo: ese centro (~y=1680) cae dentro de la
        # zona que la interfaz de reels/TikTok suele tapar (limite duro 83.3%
        # = y 1600).
        zona_bottom = canvas_h
    franja_top = off_y + scene_fit.height + VENTANA_PAD
    franja_h = round(zona_bottom - VENTANA_PAD - franja_top)

    if franja_h < 100:
        warnings.append(f"franja de texto muy baja ({franja_h}px) (BASE, ventana_texto)")
    r = render_text_block(canvas, texto, "cuerpo", (round(canvas_w * 0.10), franja_top, round(canvas_w * 0.80), max(franja_h, 1)))
    if r["truncated"]:
        warnings.append("texto_overlay truncado (BASE, ventana_texto)")
    return {"warnings": warnings}


def _compose_solo_texto(canvas, slide, aspecto, assets_dir):
    """Texto sin imagen, centrado. `posicion_texto`: 'centro' (default) lo
    centra en la zona de contenido (sobre el icono en 4:5); 'tercio_superior'
    centra el bloque sobre la linea del primer tercio del canvas (variante
    de variedad, decision de Johnny 11-oct-2026)."""
    texto = slide.get("texto_cuerpo")
    if not texto:
        raise CompositorError("solo_texto requiere 'texto_cuerpo' en el slide")

    posicion = slide.get("posicion_texto", "centro")
    if posicion not in POSICIONES_TEXTO:
        raise CompositorError(f"posicion_texto invalida: {posicion} (validas: {', '.join(POSICIONES_TEXTO)})")

    canvas_w = CANVAS[aspecto]["w"]
    canvas_h = CANVAS[aspecto]["h"]
    zona_top, zona_bottom = _zona_contenido(canvas, aspecto)

    if posicion == "centro":
        box_y, box_h = zona_top, zona_bottom - zona_top
    else:
        cy = canvas_h / 3
        half = min(cy - zona_top, zona_bottom - cy)
        box_y, box_h = cy - half, 2 * half

    r = render_text_block(canvas, texto, "cuerpo", (round(canvas_w * 0.12), round(box_y), round(canvas_w * 0.76), round(box_h)))

    warnings = []
    if r["truncated"]:
        warnings.append("texto_cuerpo truncado (BASE, solo_texto)")
    return {"warnings": warnings}


def _compose_texto_lateral(canvas, slide, aspecto, assets_dir):
    """Imagen a un costado + texto centrado en altura respecto a ella.
    La imagen es 9:16 y llena 540x960 (recorte minimo solo si el ratio difiere
    <= RATIO_TOL; si difiere mas se muestra completa y avisa RATIO:): es la
    proporcion que se pide a Gemini tal cual (decision de Johnny, 11-oct-2026).
    Va pegada al borde del canvas y centrada verticalmente en la zona de
    contenido (en 4:5, la zona sobre el icono); el texto ocupa el lado opuesto
    con la misma altura de caja que la imagen."""
    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("texto_lateral requiere 'imagen_escena' en el slide")

    texto = slide.get("texto_cuerpo")
    if not texto:
        raise CompositorError("texto_lateral requiere 'texto_cuerpo' en el slide")

    lado = slide.get("lado_imagen", "izquierda")
    if lado not in ("izquierda", "derecha"):
        raise CompositorError(f"lado_imagen invalido: {lado} (validos: izquierda, derecha)")

    warnings = []
    if "porcentaje_imagen" in slide or "ancla_recorte" in slide:
        warnings.append("porcentaje_imagen/ancla_recorte ignorados (texto_lateral usa imagen 9:16 fija de 540x960, sin recorte)")

    canvas_w = CANVAS[aspecto]["w"]
    zona_top, zona_bottom = _zona_contenido(canvas, aspecto)
    img_y = round((zona_top + zona_bottom - LATERAL_IMG_H) / 2)

    scene = _load_scene(imagen_escena, assets_dir)
    scene_fit, off_x, off_y = _colocar_imagen(scene, LATERAL_IMG_W, LATERAL_IMG_H, "texto_lateral", warnings)

    if lado == "izquierda":
        img_x = 0
        text_x0 = LATERAL_IMG_W + round(canvas_w * 0.06)
        text_x1 = canvas_w - round(canvas_w * 0.06)
        align = "left"
    else:
        img_x = canvas_w - LATERAL_IMG_W
        text_x0 = round(canvas_w * 0.06)
        text_x1 = img_x - round(canvas_w * 0.06)
        align = "right"

    canvas.paste(scene_fit, (img_x + off_x, img_y + off_y))

    r = render_text_block(canvas, texto, "cuerpo", (text_x0, img_y, text_x1 - text_x0, LATERAL_IMG_H), align=align)
    if r["truncated"]:
        warnings.append("texto_cuerpo truncado (BASE, texto_lateral)")
    return {"warnings": warnings}


def _compose_lockup_cierre(canvas, slide, aspecto, assets_dir):
    """Lockup vertical (simbolo + wordmark) centrado sobre parchment liso.
    En 4:5 es la ultima slide del carrusel; en 9:16 es un recurso opcional
    para el momento del guion en que se nombra la marca. Sin texto ni
    imagen: la marca va sola, con su espacio de proteccion intacto."""
    canvas_w = CANVAS[aspecto]["w"]
    zona_top, zona_bottom = usable_zone(aspecto)[0], usable_zone(aspecto)[1]

    lockup = _lockup_vertical(LOCKUP_W)
    x = (canvas_w - lockup.width) / 2
    y = (zona_top + zona_bottom - lockup.height) / 2
    _paste_brand_mark(canvas, lockup, x, y)
    return {"warnings": []}


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
    if layout == "lockup_cierre":
        return _compose_lockup_cierre(canvas, slide, aspecto, assets_dir)
    raise CompositorError(f"base.compose no maneja el layout: {layout}")
