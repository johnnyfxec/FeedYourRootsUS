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


def _wrap_text(text, font, max_width, draw):
    """Word-wrap simple: acumula palabras mientras quepan en max_width."""
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        w = draw.textlength(trial, font=font)
        if w <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _block_height(lines, font, line_spacing=1.2):
    ascent, descent = font.getmetrics()
    line_h = (ascent + descent) * line_spacing
    return line_h * len(lines), line_h


def fit_text(text, role, max_width, max_height, draw):
    """Aplica la regla de ajuste automatico completa de la Seccion 3:
    word-wrap al tamano base -> si excede alto, reduce de a STEP_PX hasta
    MIN_SIZE_FRACTION -> si aun asi no cabe, trunca con '...' en la ultima
    linea que si entra. Retorna (lines, font, truncated: bool)."""
    if role not in TYPOGRAPHY:
        raise TextRenderError(f"rol de texto desconocido: {role}")

    spec = TYPOGRAPHY[role]
    base_size = spec["size"]
    min_size = int(base_size * MIN_SIZE_FRACTION)

    size = base_size
    while size >= min_size:
        font = _load_font(spec["font"], size)
        lines = _wrap_text(text, font, max_width, draw)
        height, _ = _block_height(lines, font, line_spacing=spec.get("line_spacing", 1.2))
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


def render_text_block(canvas, text, role, box, align="center"):
    """Renderiza `text` con el rol dado dentro de `box` (x, y, w, h) sobre
    `canvas` (PIL Image RGBA). Retorna dict con 'truncated' (bool) para que
    main.py registre la advertencia en el log de ensamblado (Seccion 3, paso 4)
    sin detener el proceso."""
    if role not in TYPOGRAPHY:
        raise TextRenderError(f"rol de texto desconocido: {role}")

    spec = TYPOGRAPHY[role]
    x, y, w, h = box
    draw = ImageDraw.Draw(canvas)

    lines, font, truncated = fit_text(text, role, w, h, draw)
    _, line_h = _block_height(lines, font, line_spacing=spec.get("line_spacing", 1.2))
    total_h, _ = _block_height(lines, font, line_spacing=spec.get("line_spacing", 1.2))
    cursor_y = y + max(0, (h - total_h) / 2)  # centrado vertical en el box

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


def render_text_block_rotated(canvas, text, role, w, h, angle, cx, cy, align="center"):
    """Como render_text_block, pero para texto que vive sobre una superficie
    rotada (etiqueta_colgante, nota_esquina medidas con medidor_esquinas.html).
    Renderiza en un lienzo transparente de (w, h), rota ese lienzo al angulo
    real de la superficie, y lo pega centrado en (cx, cy) del canvas. Mismo
    principio que _paste_rotated_scene en compositors/tipo_a.py, pero para
    texto en vez de imagen. Retorna dict con 'truncated' igual que
    render_text_block."""
    layer = Image.new("RGBA", (round(w), round(h)), (0, 0, 0, 0))
    result = render_text_block(layer, text, role, (0, 0, round(w), round(h)), align=align)

    rotated = layer.rotate(-angle, expand=True, resample=Image.BICUBIC)
    paste_x = round(cx - rotated.width / 2)
    paste_y = round(cy - rotated.height / 2)
    canvas.alpha_composite(rotated, (paste_x, paste_y))

    return result


def render_text_block_rotated(canvas, text, role, w, h, angle, cx, cy, align="center"):
    """Como render_text_block, pero para texto que vive sobre una superficie
    rotada (etiqueta_colgante, nota_esquina medidas con medidor_esquinas.html).
    Renderiza en un lienzo transparente de (w, h), rota ese lienzo al angulo
    real de la superficie, y lo pega centrado en (cx, cy) del canvas. Mismo
    principio que _paste_rotated_scene en compositors/tipo_a.py, pero para
    texto en vez de imagen. Retorna dict con 'truncated' igual que
    render_text_block."""
    layer = Image.new("RGBA", (round(w), round(h)), (0, 0, 0, 0))
    result = render_text_block(layer, text, role, (0, 0, round(w), round(h)), align=align)

    rotated = layer.rotate(-angle, expand=True, resample=Image.BICUBIC)
    paste_x = round(cx - rotated.width / 2)
    paste_y = round(cy - rotated.height / 2)
    canvas.alpha_composite(rotated, (paste_x, paste_y))

    return result


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
