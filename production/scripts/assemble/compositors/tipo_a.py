# Compositor Tipo A -- Contenedor Escalable (Seccion 2.1 de la arquitectura).
# El marco se redimensiona segun % imagen/texto del slide; la ventana interior
# escala con el mismo factor. Aplica a: marco_grande, doble_marco.

import os
from PIL import Image, ImageDraw

from layout_specs import (
    CANVAS, ASSETS, WINDOWS, ROTATED_WINDOWS, PORTADA_WIDTHS, TYPOGRAPHY, usable_zone,
)
from text_renderer import crop_to_fill, render_text_block, render_text_block_top


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


def _compose_marco_grande(canvas, slide, aspecto, assets_dir, layout_name="marco_grande"):
    porcentaje_imagen = slide.get("porcentaje_imagen")
    if porcentaje_imagen is None:
        raise CompositorError(f"{layout_name} requiere 'porcentaje_imagen' en el slide")

    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError(f"{layout_name} requiere 'imagen_escena' en el slide")

    if layout_name not in WINDOWS or aspecto not in WINDOWS[layout_name]:
        raise CompositorError(f"ventana no medida para {layout_name} en aspecto {aspecto}")

    win = WINDOWS[layout_name][aspecto]
    asset_w, asset_h = win["asset_w"], win["asset_h"]

    margen_top, margen_bottom, usable_h = usable_zone(aspecto)
    canvas_w = CANVAS[aspecto]["w"]

    porcentaje_texto = 100 - porcentaje_imagen
    image_zone_height = usable_h * (porcentaje_imagen / 100)
    text_zone_height = usable_h * (porcentaje_texto / 100)

    frame_scale = image_zone_height / asset_h
    frame_w_final = asset_w * frame_scale
    frame_h_final = asset_h * frame_scale

    frame_x = (canvas_w - frame_w_final) / 2
    frame_y = margen_top

    frame_asset = _load_asset(layout_name, aspecto, assets_dir)
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
        raise CompositorError(f"{layout_name} requiere texto_titulo o texto_subtitulo")

    cursor_y = texto_box[1]
    box_w = texto_box[2]  # texto_box[2] YA es el ancho (w), no x1 -- no restar texto_box[0]
    if titulo:
        remaining_h = texto_box[3] - (cursor_y - texto_box[1])
        titulo_h = remaining_h if not subtitulo else remaining_h * 0.6
        r = render_text_block(canvas, titulo, "titulo", (texto_box[0], round(cursor_y), box_w, round(titulo_h)))
        if r["truncated"]:
            warnings.append(f"texto_titulo truncado (Tipo A, {layout_name})")
        cursor_y += titulo_h
    if subtitulo:
        remaining_h = texto_box[3] - (cursor_y - texto_box[1])
        r = render_text_block(canvas, subtitulo, "subtitulo", (texto_box[0], round(cursor_y), box_w, round(remaining_h)))
        if r["truncated"]:
            warnings.append(f"texto_subtitulo truncado (Tipo A, {layout_name})")

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
        margen_top, _, _ = usable_zone(aspecto)
        box = (round(canvas_w * 0.08), 20, round(canvas_w * 0.84), round(margen_top - 30))
        r = render_text_block(canvas, titulo, "titulo", box)
        if r["truncated"]:
            warnings.append("texto_titulo truncado (Tipo A, doble_marco)")

    return {"warnings": warnings}


