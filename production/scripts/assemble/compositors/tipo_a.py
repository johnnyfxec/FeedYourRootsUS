# Compositor Tipo A -- Contenedor Escalable (Seccion 2.1 de la arquitectura).
# El marco se redimensiona segun % imagen/texto del slide; la ventana interior
# escala con el mismo factor. Aplica a: marco_grande, doble_marco (y las
# portadas marco_grande_portada / marco_grande_cuadrado).

import os
from PIL import Image

from layout_specs import (
    CANVAS, ASSETS, WINDOWS, ROTATED_WINDOWS, BBOX, PORTADA_WIDTHS, TYPOGRAPHY, usable_zone,
    usable_zone_x,
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

    # El texto bajo el marco va en `texto_pie`, rol SUBTITULO (Lora negrita
    # cursiva): el titulo dorado con borde es exclusivo de las portadas, para
    # no restarle peso (decision de Johnny, 11-oct-2026). Centrado en el
    # espacio que deja el marco.
    warnings = []
    pie = slide.get("texto_pie")
    if not pie:
        raise CompositorError(f"{layout_name} requiere 'texto_pie' en el slide")
    r = render_text_block(canvas, pie, "subtitulo", texto_box)
    if r["truncated"]:
        warnings.append(f"texto_pie truncado (Tipo A, {layout_name})")

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

    # ORDEN DE CAPAS (corregido 20-oct-2026, defecto real en PZA_10.4 S3 detectado por
    # Johnny): antes las dos escenas se pegaban ANTES que el frame_asset, asi que cualquier
    # parte de la escena TRASERA que no quedaba cubierta por su propio marco (overflow del
    # recorte+rotacion) se veia "flotando" encima del fondo, invadiendo visualmente la zona
    # del marco FRONTAL. Arreglo pedido por Johnny -- simple, sin mascaras: escena trasera
    # al fondo, el PNG del marco (con su propia transparencia) en medio, y la escena FRONTAL
    # pegada AL FINAL, encima de todo. Asi el marco tapa cualquier sobrante de la escena
    # trasera, y la escena frontal siempre gana sobre el marco.
    _paste_rotated_scene(canvas, scene1, windows["trasero"], ancla)

    frame_asset = _load_asset("doble_marco", aspecto, assets_dir)
    canvas.alpha_composite(frame_asset, (0, 0))

    _paste_rotated_scene(canvas, scene2, windows["frontal"], ancla)

    # Pie opcional (`texto_pie`, rol subtitulo) en la franja libre sobre los
    # marcos: desde el margen superior hasta el borde de contenido del asset
    # (BBOX), con 10 px de aire. Antes la caja se calculaba con la zona
    # segura de 9:16 y en 4:5 medía 10 px de alto (el titulo siempre salia
    # truncado).
    warnings = []
    pie = slide.get("texto_pie")
    if pie:
        canvas_w = CANVAS[aspecto]["w"]
        top = 14 if aspecto == "4:5" else usable_zone(aspecto)[0]
        bottom = BBOX["doble_marco"][aspecto]["y0"] - 10
        box = (round(canvas_w * 0.08), round(top), round(canvas_w * 0.84), round(bottom - top))
        r = render_text_block(canvas, pie, "subtitulo", box)
        if r["truncated"]:
            warnings.append("texto_pie truncado (Tipo A, doble_marco)")

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

    # Bloque de texto: ancho fijo medido, anclado (no centrado) a un
    # margen fijo debajo del borde inferior del marco -- fix del bug de
    # centrado vertical (ver Arquitectura v1.1 Seccion 8).
    frame_bottom = frame_y + frame_h_final
    MARGEN_MARCO_TITULO = 20  # px -- punto de partida, ajustar tras revision visual
    titulo_y = frame_bottom + MARGEN_MARCO_TITULO
    espacio_disponible = canvas_h - titulo_y
    texto_x = (canvas_w - texto_w_target) / 2

    r = render_text_block_top(
        canvas, titulo, "titulo",
        round(texto_x), round(titulo_y), texto_w_target, round(espacio_disponible),
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
    if not titulo:
        raise CompositorError("marco_grande_cuadrado requiere texto_titulo")
    if slide.get("texto_subtitulo"):
        raise CompositorError(
            "marco_grande_cuadrado ya NO admite texto_subtitulo (corregido 29-oct-2026: "
            "se elimino para liberar alto y evitar que el titulo quedara tapado por el "
            "right rail de iconos durante reproduccion -- ver Layout Specs Seccion 15). "
            "Si el brief trae subtitulo para esta pieza, quitarlo del config."
        )

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

    # Texto debajo de la ventana, en el espacio libre hasta el borde del
    # canvas. CORREGIDO 29-oct-2026 (bug real, no el de SAFE_PRACTICAL
    # vertical que se corrigio antes): el ancho de 898px invadia el right
    # rail de iconos (like/comentar/guardar/perfil) durante reproduccion en
    # Instagram/TikTok/Shorts -- confirmado con captura real de un video
    # publicado. El subtitulo se elimino (ver arriba) para que el titulo
    # tenga todo el alto libre y pueda crecer a mas lineas sin reducirse
    # tanto al angostarse. Ancho ahora viene de usable_zone_x() (13%
    # simetrico cada lado, calibrado contra medicion real de Johnny:
    # boton de 8mm sobre 68.5mm de pantalla = 11.68%, redondeado con
    # colchon) -- ver layout_specs.py.
    # CORREGIDO 29-oct-2026 (segunda pasada, tras revision visual de Johnny):
    # el Y fijo de 1234px quedo de cuando el layout SI tenia subtitulo (medido
    # con editor_posicion_texto.html sobre ese mockup viejo) -- al quitar el
    # subtitulo el hueco disponible cambio pero el titulo se seguia anclando
    # al mismo Y de siempre, quedando pegado al vine grande y lejos del vine
    # chico de abajo (descentrado). El hueco real para texto esta entre los
    # dos vines decorativos que trae fijos el PNG del marco (medido con
    # pixeles reales, no estimado): vine grande termina en y=1209, vine chico
    # empieza en y=1599 -> hueco de 390px. Centrar el bloque ahi con
    # render_text_block (centrado automatico), no con render_text_block_top
    # (que ancla arriba sin centrar).
    # CORREGIDO 29-oct-2026 (tercera pasada, Johnny midio con precision de
    # pixel que un titulo de 4 lineas quedaba tocando AMBOS vines -- 0px de
    # margen arriba, 1px abajo -- aun centrado matematicamente, porque el
    # bloque de texto llenaba el hueco completo de 390px. Centrado correcto
    # no es suficiente si no queda aire: se reserva un colchon fijo de 24px
    # arriba y 24px abajo (48px total) para que el titulo NUNCA toque los
    # vines sin importar si son 2, 3 o 4 lineas balanceadas.
    VINE_GRANDE_FIN = 1209
    VINE_CHICO_INICIO = 1599
    PADDING_VERTICAL = 24
    _, _, TITULO_ANCHO = usable_zone_x(aspecto)
    TITULO_ANCHO = round(TITULO_ANCHO)

    titulo_x = round((canvas_w - TITULO_ANCHO) / 2)
    caja_y = VINE_GRANDE_FIN + PADDING_VERTICAL
    hueco_h = (VINE_CHICO_INICIO - VINE_GRANDE_FIN) - (2 * PADDING_VERTICAL)

    warnings = []
    r = render_text_block(canvas, titulo, "titulo_cuadrado", (titulo_x, caja_y, TITULO_ANCHO, hueco_h))
    if r["truncated"]:
        warnings.append("texto_titulo truncado (Tipo A, marco_grande_cuadrado)")

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
