# Renderizado de texto (Seccion 3) y recorte de imagen cover (Seccion 4)
# de la arquitectura. Cada ROL de texto tiene fuente/tamano/color fijos en
# layout_specs.TYPOGRAPHY -- este modulo solo aplica esas reglas, no decide
# valores nuevos.

import os
from PIL import Image, ImageDraw, ImageFont

from layout_specs import TYPOGRAPHY, FONTS_DIR

MIN_SIZE_FRACTION = 0.70   # Seccion 3: nunca baja de 70% del tamano base
STEP_PX = 2                # Seccion 3: reduce en pasos de 2px


class TextRenderError(Exception):
    pass


_font_cache = {}


def _load_font(font_file, size):
    key = (font_file, size)
    if key not in _font_cache:
        path = os.path.join(FONTS_DIR, font_file)
        if not os.path.exists(path):
            raise TextRenderError(f"fuente no encontrada: {path}")
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def _wrap_greedy(words, font, max_width, draw):
    """Word-wrap greedy clasico: llena cada linea al maximo antes de saltar.
    Usado solo como paso 1 para contar cuantas lineas hacen falta como minimo
    -- ver _wrap_balanced, que es el que de verdad reparte las palabras."""
    lines = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _wrap_balanced(words, font, max_width, draw):
    """CORREGIDO 29-oct-2026 (revision visual de Johnny sobre PZA_4.2 y 2.1):
    el wrap greedy de siempre llena cada linea al maximo antes de saltar a la
    siguiente, lo que deja con frecuencia una ultima linea 'huerfana' con una
    sola palabra corta suelta (ej. titulo de 34 caracteres -> '5 THINGS EVEN
    A' / '3-YEAR-OLD CAN' / 'DO', con 'DO' solo) -- se ve desordenado y corta
    el titulo en un punto que no respeta unidades de sentido. La solucion no
    es reducir el tamano de fuente (rompe uniformidad de grilla entre piezas,
    senalado por Johnny) ni forzar un maximo de 2 lineas (puede arruinar
    claridad en titulos largos, tambien senalado por Johnny): es reparir las
    MISMAS palabras en el MISMO numero de lineas que ya calculaba el greedy,
    pero balanceando el ancho de cada linea para que ninguna quede como
    resto suelto. Algoritmo: 1) greedy da el numero minimo de lineas N
    necesario a este tamano de fuente; 2) se prueban todos los puntos de
    corte posibles en N-1 lineas (sin reordenar ni quitar palabras) y se
    elige el que minimiza la varianza de ancho entre lineas, con la
    restriccion de que ninguna linea exceda max_width. Determinista, no
    cambia tamano de fuente, no cambia el conteo de lineas del greedy."""
    greedy_lines = _wrap_greedy(words, font, max_width, draw)
    n = len(greedy_lines)
    if n <= 1:
        return greedy_lines

    def ancho(line):
        return draw.textlength(line, font=font)

    best = None
    best_var = None

    def generar_cortes(idx_palabras, cortes_restantes):
        # cortes_restantes = cuantos cortes faltan por colocar (n-1 en total)
        if cortes_restantes == 0:
            yield []
            return
        # el corte debe dejar al menos 1 palabra para cada segmento restante
        for i in range(idx_palabras + 1, len(words) - cortes_restantes + 1):
            for resto in generar_cortes(i, cortes_restantes - 1):
                yield [i] + resto

    for cortes in generar_cortes(0, n - 1):
        idxs = [0] + cortes + [len(words)]
        candidate = [" ".join(words[idxs[i]:idxs[i + 1]]) for i in range(len(idxs) - 1)]
        anchos = [ancho(l) for l in candidate]
        if max(anchos) > max_width:
            continue
        media = sum(anchos) / len(anchos)
        var = sum((a - media) ** 2 for a in anchos)
        if best_var is None or var < best_var:
            best_var = var
            best = candidate

    return best if best is not None else greedy_lines


def _wrap_text(text, font, max_width, draw):
    """Word-wrap con soporte de salto de linea manual (\n). Cada segmento
    separado por \n en el texto original se trata como una linea forzada
    -- respeta la jerarquia retorica decidida en el brief (ver
    FYR_Protocolo_De_Trabajo.md, regla de jerarquia de titulo). Dentro de
    cada segmento forzado, se aplica wrap BALANCEADO (_wrap_balanced) por
    ancho, no greedy puro -- evita lineas huerfanas con una sola palabra
    suelta (ver _wrap_balanced)."""
    lines = []
    for segment in text.split("\n"):
        words = segment.split()
        if not words:
            continue
        lines.extend(_wrap_balanced(words, font, max_width, draw))
    return lines


def _block_height(lines, font, line_spacing=1.2):
    ascent, descent = font.getmetrics()
    line_h = (ascent + descent) * line_spacing
    return line_h * len(lines), line_h