def _compose_marco_grande_portada(canvas, slide, aspecto, assets_dir):
    """Portada de carrusel 4:5 -- SOLO titulo, sin subtitulo. El marco se
    escala por ANCHO FIJO (no por porcentaje_imagen/altura como
    marco_grande), replicando el ancho absoluto medido en la portada 9:16
    (mismo ancho de canvas, 1080px en ambos). Decision de Johnny: el 4:5
    debe verse en el feed con el mismo peso visual de marco que el 9:16.
    El bloque de texto se centra verticalmente entre el borde inferior del
    marco y el borde inferior del canvas."""
    if aspecto not in PORTADA_WIDTHS:
        raise CompositorError(f"marco_grande_portada no tiene anchos medidos para aspecto {aspecto}")

    titulo = slide.get("texto_titulo")
    if not titulo:
        raise CompositorError("marco_grande_portada requiere texto_titulo")
    if slide.get("texto_subtitulo"):
        raise CompositorError("marco_grande_portada no acepta texto_subtitulo (solo portadas de video 9:16 llevan subtitulo)")

    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("marco_grande_portada requiere 'imagen_escena'")

    if "marco_grande" not in WINDOWS or aspecto not in WINDOWS["marco_grande"]:
        raise CompositorError(f"ventana no medida para marco_grande en aspecto {aspecto}")

    win = WINDOWS["marco_grande"][aspecto]
    asset_w, asset_h = win["asset_w"], win["asset_h"]
    canvas_w = CANVAS[aspecto]["w"]
    canvas_h = CANVAS[aspecto]["h"]

    marco_w_target = PORTADA_WIDTHS[aspecto]["marco_w"]
    texto_w_target = PORTADA_WIDTHS[aspecto]["texto_w"]

    # Escala por ANCHO (no por altura como marco_grande normal)
    frame_scale = marco_w_target / asset_w
    frame_w_final = asset_w * frame_scale
    frame_h_final = asset_h * frame_scale

    frame_x = (canvas_w - frame_w_final) / 2
    frame_y = round(canvas_h * 0.03)  # margen estetico minimo superior

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
    # +2% de margen para que el recorte cubra toda la ventana sin dejar
    # bordes blancos visibles en las esquinas del marco.
    overscan = 1.02
    scene_cropped = crop_to_fill(scene, round(ventana_w * overscan), round(ventana_h * overscan), anchor=ancla)
    paste_x = round(ventana_x - (ventana_w * (overscan - 1)) / 2)
    paste_y = round(ventana_y - (ventana_h * (overscan - 1)) / 2)

    canvas.paste(scene_cropped, (paste_x, paste_y))
    canvas.alpha_composite(frame_resized, (round(frame_x), round(frame_y)))

    # Bloque de texto: ancho fijo medido, centrado verticalmente entre el
    # borde inferior del marco y el borde inferior del canvas.
    frame_bottom = frame_y + frame_h_final
    espacio_disponible = canvas_h - frame_bottom
    texto_x = (canvas_w - texto_w_target) / 2

    r = render_text_block(
        canvas, titulo, "titulo",
        (round(texto_x), round(frame_bottom), texto_w_target, round(espacio_disponible)),
    )

    warnings = []
    if r["truncated"]:
        warnings.append("texto_titulo truncado (Tipo A, marco_grande_portada)")

    return {"warnings": warnings}


def _compose_marco_grande_cuadrado(canvas, slide, aspecto, assets_dir):
    """Portada de reel/video 9:16 -- asset FIJO, lienzo completo (1080x1920)
    con vid y hoja ya integrados en su posicion final, sin escalado
    dinamico (a diferencia de marco_grande, que escala por porcentaje_imagen).
    Ventana cuadrada ya medida recibe la imagen de escena. Titulo y
    subtitulo (si existen) van debajo de la ventana, en el espacio libre
    del propio asset."""
    if "marco_grande_cuadrado" not in WINDOWS or aspecto not in WINDOWS["marco_grande_cuadrado"]:
        raise CompositorError(f"ventana no medida para marco_grande_cuadrado en aspecto {aspecto}")

    imagen_escena = slide.get("imagen_escena")
    if not imagen_escena:
        raise CompositorError("marco_grande_cuadrado requiere 'imagen_escena'")

    titulo = slide.get("texto_titulo")
    subtitulo = slide.get("texto_subtitulo")
    if not titulo and not subtitulo:
        raise CompositorError("marco_grande_cuadrado requiere texto_titulo o texto_subtitulo")

    win = WINDOWS["marco_grande_cuadrado"][aspecto]
    canvas_w = CANVAS[aspecto]["w"]
    canvas_h = CANVAS[aspecto]["h"]
    ancla = slide.get("ancla_recorte", "center")

    scene = _load_scene(imagen_escena, assets_dir)
    overscan = 1.02
    scene_cropped = crop_to_fill(scene, round(win["w"] * overscan), round(win["h"] * overscan), anchor=ancla)
    paste_x = round(win["x"] - (win["w"] * (overscan - 1)) / 2)
    paste_y = round(win["y"] - (win["h"] * (overscan - 1)) / 2)
    canvas.paste(scene_cropped, (paste_x, paste_y))

    frame_asset = _load_asset("marco_grande_cuadrado", aspecto, assets_dir)
    canvas.alpha_composite(frame_asset, (0, 0))

    # Texto debajo de la ventana, en el espacio libre hasta el margen
    # practico inferior del canvas (este SI usa SAFE_PRACTICAL/usable_zone,
    # es 9:16 real con proteccion de UI de reel).
    _, margen_bottom, _ = usable_zone(aspecto)
    # Y de inicio del titulo medida directamente sobre el asset real (no
    # derivada de la ventana) -- linea superior del titulo en el mockup,
    # medida con medidor_esquinas.html: y=1389.2 sobre canvas 1080x1920.
    # La caja se extiende hasta el borde REAL del canvas (no hasta
    # margen_bottom de zona segura) para que el tamano de fuente ya
    # calibrado (93px) nunca se reduzca por falta de espacio -- la Y de
    # inicio medida ya considera zona segura, no hay que restringir de nuevo.
    TITULO_Y_MEDIDO = 1234.0  # Y superior real, medido con editor_posicion_texto.html sobre mockup real
    TITULO_ANCHO = 898  # ancho medido, mismo valor absoluto que en portada 4:5
    SUBTITULO_ANCHO = round(TITULO_ANCHO * 0.65)  # 65% del ancho del titulo

    titulo_x = round((canvas_w - TITULO_ANCHO) / 2)
    subtitulo_x = round((canvas_w - SUBTITULO_ANCHO) / 2)
    max_h_disponible = canvas_h - TITULO_Y_MEDIDO

    # Espacio fijo entre titulo y subtitulo, medido con medidor_esquinas.html
    # sobre el mockup real (78.3px entre la ultima linea del titulo y la
    # primera del subtitulo) -- no se calcula como fraccion del espacio
    # total disponible, que dio resultados erraticos con textos de largo
    # variable.
    SUBTITULO_Y_MEDIDO = 1454.0  # Y superior real del subtitulo, medido directamente con editor_posicion_texto.html -- reemplaza el calculo encadenado (titulo + line_h + espacio) que causaba errores acumulados.

    # Ambas posiciones Y son ABSOLUTAS, medidas directamente con
    # editor_posicion_texto.html sobre el mockup real -- no se calculan
    # de forma encadenada (titulo -> espacio -> subtitulo), que fue la
    # fuente de varios bugs de acumulacion de error. Cada bloque de texto
    # se posiciona independiente, en su Y ya confirmada.
    warnings = []
    if titulo:
        r = render_text_block_top(canvas, titulo, "titulo", titulo_x, round(TITULO_Y_MEDIDO), TITULO_ANCHO, max_h_disponible)
        if r["truncated"]:
            warnings.append("texto_titulo truncado (Tipo A, marco_grande_cuadrado)")
    if subtitulo:
        sub_max_h = canvas_h - SUBTITULO_Y_MEDIDO
        r = render_text_block_top(canvas, subtitulo, "subtitulo", subtitulo_x, round(SUBTITULO_Y_MEDIDO), SUBTITULO_ANCHO, sub_max_h)
        if r["truncated"]:
            warnings.append("texto_subtitulo truncado (Tipo A, marco_grande_cuadrado)")

    return {"warnings": warnings}


def compose(canvas, slide, aspecto, assets_dir):
    layout = slide.get("layout")
    if layout == "marco_grande":
        return _compose_marco_grande(canvas, slide, aspecto, assets_dir, layout_name="marco_grande")
    if layout == "marco_grande_cuadrado":
        return _compose_marco_grande_cuadrado(canvas, slide, aspecto, assets_dir)
    if layout == "marco_grande_portada":
        return _compose_marco_grande_portada(canvas, slide, aspecto, assets_dir)
    if layout == "doble_marco":
        return _compose_doble_marco(canvas, slide, aspecto, assets_dir)
    raise CompositorError(f"tipo_a.compose no maneja el layout: {layout}")