def _altura_tinta_real(lines, font, line_h, stroke_w, draw):
    """Mide el alto real de tinta (incluye stroke y descendentes) de un
    bloque de lineas ya apiladas con line_h, dibujando en y=0 (textbbox es
    lineal en y, no hace falta dibujar en la posicion final). Ver nota en
    fit_text sobre por que esto reemplazo a _block_height para decidir
    tamano de fuente."""
    top = None
    bottom = None
    y = 0
    for line in lines:
        bbox = draw.textbbox((0, y), line, font=font, stroke_width=stroke_w)
        top = bbox[1] if top is None else min(top, bbox[1])
        bottom = bbox[3] if bottom is None else max(bottom, bbox[3])
        y += line_h
    return bottom - top


def fit_text(text, role, max_width, max_height, draw):
    """Aplica la regla de ajuste automatico completa de la Seccion 3:
    word-wrap al tamano base -> si excede alto, reduce de a STEP_PX hasta
    MIN_SIZE_FRACTION -> si aun asi no cabe, trunca con '...' en la ultima
    linea que si entra. Retorna (lines, font, truncated: bool).

    CORREGIDO 29-oct-2026 (Johnny midio con precision de pixel que un titulo
    de 4 lineas se pasaba de su caja pese a que el calculo decia que cabia):
    decide si el bloque cabe midiendo ALTURA DE TINTA REAL (_altura_tinta_real,
    via textbbox) en vez de la aproximacion tipografica (ascent+descent)*
    line_spacing de _block_height -- esa aproximacion no cuenta el stroke_w
    (N px extra fuera del glifo) ni cuanto se pasan los descendentes reales
    de la fuente, y subestimaba el alto real en unos pocos px: suficiente
    para que el bloque pareciera caber y luego se viera tocando los bordes
    de su caja al centrarlo."""
    if role not in TYPOGRAPHY:
        raise TextRenderError(f"rol de texto desconocido: {role}")

    spec = TYPOGRAPHY[role]
    base_size = spec["size"]
    min_size = int(base_size * MIN_SIZE_FRACTION)
    stroke_w = spec.get("stroke_w", 0) if spec.get("stroke") else 0

    size = base_size
    while size >= min_size:
        font = _load_font(spec["font"], size)
        lines = _wrap_text(text, font, max_width, draw)
        _, line_h = _block_height(lines, font, line_spacing=spec.get("line_spacing", 1.2))
        height = _altura_tinta_real(lines, font, line_h, stroke_w, draw)
        if height <= max_height:
            return lines, font, False
        size -= STEP_PX

    # Minimo alcanzado y sigue sin caber: truncar
    font = _load_font(spec["font"], min_size)
    lines = _wrap_text(text, font, max_width, draw)
    _, line_h = _block_height(lines, font, line_spacing=spec.get("line_spacing", 1.2))
    max_lines = max(1, int(max_height // line_h))
    kept = lines[:max_lines]
    if kept:
        last = kept[-1]
        while draw.textlength(last + "…", font=font) > max_width and len(last) > 1:
            last = last[:-1]
        kept[-1] = last + "…"
    return kept, font, True


def _bbox_tinta_real(lines, font, line_h, cursor_y0, cursor_x_de_linea, stroke_w, draw):
    """CORREGIDO 29-oct-2026 (Johnny midio con precision de pixel que un
    titulo de 4 lineas quedaba tocando el vine de arriba Y el de abajo, 0-1px
    de margen, pese a que el centrado matematico via _block_height decia que
    cabia perfecto con margen de sobra). Causa raiz: _block_height aproxima
    el alto del bloque con (ascent+descent)*line_spacing, que es la metrica
    TIPOGRAFICA de la fuente -- no cuenta el stroke_w (dibuja N px extra
    fuera del glifo en cada direccion) ni cuanto se pasan los descendentes
    reales (ej. el parentesis de cierre ')') de esa aproximacion. Para
    titulos de 2-3 lineas el margen de error pasaba desapercibido; a 4
    lineas se volvia visible. Esta funcion mide el bbox de TINTA REAL
    (draw.textbbox, que si incluye stroke) de las lineas ya renderizadas en
    sus posiciones candidatas, para poder centrar por tinta real en vez de
    por la aproximacion tipografica. Retorna (top, bottom) en coordenadas
    del canvas."""
    top = None
    bottom = None
    y = cursor_y0
    for i, line in enumerate(lines):
        x = cursor_x_de_linea(i, line)
        bbox = draw.textbbox((x, y), line, font=font, stroke_width=stroke_w)
        top = bbox[1] if top is None else min(top, bbox[1])
        bottom = bbox[3] if bottom is None else max(bottom, bbox[3])
        y += line_h
    return top, bottom


def render_text_block(canvas, text, role, box, align="center"):
    """Renderiza `text` con el rol dado dentro de `box` (x, y, w, h) sobre
    `canvas` (PIL Image RGBA). Retorna dict con 'truncated' (bool) para que
    main.py registre la advertencia en el log de ensamblado (Seccion 3, paso 4)
    sin detener el proceso. Centrado vertical por TINTA REAL, no por metrica
    tipografica aproximada -- ver _bbox_tinta_real."""
    if role not in TYPOGRAPHY:
        raise TextRenderError(f"rol de texto desconocido: {role}")

    spec = TYPOGRAPHY[role]
    x, y, w, h = box
    draw = ImageDraw.Draw(canvas)
    stroke_w = spec.get("stroke_w", 0) if spec.get("stroke") else 0

    lines, font, truncated = fit_text(text, role, w, h, draw)
    _, line_h = _block_height(lines, font, line_spacing=spec.get("line_spacing", 1.2))

    def cursor_x_de_linea(i, line):
        line_w = draw.textlength(line, font=font)
        if align == "center":
            return x + (w - line_w) / 2
        elif align == "left":
            return x
        return x + (w - line_w)

    # Paso 1: bbox de tinta real con un cursor_y0 provisional (y=0 basta,
    # textbbox es lineal en y) para saber cuanto ocupa el bloque de verdad.
    top0, bottom0 = _bbox_tinta_real(lines, font, line_h, 0, cursor_x_de_linea, stroke_w, draw)
    alto_tinta_real = bottom0 - top0

    # Paso 2: centrar ese alto real dentro del box, y resolver el cursor_y0
    # que al dibujar deja la tinta exactamente centrada (no el cursor de
    # baseline tipografico).
    offset_centrado = y + max(0, (h - alto_tinta_real) / 2)
    cursor_y = offset_centrado - top0

    for i, line in enumerate(lines):
        cursor_x = cursor_x_de_linea(i, line)
        if stroke_w > 0:
            draw.text(
                (cursor_x, cursor_y), line, font=font,
                fill=spec["color"], stroke_width=stroke_w,
                stroke_fill=spec["stroke"],
            )
        else:
            draw.text((cursor_x, cursor_y), line, font=font, fill=spec["color"])
        cursor_y += line_h

    return {"truncated": truncated, "lines_rendered": len(lines)}


def render_text_block_top(canvas, text, role, x, y, w, max_h, align="center"):
    """Como render_text_block, pero SIN centrado vertical automatico -- el
    texto arranca exactamente en `y`, sin offset. Existe porque el centrado
    automatico de render_text_block genera un offset impredecible cuando el
    tamano de fuente se reduce internamente (fit_text puede bajar de 93 a
    91px por ejemplo), y ese offset se acumula en cascada cuando se
    encadenan varios bloques de texto (titulo -> subtitulo) uno debajo del
    otro con una Y calculada a partir de donde termino el anterior.
    Retorna dict con 'truncated' y 'height' (alto real usado, para que el
    llamador pueda encadenar el siguiente bloque con precision)."""
    if role not in TYPOGRAPHY:
        raise TextRenderError(f"rol de texto desconocido: {role}")

    spec = TYPOGRAPHY[role]
    draw = ImageDraw.Draw(canvas)

    lines, font, truncated = fit_text(text, role, w, max_h, draw)
    total_h, line_h = _block_height(lines, font, line_spacing=spec.get("line_spacing", 1.2))

    cursor_y = y  # SIN offset de centrado -- arranca exactamente en y
    for line in lines:
        line_w = draw.textlength(line, font=font)
        if align == "center":
            cursor_x = x + (w - line_w) / 2
        elif align == "left":
            cursor_x = x
        else:
            cursor_x = x + (w - line_w)

        if spec.get("stroke") and spec.get("stroke_w", 0) > 0:
            draw.text(
                (cursor_x, cursor_y), line, font=font,
                fill=spec["color"], stroke_width=spec["stroke_w"],
                stroke_fill=spec["stroke"],
            )
        else:
            draw.text((cursor_x, cursor_y), line, font=font, fill=spec["color"])
        cursor_y += line_h

    return {"truncated": truncated, "lines_rendered": len(lines), "height": total_h, "line_h": line_h}


def crop_to_fill(image, target_w, target_h, anchor="center"):
    """Recorte 'cover' estandar (Seccion 4) -- equivalente a object-fit: cover.
    anchor: 'center' (default) o 'top'. Cualquier otro valor es un error
    explicito, no un fallback silencioso (fail loudly, Seccion 5.3)."""
    if anchor not in ("center", "top"):
        raise TextRenderError(f"ancla_recorte invalida: {anchor} (validos: center, top)")

    img_w, img_h = image.size
    scale = max(target_w / img_w, target_h / img_h)
    new_w, new_h = round(img_w * scale), round(img_h * scale)
    resized = image.resize((new_w, new_h), Image.LANCZOS)

    crop_x = (new_w - target_w) / 2
    if anchor == "center":
        crop_y = (new_h - target_h) / 2
    else:  # top
        crop_y = 0

    crop_x, crop_y = round(crop_x), round(crop_y)
    return resized.crop((crop_x, crop_y, crop_x + target_w, crop_y + target_h))
